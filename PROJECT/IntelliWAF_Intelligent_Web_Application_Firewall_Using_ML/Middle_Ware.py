from mitmproxy import http
from datetime import datetime
import os
import hashlib
import urllib.parse
import math

OUTFILE = "Data_captures.txt"
MAX_BODY_CHARS = 200000

def OP_File():
    if not os.path.exists(OUTFILE):
        open(OUTFILE, "w", encoding="utf-8").close()

def Plain_String(x):
    if x is None:
        return "(none)"
    try:
        if hasattr(x, "items"):
            try:
                return ", ".join(f"{k}={v}" for k, v in x.items())
            except Exception:
                try:
                    return ", ".join(f"{k}={v}" for k, v in list(x))
                except Exception:
                    return str(x)
        if isinstance(x, (bytes, bytearray)):
            try:
                return x.decode("utf-8", errors="replace")
            except Exception:
                return f"[binary {len(x)} bytes]"
        return str(x)
    except Exception:
        return repr(x)

def format_headers(h):
    try:
        return "\n".join(f"{k}: {v}" for k, v in h.items())
    except Exception:
        return Plain_String(h)

def request(flow: http.HTTPFlow) -> None:
    OP_File()
    req = flow.request
    parts = ["---- CAPTURE START ----", "timestamp: " + datetime.utcnow().isoformat() + "Z"]

    try:
        client_addr = flow.client_conn.address
        client_ip = f"{client_addr[0]}:{client_addr[1]}" if client_addr else "(unknown)"
    except Exception:
        client_ip = "(unknown)"
    parts.append(f"client_ip: {client_ip}")
    parts.append(f"method: {Plain_String(req.method)}")
    parts.append(f"url: {Plain_String(req.pretty_url)}")
    parts.append(f"path: {Plain_String(req.path)}")
    parts.append("---- HEADERS ----")
    parts.append(format_headers(req.headers))
    parts.append("---- QUERY ----")
    parts.append(Plain_String(req.query))
    parts.append("---- BODY ----")
    if req.content:
        try:
            txt = req.get_text(strict=False)
            if len(txt) > MAX_BODY_CHARS:
                txt = txt[:MAX_BODY_CHARS] + "\n...(truncated)\n"
            parts.append(txt)
        except Exception:
            parts.append(Plain_String(req.content))
    else:
        parts.append("(empty)")

    parts.append("---- CACHE-RELATED HEADERS ----")
    for hname in ("Cache-Control", "Pragma", "Expires", "If-Modified-Since", "If-None-Match"):
        val = req.headers.get(hname)
        parts.append(f"{hname}: {Plain_String(val)}")
    parts.append("---- CAPTURE END ----\n\n")

    try:
        with open(OUTFILE, "a", encoding="utf-8") as f:
            f.write("\n".join(parts))
    except Exception as e:
        print("Failed to write capture:", e)

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest() if s else ""

def safe_text(b: bytes) -> str:
    try:
        t = b.decode("utf-8", errors="replace")
    except Exception:
        t = f"[binary {len(b)} bytes]"
    if len(t) > MAX_BODY_CHARS:
        return t[:MAX_BODY_CHARS] + "\n...(truncated)\n"
    return t

def shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    probs = [v / len(s) for v in counts.values()]
    return -sum(p * math.log2(p) for p in probs if p > 0)

def redact_form(body_text: str) -> str:
    if not body_text:
        return ""
    try:
        parsed = urllib.parse.parse_qs(body_text, keep_blank_values=True)
        for k in list(parsed.keys()):
            if "pass" in k.lower() or "pwd" in k.lower() or "token" in k.lower():
                parsed[k] = ["<REDACTED>"]
        return urllib.parse.urlencode(parsed, doseq=True)
    except Exception:
        return body_text

def count_files(content_type: str, body_bytes: bytes) -> int:
    if not content_type or not body_bytes:
        return 0
    return body_bytes.count(b'filename=') if "multipart/form-data" in content_type.lower() else 0

def response(flow: http.HTTPFlow) -> None:
    try:
        OP_File()
        req = flow.request
        resp = flow.response
        parts = ["---- RESPONSE ENRICHMENT START ----", "timestamp: " + datetime.utcnow().isoformat() + "Z"]

        try:
            client_addr = flow.client_conn.address
            client_ip = f"{client_addr[0]}:{client_addr[1]}" if client_addr else "(unknown)"
        except Exception:
            client_ip = "(unknown)"
        parts.append(f"client_ip: {client_ip}")
        parts.append(f"method: {Plain_String(req.method)}")
        parts.append(f"url: {Plain_String(req.pretty_url)}")

        # Response basics
        if resp:
            parts.append(f"response_status: {Plain_String(resp.status_code)}")
            resp_len = len(resp.raw_content) if getattr(resp, "raw_content", None) else len(resp.content or b"")
            parts.append(f"response_length: {resp_len}")
            parts.append("---- RESPONSE HEADERS ----")
            parts.append(format_headers(resp.headers))
        else:
            parts.append("response_status: (none)")

        # latency
        try:
            if getattr(resp, "timestamp_start", None) and getattr(req, "timestamp_start", None):
                parts.append(f"latency_ms: {int((resp.timestamp_start - req.timestamp_start) * 1000)}")
        except Exception:
            parts.append("latency_ms: (unknown)")

        # request body preview
        content_type = req.headers.get("Content-Type","")
        body_bytes = req.raw_content or b""
        body_preview = safe_text(body_bytes)
        if "application/x-www-form-urlencoded" in (content_type or "").lower():
            body_preview = redact_form(body_preview)
        parts.append("---- REQ BODY PREVIEW ----")
        parts.append(body_preview or "(empty)")

        # entropy and file count
        parts.append(f"request_body_entropy: {shannon_entropy(body_preview):.3f}")
        parts.append(f"response_body_entropy: {shannon_entropy(safe_text(resp.raw_content if resp else b'')):.3f}")
        parts.append(f"file_count: {count_files(content_type, body_bytes)}")

        # cookie hash / user-agent
        ua = req.headers.get("User-Agent","")
        parts.append(f"user_agent_family: {Plain_String(ua.split(' ')[0] if ua else '(none)')}")
        cookie = req.headers.get("Cookie","")
        parts.append(f"cookie_hash: {sha256_hex(cookie)}")
        parts.append(f"session_id_hash: {sha256_hex(cookie)}")

        # TLS / server info
        try:
            server_conn = getattr(flow, "server_conn", None)
            if server_conn:
                if getattr(server_conn, "ip_address", None):
                    parts.append(f"server_ip: {Plain_String(server_conn.ip_address)}")
                tls_ver = getattr(server_conn, "tls_version", None)
                if tls_ver:
                    parts.append(f"tls_version: {Plain_String(tls_ver)}")
        except Exception:
            pass

        # response preview
        if resp:
            try:
                resp_bytes = resp.raw_content or resp.content or b""
            except Exception:
                resp_bytes = b""
            parts.append("---- RESP BODY PREVIEW ----")
            parts.append(safe_text(resp_bytes) or "(empty)")

        parts.append("---- RESPONSE ENRICHMENT END ----\n\n")

        with open(OUTFILE, "a", encoding="utf-8") as f:
            f.write("\n".join(parts))

    except Exception as e:
        print("response() error:", e)
