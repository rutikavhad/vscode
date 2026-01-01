from mitmproxy import http
from datetime import datetime
import csv
import os
import math

import attacks

CSVFILE = "traffic_events.csv"


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
                "body_entropy",
                "special_char_count"
            ])


def shannon_entropy(s):
    if not s:
        return 0.0
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    return -sum(
        (v / len(s)) * math.log2(v / len(s))
        for v in freq.values()
    )


def request(flow: http.HTTPFlow):
    init_csv()
    req = flow.request

    # =========================
    # CLIENT IP + PORT (FIXED)
    # =========================
    client_ip = "unknown"
    try:
        addr = flow.client_conn.address
        if addr:
            client_ip = f"{addr[0]}:{addr[1]}"
    except:
        pass

    # =========================
    # BODY SAFE HANDLING
    # =========================
    try:
        body = req.get_text(strict=False) or ""
    except:
        body = ""

    body_len = len(body)
    entropy = round(shannon_entropy(body), 3) if body else 0.0

    # =========================
    # SPECIAL CHAR COUNT (FIXED → NEVER NaN)
    # =========================
    if body:
        special_char_count = sum(
            body.count(c)
            for c in ['<', '>', '"', "'", ';', '|', '&', '$', '/', '\\']
        )
    else:
        special_char_count = 0

    # =========================
    # ATTACK DETECTION
    # =========================
    attack_type = attacks.detect_attack_type(req, client_ip)

    # =========================
    # WRITE CSV (STRICT FORMAT)
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
            entropy,
            float(special_char_count)
        ])

    # =========================
    # BLOCK ATTACKS
    # =========================
    if attack_type != "NORMAL":
        status = 429 if attack_type == "DDOS" else 403
        flow.response = http.Response.make(
            status,
            f"Blocked\nDetected: {attack_type}".encode(),
            {"Content-Type": "text/plain"}
        )
