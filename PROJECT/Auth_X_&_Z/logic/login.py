'''
THIS TEST ALL LOGIN AREAS 
LIMIT RATE
CHECK SESSION
CHECK CSRF TOKEN
'''

import requests
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver

import io
from contextlib import redirect_stdout

#findings=[]

def discover_login_form(url):
    """Find input fields (username, password, hidden) and form action."""
    resp = requests.get(url, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")

    result = {"action": url, "method": "POST", "fields": {}, "inputs": []}

    for form in soup.find_all("form"):
        if not form.find("input", {"type": "password"}):
            continue

        result["action"] = form.get("action", url)
        result["method"] = form.get("method", "POST").upper()

        for inp in form.find_all("input"):
            t = inp.get("type", "text").lower()
            n = inp.get("name", "")
            v = inp.get("value", "")

            result["inputs"].append({"type": t, "name": n, "value": v})

            if t == "password":
                result["fields"]["password"] = n
            elif t in ("text", "email"):
                result["fields"]["username"] = n
            elif t == "hidden":
                result["fields"][n] = v  # includes CSRF tokens

        break  # stop at first password form

    print(f"[FORM] Action : {result['action']}")
    print(f"[FORM] Method : {result['method']}")
    print(f"[FORM] Fields : {result['fields']}")
    return result


def test_rate_limit(form, attempts=20, delay=0.2):
    """Send repeated bad-login requests and check for rate limiting."""
    session = requests.Session()
    print(f"\n[RATE LIMIT] Sending {attempts} attempts...")

    for i in range(1, attempts + 1):
        payload = {k: v for k, v in form["fields"].items()}
        payload[form["fields"].get("username", "username")] = "testuser"
        payload[form["fields"].get("password", "password")] = "wrongpass"

        resp = session.post(form["action"], data=payload, timeout=10)
        body = resp.text.lower()

        flag = ""
        if resp.status_code == 429:
            flag = "HTTP 429 - RATE LIMITED"
        elif re.search(r"too many|locked|blocked|wait|limit", body):
            flag = "LOCKOUT MESSAGE"
        elif re.search(r"captcha|recaptcha|hcaptcha", body):
            flag = "CAPTCHA APPEARED"

        print(f"  [{i:02}] Status: {resp.status_code} | Length: {len(body)} {flag}")

        if flag:
            print(f"[!] Protection detected at attempt {i}: {flag}")
            return

        time.sleep(delay)

    print("[!] WARNING: No rate limiting detected!")


def check_session(url):
    """Check session cookie flags (HttpOnly, Secure, SameSite)."""
    resp = requests.get(url, timeout=10)
    print("\n[SESSION] Cookies:")

    for cookie in resp.cookies:
        flags = []
        raw = resp.headers.get("Set-Cookie", "")
        if "httponly" not in raw.lower(): flags.append("MISSING HttpOnly")
        if "secure"   not in raw.lower(): flags.append("MISSING Secure")
        if "samesite" not in raw.lower(): flags.append("MISSING SameSite")
        print(f"  {cookie.name} => {', '.join(flags) if flags else 'OK'}")


def check_csrf(url):
    """Check if a CSRF token exists and changes per load."""
    def get_token(u):
        soup = BeautifulSoup(requests.get(u, timeout=10).text, "html.parser")
        for inp in soup.find_all("input", {"type": "hidden"}):
            if re.search(r"csrf|token|nonce", inp.get("name", ""), re.I):
                return inp.get("name"), inp.get("value")
        return None, None

    field, t1 = get_token(url)
    _,     t2 = get_token(url)

    print("\n[CSRF]")
    if not t1:
        print("  [!] No CSRF token found — HIGH RISK")
    elif t1 != t2:
        print(f"  Token field: {field} | Changes per load: YES (good)")
    else:
        print(f"  Token field: {field} | Changes per load: NO (weak)")


def check_csrf_full(url):
    print("\n[CSRF TEST]")
    session = requests.Session()
    def extract_token(response):
        soup = BeautifulSoup(response.text, "html.parser")
        for inp in soup.find_all("input", {"type": "hidden"}):
            name = inp.get("name", "")
            value = inp.get("value", "")
            if re.search(r"csrf|token|nonce", name, re.I):
                return name, value
        return None, None

    try:
        # Step 1: Get page twice (same session)
        r1 = session.get(url, timeout=10)
        field1, token1 = extract_token(r1)

        r2 = session.get(url, timeout=10)
        field2, token2 = extract_token(r2)

        # Step 2: Token presence
        if not token1:
            print("  [!] No CSRF token found — HIGH RISK")
            return

        print(f"  [+] Token found: {field1}")

        # Step 3: Token behavior
        if token1 != token2:
            print("  [+] Token rotates per request")
        else:
            print("  [*] Token stable (may be session-based)")

        # Step 4: Cookie check (basic)
        if "csrf" in str(session.cookies).lower():
            print("  [+] CSRF token also present in cookies")

        # Step 5: Validation test (IMPORTANT)
        test_data_valid = {
            "username": "test",
            "password": "test",
            field1: token1
        }

        test_data_invalid = {
            "username": "test",
            "password": "test",
            field1: "invalid_token_123"
        }

        # NOTE: This assumes POST endpoint = same URL (works for labs, not always real apps)
        r_valid = session.post(url, data=test_data_valid)
        r_invalid = session.post(url, data=test_data_invalid)

        if r_valid.status_code == r_invalid.status_code:
            print("  [!] Server accepts invalid CSRF token — VULNERABLE")
        else:
            print("  [+] CSRF validation seems enforced")

    except Exception as e:
        print(f"  [ERROR] {e}")



#CAPTCHA Misconfiguration Scanner
def check_captchas(url):
    driver = webdriver.Chrome()
    driver.get(url)
    page = driver.page_source.lower()
    print("\n[CAPTCHA]")
    if "recaptcha" in page or "hcaptcha" in page:
        print("CAPTCHA detected")
    else:
        print("No CAPTCHA detected")
    driver.quit()

    #try bypass it 
    session = requests.Session()
    data = {
        "username": "test",
        "password": "test",
        # intentionally omit captcha
    }

    login_url = url  

    res2 = session.post(login_url, data=data)

    if res2.status_code == 200:
        print("[!] Possible CAPTCHA bypass (no validation)")
    else:
        print("[+] CAPTCHA seems enforced")


def scan(url):
    """Main entry point — pass URL from your other program."""
    buffer=io.StringIO()
    with redirect_stdout(buffer):
        print(f"\n{'='*50}\n  Scanning: {url}\n{'='*50}")
        form = discover_login_form(url)
        test_rate_limit(form)
        check_session(url)
        check_csrf_full(url)
        check_captchas(url)
        print("\n[DONE]")

    print_out=buffer.getvalue()
    return print_out


# --- Run directly ---
if __name__ == "__main__":
    import sys
    scan(sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:3000/#/login")