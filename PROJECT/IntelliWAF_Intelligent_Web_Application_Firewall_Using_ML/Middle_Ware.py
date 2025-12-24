from mitmproxy import http
from datetime import datetime
import os
import math
import csv

OUTFILE = "Data_captures.txt"
CSVFILE = "captures_combined.csv"
MAX_BODY_CHARS = 200000 # turuncate vary large bodies for saftey


def OP_File():
    if not os.path.exists(OUTFILE):
        open(OUTFILE, "w", encoding="utf-8").close()

    if not os.path.exists(CSVFILE):
        with open(CSVFILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp",
                "client_ip",
                "method",
                "url",
                "path",
                "body",
                "body_len",
                "body_entropy",
                "special_char_count",
                "path_depth",
                "query_length",
                "has_file_upload",
                "response_status",
                "response_length"
            ])

def Plain_String(x):
    if x is None:
        return "(none)"
    try:
         # mapping-like: headers, query etc
        if hasattr(x, "items"):
            try:
                return ", ".join(f"{k}={v}" for k, v in x.items())
            except Exception:
                try:
                    return ", ".join(f"{k}={v}" for k, v in list(x))
                except Exception:
                    return str(x)
        # bytes -> try decode
        if isinstance(x, (bytes, bytearray)):
            try:
                return x.decode("utf-8", errors="replace")
            except Exception:
                return f"[binary {len(x)} bytes]"
        return str(x)
    except Exception:
        return repr(x)

#Return headers as multi-line string 'Name: value'
def format_headers(h):
    try:
        return "\n".join(f"{k}: {v}" for k, v in h.items())
    except Exception:
        return Plain_String(h)


def shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    probs = [v / len(s) for v in counts.values()]
    return -sum(p * math.log2(p) for p in probs if p > 0)


def request(flow: http.HTTPFlow) -> None:
    OP_File()
    req = flow.request

    timestamp = datetime.utcnow().isoformat() + "Z"
    parts = ["---- CAPTURE START ----", f"timestamp: {timestamp}"]
    
    try:
        client_addr = flow.client_conn.address
        client_ip = f"{client_addr[0]}:{client_addr[1]}" if client_addr else "(unknown)"
    except Exception:
        client_ip = "(unknown)"
    # client ip (may be unknown in some environments)
    parts.append(f"client_ip: {client_ip}")
    parts.append(f"method: {Plain_String(req.method)}") # which methods are use (GET,POST,etc.)
    parts.append(f"url: {Plain_String(req.pretty_url)}") #main URL
    parts.append(f"path: {Plain_String(req.path)}") #path of web page
    parts.append("---- HEADERS ----") 
    parts.append(format_headers(req.headers)) #headers
    parts.append("---- QUERY ----")
    parts.append(Plain_String(req.query)) #Query Params
    parts.append("---- BODY ----")
    # body (text where possible, or binary indicator)
    try:
        txt = req.get_text(strict=False)
        if len(txt) > MAX_BODY_CHARS:
            txt = txt[:MAX_BODY_CHARS] + "\n...(truncated)\n"
        body_text = txt
        parts.append(txt)
    except Exception:
        body_text = Plain_String(req.content)
        parts.append(body_text)

    parts.append("---- CAPTURE END ----\n\n")

    try:
        with open(OUTFILE, "a", encoding="utf-8") as f:
            f.write("\n".join(parts))
    except Exception as e:
        print("Failed to write capture:", e)


def response(flow: http.HTTPFlow) -> None:
    try:
        OP_File()
        req = flow.request
        resp = flow.response

        timestamp = datetime.utcnow().isoformat() + "Z"
        parts = ["---- RESPONSE ENRICHMENT START ----", f"timestamp: {timestamp}"]

        try:
            client_addr = flow.client_conn.address
            client_ip = f"{client_addr[0]}:{client_addr[1]}" if client_addr else "(unknown)"
        except Exception:
            client_ip = "(unknown)"

        parts.append(f"client_ip: {client_ip}")
        parts.append(f"method: {Plain_String(req.method)}")
        parts.append(f"url: {Plain_String(req.pretty_url)}")

        if resp:
            parts.append(f"response_status: {Plain_String(resp.status_code)}")
            resp_len = len(resp.raw_content) if getattr(resp, "raw_content", None) else len(resp.content or b"")
            parts.append(f"response_length: {resp_len}")
        else:
            resp_len = 0
            parts.append("response_status: (none)")

        parts.append("---- RESPONSE ENRICHMENT END ----\n\n")

        with open(OUTFILE, "a", encoding="utf-8") as f:
            f.write("\n".join(parts))

        # ML FEATURE EXTRACTION
        #MAKE CSV FILE TO ML MODEL CAN READ THE DATA
        try:
            body_text = req.get_text(strict=False) or ""
        except:
            body_text = ""

        body_len = len(body_text)
        entropy = shannon_entropy(body_text)
        special_count = sum(body_text.count(c) for c in ['<', '>', '"', "'", ';', '|', '&', '$', '/', '\\'])
        path_depth = req.path.count('/')
        query_length = len(req.query or "")
        has_file_upload = 1 if "multipart/form-data" in req.headers.get("Content-Type","").lower() else 0
        status = resp.status_code if resp else ""

        with open(CSVFILE, "a", newline="", encoding="utf-8") as f: #Write data in csv file
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                str(flow.client_conn.address),
                req.method,
                req.pretty_url,
                req.path,
                body_text.replace("\n", "\\n"),
                body_len,
                round(entropy, 3),
                special_count,
                path_depth,
                query_length,
                has_file_upload,
                status,
                resp_len
            ])

    except Exception as e:
        print("response() error:", e)
