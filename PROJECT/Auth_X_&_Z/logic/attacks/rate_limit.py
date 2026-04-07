import requests
import time
import random
import re
from statistics import mean
#this just check how many requsts can send by 1 ip address 

def test_rate_limit(form, attempts=10, base_delay=0.0, jitter=0.3):
    """
    Advanced rate limit tester:
    - Detects HTTP limits (429)
    - Detects slowdown (soft throttling)
    - Detects content changes
    - Detects CAPTCHA / lock messages
    - Tracks response timing patterns
    """

    session = requests.Session()

    print(f"\n[RATE LIMIT TEST] Attempts: {attempts}")
    timings = []
    baseline_times = []
    baseline_body_len = None

    for i in range(1, attempts + 1):
        payload = {k: v for k, v in form["fields"].items()}
        payload[form["fields"].get("username", "username")] = f"testuser{i%5}"
        payload[form["fields"].get("password", "password")] = "wrongpass"

        # Measure response time
        start = time.time()
        try:
            resp = session.post(form["action"], data=payload, timeout=15)
            elapsed = time.time() - start
        except Exception as e:
            print(f"[{i:03}] ERROR: {e}")
            continue

        body = resp.text.lower()
        timings.append(elapsed)

        # Establish baseline (first few requests)
        if i <= 5:
            baseline_times.append(elapsed)
            baseline_body_len = len(body)
        
        avg_baseline = mean(baseline_times) if baseline_times else elapsed

        flag = ""

        # --- Detection logic ---

        # 1. Hard rate limit
        if resp.status_code == 429:
            flag = "🚫 HTTP 429 RATE LIMITED"

        # 2. Retry-After header
        elif "retry-after" in resp.headers:
            flag = f"⏳ Retry-After: {resp.headers.get('Retry-After')}"

        # 3. CAPTCHA detection
        elif re.search(r"captcha|recaptcha|hcaptcha", body):
            flag = "🤖 CAPTCHA TRIGGERED"

        # 4. Lockout / block message
        elif re.search(r"too many|locked|blocked|wait|limit|suspended", body):
            flag = "🔒 LOCKOUT MESSAGE"

        # 5. Response size anomaly
        elif baseline_body_len and abs(len(body) - baseline_body_len) > 0.3 * baseline_body_len:
            flag = "📦 RESPONSE SIZE CHANGED"

        # 6. Slowdown detection (soft throttling)
        elif avg_baseline > 0 and elapsed > avg_baseline * 3:
            flag = f"🐢 SLOWDOWN DETECTED ({elapsed:.2f}s vs {avg_baseline:.2f}s)"

        print(
            f"[{i:03}] Status: {resp.status_code} | "
            f"Time: {elapsed:.2f}s | Size: {len(body)} {flag}"
        )

        # Stop early if strong protection detected
        if flag:
            print(f"\n[!] Protection triggered at attempt {i}: {flag}")
            break

        # Jittered delay (more realistic traffic)
        sleep_time = base_delay + random.uniform(0, jitter)
        time.sleep(sleep_time)

    # --- Summary ---
    if timings:
        print("\n--- SUMMARY ---")
        print(f"Avg response time: {mean(timings):.2f}s")
        print(f"Max response time: {max(timings):.2f}s")
        print(f"Min response time: {min(timings):.2f}s")

        if len(timings) > 10:
            if max(timings) > mean(baseline_times) * 3:
                print("⚠️ Likely SOFT rate limiting detected (slowdown pattern)")
            else:
                print("⚠️ No strong throttling pattern detected")

    print("\n[✔] Test completed\n")