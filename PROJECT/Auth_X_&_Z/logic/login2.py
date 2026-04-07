# # login2.py
# import json
# def test_login(url, cfile):
#     creds = json.load(open(cfile))
#     findings = []
#     # use creds["user1"], creds["user2"], creds["admin"]
#     return findings



import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ── keyword lists ─────────────────────────────────────────────────
# username: ordered by confidence (most specific first)
USERNAME_KEYS = [
    "email", "username", "user_name", "user-name",
    "login", "identifier", "account", "uname",
    "userid", "user_id", "user-id",
    "phone", "mobile",        # some sites use phone as primary identifier
    "name",                   # last resort — very generic
]

PASSWORD_KEYS = [
    "password", "passwd", "pass", "pwd",
    "psw", "secret", "pin",
]

SUBMIT_KEYS = [
    "login", "signin", "sign_in", "sign-in",
    "submit", "enter", "go", "continue",
    "log_in", "log-in", "logon",
]


def _score_field(inp, key_list):
    """
    Return a score for how likely this <input> matches a semantic role.
    Checks name, id, placeholder, and aria-label against keywords.
    Higher score = stronger match.
    """
    score = 0
    attrs = [
        inp.get("name",         "").lower(),
        inp.get("id",           "").lower(),
        inp.get("placeholder",  "").lower(),
        inp.get("aria-label",   "").lower(),
        inp.get("autocomplete", "").lower(),
    ]
    for i, keyword in enumerate(key_list):
        weight = len(key_list) - i   # earlier in list = higher weight
        for attr in attrs:
            if keyword == attr:          # exact match
                score += weight * 3
            elif keyword in attr:        # partial match
                score += weight * 1
    return score


def _extract_fields(form, base_url):
    """
    Given a BeautifulSoup <form> tag, extract and classify all inputs.
    Returns a normalised dict compatible with test_rate_limit / check_csrf.
    """
    result = {
        "action":   urljoin(base_url, form.get("action", base_url)),
        "method":   form.get("method", "POST").upper(),
        "fields":   {},
        "inputs":   [],
    }

    best_user = {"score": 0, "name": None}
    best_pass = {"score": 0, "name": None}

    for inp in form.find_all("input"):
        t = inp.get("type", "text").lower()
        n = inp.get("name", "")
        v = inp.get("value", "")

        result["inputs"].append({"type": t, "name": n, "value": v})

        if t == "password":
            # password type is unambiguous — always wins
            result["fields"]["password"] = n

        elif t == "hidden":
            result["fields"][n] = v    # CSRF tokens land here

        elif t in ("text", "email", "tel", "number"):
            # score it; keep the highest
            s = _score_field(inp, USERNAME_KEYS)
            if t == "email":
                s += 20               # <input type="email"> is a strong hint
            if s > best_user["score"]:
                best_user = {"score": s, "name": n}

        elif t in ("submit", "button"):
            result["fields"]["_submit"] = n

    # commit best username candidate
    if best_user["name"]:
        result["fields"]["username"] = best_user["name"]

    # also check <button type="submit"> tags
    for btn in form.find_all("button", type=re.compile(r"submit", re.I)):
        result["fields"].setdefault("_submit", btn.get("name", ""))

    return result


# ── Layer 1 + 2: requests + BeautifulSoup ────────────────────────

def _try_requests(url):
    """Try to find the login form with plain HTTP (no JS)."""
    try:
        resp = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })
    except Exception as e:
        print(f"  [!] requests failed: {e}")
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    # rank every form that has at least one password input
    candidates = []
    for form in soup.find_all("form"):
        pw = form.find("input", {"type": "password"})
        if not pw:
            continue
        # score the form itself: how many login-related inputs does it have?
        form_score = sum(
            _score_field(i, USERNAME_KEYS + PASSWORD_KEYS + SUBMIT_KEYS)
            for i in form.find_all("input")
        )
        candidates.append((form_score, form))

    if not candidates:
        return None

    # pick the highest-scoring form
    candidates.sort(key=lambda x: x[0], reverse=True)
    best_form = candidates[0][1]
    return _extract_fields(best_form, url)


# ── Layer 3: Selenium fallback for JS-rendered pages ─────────────

def _try_selenium(url):
    """Fallback: render the page in Chrome, then parse with BS4."""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By

        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--log-level=3")

        driver = webdriver.Chrome(options=opts)
        driver.get(url)

        # wait up to 8s for a password field to appear
        try:
            WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
            )
        except Exception:
            pass  # page loaded but no password field found — still parse what we have

        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, "html.parser")
        for form in soup.find_all("form"):
            if form.find("input", {"type": "password"}):
                return _extract_fields(form, url)

        # SPA fallback: no <form> tags, but password input exists outside a form
        pw = soup.find("input", {"type": "password"})
        if pw:
            # build a synthetic form using the parent container
            parent = pw.find_parent(["div", "section", "main"]) or soup.body
            return _extract_fields(parent, url) if parent else None

        return None

    except ImportError:
        print("  [!] selenium not installed — skipping JS fallback")
        return None
    except Exception as e:
        print(f"  [!] selenium error: {e}")
        return None


# ── Public entry point ────────────────────────────────────────────

def discover_login_form(url):
    """
    Auto-detect login/register form on any page.
    Layer 1: plain requests (fast, works on 80% of sites)
    Layer 2: heuristic field scoring (handles unusual field names)
    Layer 3: Selenium for JS-rendered / SPA pages
    Returns a dict with 'action', 'method', 'fields', 'inputs'.
    """
    print(f"[FORM] Scanning: {url}")

    # Layer 1 + 2 — fast path
    result = _try_requests(url)

    # Layer 3 — Selenium fallback if no form found
    if not result:
        print("[FORM] No static form found — trying Selenium...")
        result = _try_selenium(url)

    if not result:
        print("[FORM] Could not detect any login form")
        return {"action": url, "method": "POST", "fields": {}, "inputs": []}

    print(f"[FORM] Action   : {result['action']}")
    print(f"[FORM] Method   : {result['method']}")
    print(f"[FORM] Username : {result['fields'].get('username', 'NOT FOUND')}")
    print(f"[FORM] Password : {result['fields'].get('password', 'NOT FOUND')}")
    print(f"[FORM] Hidden   : {[k for k in result['fields'] if k not in ('username','password','_submit')]}")

    return result


discover_login_form("https://www.facebook.com/login/")





