# parse_and_extract.py
import re
import csv
import math
from collections import Counter
from urllib.parse import urlparse, parse_qs, unquote_plus

CAP_START = "---- CAPTURE START ----"
CAP_END = "---- CAPTURE END ----"

SQLI_KEYWORDS = {"select","union","insert","update","delete","drop","sleep","benchmark","concat"}
XSS_PATTERNS = [r"<script", r"on\w+\s*=", r"javascript:"]

def shannon_entropy(s: str):
    if not s:
        return 0.0
    counts = Counter(s)
    probs = [c/len(s) for c in counts.values()]
    return -sum(p*math.log2(p) for p in probs)

def pct_non_alnum(s: str):
    return sum(1 for c in s if not c.isalnum()) / max(1, len(s))

def parse_capture_block(block: str):
    # Extract top-level fields using simple regexes
    get_field = lambda pattern: (re.search(pattern, block, re.MULTILINE) or re.search(pattern, block, re.IGNORECASE) or None)
    ts = (re.search(r"timestamp:\s*(.+)", block) or [None, ""])[1].strip()
    client_ip = (re.search(r"client_ip:\s*(.+)", block) or [None, ""])[1].strip()
    method = (re.search(r"method:\s*(.+)", block) or [None, ""])[1].strip()
    url = (re.search(r"url:\s*(.+)", block) or [None, ""])[1].strip()
    path = (re.search(r"path:\s*(.+)", block) or [None, ""])[1].strip()
    # headers: everything between ---- HEADERS ---- and next ----
    headers_match = re.search(r"---- HEADERS ----\n(.*?)\n----", block, re.DOTALL)
    headers = {}
    if headers_match:
        for line in headers_match.group(1).splitlines():
            if ":" in line:
                k,v = line.split(":",1)
                headers[k.strip()] = v.strip()
    # query and body sections
    query_match = re.search(r"---- QUERY ----\n(.*?)\n---- BODY ----", block, re.DOTALL)
    query = query_match.group(1).strip() if query_match else ""
    body_match = re.search(r"---- BODY ----\n(.*?)\n---- CACHE-RELATED HEADERS ----", block, re.DOTALL)
    body = body_match.group(1).strip() if body_match else ""
    # normalize body (if it's form-encoded)
    try:
        body_norm = unquote_plus(body)
    except Exception:
        body_norm = body

    return {
        "timestamp": ts,
        "client_ip": client_ip,
        "method": method,
        "url": url,
        "path": path,
        "headers": headers,
        "query": query,
        "body": body_norm,
    }

def extract_features_from_capture(c):
    u = urlparse(c["url"])
    path = u.path or "/"
    qs = u.query or c["query"] or ""
    body = c["body"] or ""
    headers = c["headers"]
    features = {}
    features["timestamp"] = c["timestamp"]
    features["client_ip"] = c["client_ip"]
    features["method"] = c["method"]
    features["url_len"] = len(c["url"])
    features["path_depth"] = path.count("/")
    features["query_len"] = len(qs)
    # parse parameters from body (form-encoded)
    params = parse_qs(qs) if qs else {}
    body_params = parse_qs(body) if body else {}
    features["num_query_params"] = len(params)
    features["num_body_params"] = len(body_params)
    features["body_len"] = len(body)
    features["body_entropy"] = round(shannon_entropy(body), 6)
    features["url_entropy"] = round(shannon_entropy(qs or path), 6)
    features["sql_keywords"] = int(any(k in (qs+body).lower() for k in SQLI_KEYWORDS))
    features["xss_indicators"] = int(any(re.search(p, (body+qs).lower()) for p in XSS_PATTERNS))
    features["pct_non_alnum_url"] = round(pct_non_alnum(c["url"]), 6)
    ua = headers.get("User-Agent","")
    features["ua_len"] = len(ua)
    features["has_referer"] = int("Referer" in headers or "Referrer" in headers)
    # simple cookie presence
    features["has_cookie"] = int("Cookie" in headers)
    # login-specific heuristics
    features["is_login_attempt"] = int(bool(body_params and ("username" in body_params or "user" in body_params or "password" in body_params)))
    # default credential patterns
    uname = body_params.get("username", [""])[0] if body_params else ""
    pwd = body_params.get("password", [""])[0] if body_params else ""
    features["username_len"] = len(uname)
    features["password_len"] = len(pwd)
    features["default_creds"] = int((uname.lower() in {"admin","user","root","test"}) and (pwd.lower() in {"password","admin","123456","root","test"}))
    # misc
    features["content_length_header"] = int(headers.get("Content-Length", "0") or 0)
    return features

def process_capture_file(input_path, output_csv="features.csv"):
    with open(input_path,"r",encoding="utf-8") as f:
        content = f.read()
    blocks = [b for b in content.split(CAP_START) if b.strip()]
    rows = []
    for b in blocks:
        try:
            c = parse_capture_block(b)
            feat = extract_features_from_capture(c)
            rows.append(feat)
        except Exception as e:
            print("parse error:", e)
    # write CSV with stable header order
    if not rows:
        print("no captures found")
        return
    fieldnames = list(rows[0].keys())
    with open(output_csv,"w",newline="",encoding="utf-8") as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print("Wrote", output_csv)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python parse_and_extract.py captures.txt")
    else:
        process_capture_file(sys.argv[1], output_csv="features.csv")
