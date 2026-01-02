from mitmproxy import http
from datetime import datetime
import csv
import os
import math
import time

import attacks   # your existing attacks.py (UNCHANGED)

# =========================
# CONFIG
# =========================
CSVFILE = "traffic_events.csv"

# =========================
# DDOS / RATE LIMIT CONFIG
# =========================
MAX_REQUESTS = 50      # requests
TIME_WINDOW = 60       # seconds (1 minute)
BLOCK_TIME = 120       # seconds (2 minutes)

request_log = {}       # ip -> [timestamps]
blocked_ips = {}       # ip -> unblock_time

# =========================
# CSV INIT
# =========================
def init_csv():
    if not os.path.exists(CSVFILE):
        with open(CSVFILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp",
                "client_ip",
                "method",
                "url",
                "path",
                "attack_type",
                "body_len",
                "body_entropy"
            ])

# =========================
# ENTROPY
# =========================
def shannon_entropy(s):
    if not s:
        return 0.0
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    probs = [v / len(s) for v in freq.values()]
    return -sum(p * math.log2(p) for p in probs if p > 0)

# =========================
# DDOS CHECK FUNCTION
# =========================
def check_ddos(client_ip):
    now = time.time()

    # Already blocked?
    if client_ip in blocked_ips:
        if now < blocked_ips[client_ip]:
            return True
        else:
            del blocked_ips[client_ip]  # unblock

    if client_ip not in request_log:
        request_log[client_ip] = []

    # Keep only recent requests
    request_log[client_ip] = [
        t for t in request_log[client_ip]
        if now - t <= TIME_WINDOW
    ]

    # Add current request
    request_log[client_ip].append(now)

    # Check limit
    if len(request_log[client_ip]) > MAX_REQUESTS:
        blocked_ips[client_ip] = now + BLOCK_TIME
        del request_log[client_ip]
        return True

    return False

# =========================
# MITMPROXY REQUEST
# =========================
def request(flow: http.HTTPFlow):
    init_csv()
    req = flow.request

    # =========================
    # CLIENT IP
    # =========================
    client_ip = "(unknown)"
    try:
        addr = flow.client_conn.address
        if addr:
            client_ip = addr[0]  # IP only
    except:
        pass

    # =========================
    # DDOS CHECK (FIRST)
    # =========================
    if check_ddos(client_ip):
        # =========================
        # WRITE DDOS EVENT TO CSV
        # =========================
        with open(CSVFILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.utcnow().isoformat() + "Z",
                client_ip,
                req.method,
                req.pretty_url,
                req.path,
                "DDOS",        # attack_type
                0,             # body_len
                0.0            # body_entropy
            ])

        # BLOCK REQUEST
        flow.response = http.Response.make(
            429,
            b"Too Many Requests - DDoS Protection Active",
            {"Content-Type": "text/plain"}
        )
        return

    # =========================
    # BODY
    # =========================
    try:
        body = req.get_text(strict=False) or ""
    except:
        body = ""

    body_len = len(body)
    entropy = round(shannon_entropy(body), 3)

    # =========================
    # ATTACK DETECTION
    # =========================
    file_result = attacks.check_file_upload(req)

    if file_result == "FILE_UPLOAD_ABUSE":
        attack_type = "FILE_UPLOAD_ABUSE"

    elif file_result == "NORMAL":
        attack_type = "NORMAL"

    else:
        found = attacks.check_other_attacks(req)
        attack_type = "|".join(found) if found else "NORMAL"

    # =========================
    # WRITE CSV (ALWAYS)
    # =========================
    with open(CSVFILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.utcnow().isoformat() + "Z",
            client_ip,
            req.method,
            req.pretty_url,
            req.path,
            attack_type,
            body_len,
            entropy
        ])

    # =========================
    # BLOCK IF ATTACK
    # =========================
    if attack_type != "NORMAL":
        flow.response = http.Response.make(
            403,
            f"Blocked by Web Protector\nDetected: {attack_type}".encode(),
            {"Content-Type": "text/plain"}
        )
