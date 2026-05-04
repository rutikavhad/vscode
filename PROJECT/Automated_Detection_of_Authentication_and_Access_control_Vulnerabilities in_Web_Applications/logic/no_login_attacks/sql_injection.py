import requests, re
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import product as iproduct

# ----------------------------
# CONFIG
# ----------------------------


THREADS = 20
DIFF_THRESHOLD = 50
TIME_THRESHOLD = 1.8  # seconds for time-based detection


# ----------------------------
# REQUEST
# ----------------------------
def send(url, data, method="POST", headers=None):
    h = {"User-Agent": "Mozilla/5.0", **(headers or {})}
    try:
        import time
        t = time.time()
        r = requests.request(method, url, data=data, headers=h,
                             timeout=10, allow_redirects=True)
        elapsed = time.time() - t
        return r.status_code, len(r.text), r.text, elapsed
    except Exception as e:
        return None, 0, "", 0


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
    s, l, t, _ = send(form["action"], d)
    print(f"[BASE] Status: {s} | Length: {l}")
    # Capture error patterns for error-based detection
    err_patterns = _extract_errors(t)
    return s, l, err_patterns


def _extract_errors(text):
    patterns = [
        r"sql syntax", r"mysql_fetch", r"ORA-\d+", r"syntax error",
        r"unclosed quotation", r"sqlite3\.", r"pg_query", r"odbc_exec",
        r"microsoft.*database.*error", r"warning.*mysql",
    ]
    found = set()
    for p in patterns:
        if re.search(p, text, re.I):
            found.add(p)
    return found


# ----------------------------
# TEST PAYLOAD
# ----------------------------
def test_payload(payload, form, base_len, base_errors):
    findings = []

    for field_role in ("username", "password"):
        user = payload if field_role == "username" else "admin"
        pwd  = payload if field_role == "password"  else "test123"

        d = build_data(form, user, pwd)
        s, l, body, elapsed = send(form["action"], d)
        diff = l - base_len
        errors = _extract_errors(body)
        new_errors = errors - base_errors

        # Detection heuristics
        time_based  = elapsed >= TIME_THRESHOLD
        error_based = bool(new_errors)
        bool_based  = s == 200 and abs(diff) > DIFF_THRESHOLD
        union_based = bool(re.search(r"(admin|root|user|email)", body, re.I) and diff > 0)

        tag = []
        if time_based:  tag.append("TIME-BASED")
        if error_based: tag.append(f"ERROR-BASED:{new_errors}")
        if bool_based:  tag.append("BOOLEAN")
        if union_based: tag.append("UNION")

        label = "|".join(tag) if tag else None
        icon  = "[!!!]" if label else "[   ]"

        print(f"{icon}[{field_role[:4].upper()}] {payload[:40]:<40} "
              f"S={s} L={l:>6} Δ={diff:>+6} T={elapsed:.2f}s"
              + (f" >> {label}" if label else ""))

        if label:
            findings.append({
                "field": field_role, "payload": payload,
                "type": label, "size": l, "diff": diff, "time": elapsed
            })

    return findings


# ----------------------------
# MAIN
# ----------------------------
def run_sqli_scan(form, payloads, threads=THREADS):
    base_status, base_len, base_errors = get_baseline(form)

    if base_status != 200:
        print(f"[!] Baseline status {base_status} — aborting.")
        return []

    print(f"\n[*] STARTING {len(payloads)} PAYLOADS × 2 FIELDS "
          f"= {len(payloads)*2} TESTS ({threads} threads)\n")
    print(f"{'TYPE':<6} {'FIELD':<5} {'PAYLOAD':<42} {'S':>4} {'LEN':>7} "
          f"{'DIFF':>7} {'TIME':>6}")
    print("-" * 80)

    findings = []
    with ThreadPoolExecutor(max_workers=threads) as ex:
        futures = {ex.submit(test_payload, p, form, base_len, base_errors): p
                   for p in payloads}
        for future in as_completed(futures):
            res = future.result()
            if res:
                findings.extend(res)

    # Summary
    print("\n" + "=" * 80)
    print(f"[+] SCAN COMPLETE — {len(findings)} finding(s)\n")
    for f in findings:
        print(f"  [{f['type']}] field={f['field']} | payload={f['payload']}")
    print("=" * 80)

    return findings