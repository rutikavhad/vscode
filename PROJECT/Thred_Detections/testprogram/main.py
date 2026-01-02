from mitmproxy import http
from datetime import datetime
import csv, os, math, time
import attacks  # Your attacks.py

CSVFILE = "traffic_events.csv"
STATUS_FILE = "firewall_status.txt"

# --- HELPER FUNCTIONS ---
def init_csv():
    if not os.path.exists(CSVFILE):
        with open(CSVFILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "client_ip", "method", "url", "path", "attack_type", "body_len", "body_entropy"])

def get_block_html(attack_type, client_ip):
    try:
        with open("block_page.html", "r") as f:
            content = f.read()
        return content.replace("{{ATTACK_TYPE}}", attack_type).replace("{{CLIENT_IP}}", client_ip)
    except:
        return f"Blocked: {attack_type}"

def is_enabled():
    if not os.path.exists(STATUS_FILE): return True
    with open(STATUS_FILE, "r") as f: return f.read().strip() == "ON"

def shannon_entropy(s):
    if not s: return 0.0
    freq = {c: s.count(c) for c in set(s)}
    probs = [v / len(s) for v in freq.values()]
    return -sum(p * math.log2(p) for p in probs if p > 0)

# --- DDOS LOGIC ---
request_log, blocked_ips = {}, {}
def check_ddos(ip):
    now = time.time()
    if ip in blocked_ips:
        if now < blocked_ips[ip]: return True
        else: del blocked_ips[ip]
    request_log.setdefault(ip, [])
    request_log[ip] = [t for t in request_log[ip] if now - t <= 60]
    request_log[ip].append(now)
    if len(request_log[ip]) > 50:
        blocked_ips[ip] = now + 120
        return True
    return False

# --- MAIN PROXY HOOK ---
def request(flow: http.HTTPFlow):
    init_csv()
    
    # 1. Check if Firewall is ON
    if not is_enabled():
        return

    req = flow.request
    client_ip = flow.client_conn.address[0] if flow.client_conn.address else "0.0.0.0"

    # 2. DDoS Detection
    if check_ddos(client_ip):
        log_event(client_ip, req, "DDOS", 0, 0.0)
        flow.response = http.Response.make(429, get_block_html("DDoS / Rate Limit", client_ip).encode(), {"Content-Type": "text/html"})
        return

    # 3. Attack Detection
    body = req.get_text(strict=False) or ""
    file_result = attacks.check_file_upload(req)
    
    if file_result:
        attack_type = file_result
    else:
        found = attacks.check_other_attacks(req)
        attack_type = "|".join(found) if found else "NORMAL"

    log_event(client_ip, req, attack_type, len(body), round(shannon_entropy(body), 3))

    # 4. Block Response
    if attack_type != "NORMAL":
        flow.response = http.Response.make(403, get_block_html(attack_type, client_ip).encode(), {"Content-Type": "text/html"})

def log_event(ip, req, attack, b_len, entropy):
    with open(CSVFILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([datetime.utcnow().isoformat(), ip, req.method, req.pretty_url, req.path, attack, b_len, entropy])