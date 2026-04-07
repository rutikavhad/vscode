"""
THIS TESTS ALL LOGIN AREAS
LIMIT RATE
CHECK SESSION
CHECK CSRF TOKEN
CHECK CAPTCHA
"""

import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from  List.payload_list import PAYLOADS
from attacks.rate_limit import test_rate_limit
from attacks.sql_injection import run_sqli_scan

def discover_login_form(url, wait_time=3):
    """Discover login forms with username/email/id and password inputs, including hidden fields.
       Handles static and modern JS-based websites (React/Angular/Vue)."""

    # Setup headless browser
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # Wait for JS to load (basic)
    time.sleep(wait_time)

    result = {"action": url, "method": "POST", "fields": {}, "inputs": []}

    # Patterns to detect username/email/ID fields
    username_patterns = re.compile(r"user(name)?|login|email|id", re.I)
    password_patterns = re.compile(r"pass(word)?|pwd", re.I)

    # Find all forms
    forms = driver.find_elements(By.TAG_NAME, "form")
    best_form = None
    best_score = -1

    # Score forms to choose the most likely login form
    for form in forms:
        score = 0
        inputs = form.find_elements(By.TAG_NAME, "input")
        has_password = any(inp.get_attribute("type") == "password" for inp in inputs)
        if not has_password:
            continue
        score += 5  # password field is important
        if any(username_patterns.search(inp.get_attribute("name") or "") or
               username_patterns.search(inp.get_attribute("placeholder") or "")
               for inp in inputs):
            score += 3
        if "login" in (form.get_attribute("action") or "").lower():
            score += 2
        if score > best_score:
            best_score = score
            best_form = form

    if best_form:
        result["action"] = best_form.get_attribute("action") or url
        result["method"] = (best_form.get_attribute("method") or "POST").upper()

        inputs = best_form.find_elements(By.TAG_NAME, "input")
        for inp in inputs:
            t = (inp.get_attribute("type") or "text").lower()
            n = inp.get_attribute("name") or inp.get_attribute("id") or ""
            v = inp.get_attribute("value") or ""

            result["inputs"].append({"type": t, "name": n, "value": v})

            # Detect username/email/ID
            label_text = " ".join(filter(None, [
                inp.get_attribute("name"),
                inp.get_attribute("id"),
                inp.get_attribute("placeholder"),
                inp.get_attribute("aria-label")
            ])).lower()
            if t in ("text", "email") or t == "":
                if username_patterns.search(n) or username_patterns.search(label_text):
                    result["fields"]["username"] = n
            # Detect password
            if t == "password":
                result["fields"]["password"] = n
            # Hidden fields (CSRF tokens etc.)
            if t == "hidden" and n:
                result["fields"][n] = v

    driver.quit()

    # Print in same format
    print(f"[FORM] Action : {result['action']}")
    print(f"[FORM] Method : {result['method']}")
    print(f"[FORM] Fields : {result['fields']}")
    return result

#rate limit in new file

def check_session(url):
    resp = requests.get(url, timeout=10)

    print("\n[SESSION] Cookies:")

    # Get ALL Set-Cookie headers
    cookies = resp.raw.headers.get_all('Set-Cookie')

    if not cookies:
        print("  No cookies found")
        return

    for cookie in cookies:
        flags = []

        c_lower = cookie.lower()

        if "httponly" not in c_lower:
            flags.append("MISSING HttpOnly")
        if "secure" not in c_lower:
            flags.append("MISSING Secure")
        if "samesite" not in c_lower:
            flags.append("MISSING SameSite")

        name = cookie.split("=")[0]

        print(f"  {name} => {', '.join(flags) if flags else 'OK'}")

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
            print("  [!] No CSRF token found — I THING I CAN'T FIND IT")
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

        r_valid = session.post(url, data=test_data_valid)
        r_invalid = session.post(url, data=test_data_invalid)

        if r_valid.status_code == r_invalid.status_code:
            print("  [!] Server accepts invalid CSRF token — VULNERABLE")
        else:
            print("  [+] CSRF validation seems enforced")

    except Exception as e:
        print(f"  [ERROR] {e}")


def check_captchas(url):
    driver = webdriver.Chrome()
    driver.get(url)
    page = driver.page_source
    page_lower = page.lower()

    print("\n[CAPTCHA]")

    soup = BeautifulSoup(page, "html.parser")

    detected = False

    # --- Strong detection logic ---
    if (
        "recaptcha" in page_lower or
        "grecaptcha" in page_lower or
        "google.com/recaptcha" in page_lower or
        soup.find(class_="g-recaptcha")
    ):
        print("reCAPTCHA detected")
        detected = True

    if (
        "hcaptcha" in page_lower or
        "hcaptcha.com" in page_lower or
        soup.find(class_="h-captcha")
    ):
        print("hCaptcha detected")
        detected = True

    if (
        "cf-turnstile" in page_lower or
        "challenges.cloudflare.com" in page_lower or
        soup.find(class_="cf-turnstile")
    ):
        print("Cloudflare Turnstile detected")
        detected = True

    # Image CAPTCHA
    for img in soup.find_all("img"):
        src = img.get("src", "").lower()
        if "captcha" in src:
            print("Image CAPTCHA detected")
            detected = True
            break

    # Text CAPTCHA
    if re.search(r"(solve|human|verify|captcha)", page_lower):
        print("Text/Question CAPTCHA detected")
        detected = True

    if not detected:
        print("No CAPTCHA detected")

    driver.quit()

    # --- Try bypass (your original logic, slightly stronger) ---
    session = requests.Session()

    data = {
        "username": "test",
        "password": "test",
        # still omitting captcha intentionally
    }

    login_url = url

    res2 = session.post(login_url, data=data)

    # Improved validation check
    if res2.status_code == 200 and not re.search(r"(captcha|verify|blocked)", res2.text.lower()):
        print("[!] Possible CAPTCHA bypass (no validation)")
    else:
        print("[+] CAPTCHA seems enforced")
def scan(url):
    """Main entry point — prints everything directly to terminal."""
    print(f"\n{'='*50}\n  Scanning: {url}\n{'='*50}")
    form = discover_login_form(url)
    print(form)
    test_rate_limit(form)
    check_session(url)
    check_csrf_full(url)
    check_captchas(url)
    results = run_sqli_scan(
        form, 
        payloads=PAYLOADS,
        threads=10
    )
    print(results)
    print("\n[DONE]")


# --- Run directly ---
if __name__ == "__main__":
    import sys
    # url = sys.argv[1] if len(sys.argv) > 1 else "https://campusmoodle.unipune.ac.in/my/courses.php"
    url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8080/vulnerabilities/sqli/"
    scan(url)