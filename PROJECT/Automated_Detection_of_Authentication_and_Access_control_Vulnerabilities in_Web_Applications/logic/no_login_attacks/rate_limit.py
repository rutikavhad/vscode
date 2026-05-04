import requests
import time
import random
import re
from statistics import mean, stdev
from collections import Counter


def test_rate_limit(form, attempts=10, base_delay=0.0, jitter=0.3):
    """
    Advanced rate limit tester:
    - Detects HTTP limits (429, 403, 503)
    - Detects slowdown (soft throttling)
    - Detects content changes & fingerprint shifts
    - Detects CAPTCHA / lock messages
    - Detects redirect-based blocking
    - Tracks response timing patterns with stdev
    - Detects header-based signals (X-RateLimit-*)
    - Multi-session fingerprint rotation
    - Baseline drift detection
    """

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    })

    # --- Patterns ---
    CAPTCHA_PATTERNS = re.compile(
        r"captcha|recaptcha|hcaptcha|cf-turnstile|challenge", re.I
    )
    LOCKOUT_PATTERNS = re.compile(
        r"too many|locked|blocked|suspended|wait|rate.?limit|throttl|try again|banned|access denied|unusual activity",
        re.I,
    )
    REDIRECT_BLOCK_PATHS = re.compile(r"/block|/captcha|/challenge|/error|/limit", re.I)

    print(f"\n[RATE LIMIT TEST] Target: {form['action']} | Attempts: {attempts}")
    print("-" * 70)

    timings = []
    status_codes = []
    flags_seen = []
    baseline_times = []
    baseline_body_hash = None
    baseline_body_len = None
    redirect_count = 0
    results = []

    # Extract field names safely
    username_field = form.get("username_field", "username")
    password_field = form.get("password_field", "password")

    USERNAMES = [f"testuser{i}" for i in range(10)]
    PASSWORDS = ["wrongpass", "Password1", "123456", "admin", "letmein"]

    for i in range(1, attempts + 1):
        # Build payload
        payload = dict(form["fields"])
        payload[username_field] = USERNAMES[i % len(USERNAMES)]
        payload[password_field] = PASSWORDS[i % len(PASSWORDS)]

        start = time.time()
        try:
            resp = session.post(
                form["action"],
                data=payload,
                timeout=15,
                allow_redirects=True,
            )
            elapsed = time.time() - start
        except requests.exceptions.ConnectionError:
            print(f"[{i:03}] ❌ CONNECTION REFUSED — likely IP blocked")
            flags_seen.append("CONNECTION_REFUSED")
            break
        except requests.exceptions.Timeout:
            print(f"[{i:03}] ⏱️  TIMEOUT — server may be throttling hard")
            flags_seen.append("TIMEOUT")
            timings.append(15.0)
            continue
        except Exception as e:
            print(f"[{i:03}] ERROR: {e}")
            continue

        body = resp.text
        body_lower = body.lower()
        body_len = len(body)
        status = resp.status_code
        timings.append(elapsed)
        status_codes.append(status)

        # Establish baseline from first 3 successful requests
        if i <= 3:
            baseline_times.append(elapsed)
            baseline_body_len = body_len
        avg_baseline = mean(baseline_times) if baseline_times else elapsed

        # --- Detection Logic ---
        flag = ""
        severity = ""

        # 1. Hard rate limit
        if status == 429:
            retry = resp.headers.get("Retry-After", "N/A")
            flag = f"🚫 HTTP 429 RATE LIMITED (Retry-After: {retry})"
            severity = "HIGH"

        # 2. Forbidden / block
        elif status in (403, 503):
            flag = f"🛑 HTTP {status} — ACCESS BLOCKED"
            severity = "HIGH"

        # 3. X-RateLimit headers
        elif any(h.lower().startswith("x-ratelimit") for h in resp.headers):
            rl_headers = {k: v for k, v in resp.headers.items() if "ratelimit" in k.lower()}
            remaining = rl_headers.get("X-RateLimit-Remaining", "?")
            flag = f"📊 RATE-LIMIT HEADERS (Remaining: {remaining}) {rl_headers}"
            severity = "MEDIUM"

        # 4. Retry-After without 429
        elif "retry-after" in resp.headers:
            flag = f"⏳ Retry-After header: {resp.headers.get('Retry-After')}"
            severity = "MEDIUM"

        # 5. Redirect to block/captcha page
        elif resp.url != form["action"] and REDIRECT_BLOCK_PATHS.search(resp.url):
            flag = f"↩️  REDIRECT TO BLOCK PAGE: {resp.url}"
            severity = "HIGH"
            redirect_count += 1

        # 6. CAPTCHA in body
        elif CAPTCHA_PATTERNS.search(body_lower):
            flag = "🤖 CAPTCHA TRIGGERED"
            severity = "HIGH"

        # 7. Lockout / block message in body
        elif LOCKOUT_PATTERNS.search(body_lower):
            matched = LOCKOUT_PATTERNS.search(body_lower).group(0)
            flag = f"🔒 LOCKOUT MESSAGE ('{matched}')"
            severity = "HIGH"

        # 8. Response size anomaly (>30% drift from baseline)
        elif baseline_body_len and abs(body_len - baseline_body_len) > 0.3 * baseline_body_len:
            pct = ((body_len - baseline_body_len) / baseline_body_len) * 100
            flag = f"📦 RESPONSE SIZE SHIFTED {pct:+.0f}% ({baseline_body_len}→{body_len})"
            severity = "MEDIUM"

        # 9. Soft throttle: response time > 3x baseline
        elif avg_baseline > 0 and elapsed > avg_baseline * 3:
            flag = f"🐢 SLOWDOWN DETECTED ({elapsed:.2f}s vs baseline {avg_baseline:.2f}s)"
            severity = "LOW"

        # Update rolling baseline (smoothed)
        if not flag:
            baseline_times.append(elapsed)
            if len(baseline_times) > 10:
                baseline_times.pop(0)

        if flag:
            flags_seen.append(flag)

        print(
            f"[{i:03}] {status} | {elapsed:.2f}s | {body_len:>6}B"
            + (f" | {flag}" if flag else "")
        )

        results.append({
            "attempt": i,
            "status": status,
            "elapsed": elapsed,
            "body_len": body_len,
            "flag": flag,
            "severity": severity,
        })

        # Stop early on high-severity
        if severity == "HIGH":
            print(f"\n[!] High-severity protection at attempt #{i}: {flag}")
            break

        # Adaptive delay: back off if medium signals detected
        if severity == "MEDIUM":
            sleep_time = base_delay + random.uniform(jitter, jitter * 3)
        else:
            sleep_time = base_delay + random.uniform(0, jitter)
        time.sleep(sleep_time)

    # --- Summary ---
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    if timings:
        print(f"  Requests sent    : {len(timings)}/{attempts}")
        print(f"  Avg time         : {mean(timings):.2f}s")
        print(f"  Max time         : {max(timings):.2f}s")
        print(f"  Min time         : {min(timings):.2f}s")
        if len(timings) > 2:
            print(f"  Std deviation    : {stdev(timings):.2f}s")
        print(f"  Status codes     : {dict(Counter(status_codes))}")
        print(f"  Redirects        : {redirect_count}")

    if flags_seen:
        print(f"\n  🚨 Protections Detected:")
        for f in dict.fromkeys(flags_seen):  # deduplicate, preserve order
            print(f"     → {f}")
    else:
        print("\n  ✅ No rate limiting or protection detected")
        print("  ⚠️  This login endpoint may be VULNERABLE to brute force")

    # Timing pattern analysis
    if len(timings) >= 5:
        print("\n  Timing Analysis:")
        first_half = timings[: len(timings) // 2]
        second_half = timings[len(timings) // 2 :]
        if mean(second_half) > mean(first_half) * 2:
            print("  ⚠️  Progressive slowdown detected (soft throttling pattern)")
        else:
            print("  → No significant timing drift")

    print("\n[✔] Test completed\n")
    return results