
from mitmproxy import http
from datetime import datetime
import os

OUTFILE = "captures.txt"
MAX_BODY_CHARS = 200000 

def ensure_file():
    if not os.path.exists(OUTFILE):
        open(OUTFILE, "w", encoding="utf-8").close()

def safe_str(x):
    """
    Convert many mitmproxy types to safe printable strings.
    - MultiDictView, Headers, etc -> joined key=value lines
    - None -> (none)
    - bytes -> attempt decode else show length
    """
    if x is None:
        return "(none)"
    try:
        # mitmproxy query or headers are mapping-like; try to iterate items
        if hasattr(x, "items"):
            try:
                return ", ".join(f"{k}={v}" for k, v in x.items())
            except Exception:
                # Some mitmproxy objects have .multi_items() or similar
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

def format_headers(h):
    # h is a mitmproxy Headers object; iterate items for stable ordering
    try:
        return "\n".join(f"{k}: {v}" for k, v in h.items())
    except Exception:
        # fallback
        return safe_str(h)

def request(flow: http.HTTPFlow) -> None:
    """
    Called for each client request. Writes a plain-text block per request.
    """
    ensure_file()
    req = flow.request

    parts = []
    parts.append("---- CAPTURE START ----")
    parts.append("timestamp: " + datetime.utcnow().isoformat() + "Z")

    # client ip: might be None in some environments
    try:
        client_addr = flow.client_conn.address
        client_ip = f"{client_addr[0]}:{client_addr[1]}" if client_addr else "(unknown)"
    except Exception:
        client_ip = "(unknown)"
    parts.append(f"client_ip: {client_ip}")

    parts.append(f"method: {safe_str(req.method)}")
    parts.append(f"url: {safe_str(req.pretty_url)}")
    parts.append(f"path: {safe_str(req.path)}")

    parts.append("---- HEADERS ----")
    parts.append(format_headers(req.headers))

    parts.append("---- QUERY ----")
    # req.query is often a MultiDictView -> convert safely
    parts.append(safe_str(req.query))

    parts.append("---- BODY ----")
    # req.content may be bytes; req.get_text() returns decoded text
    if req.content:
        # try to get text safely
        try:
            txt = req.get_text(strict=False)
            if len(txt) > MAX_BODY_CHARS:
                txt = txt[:MAX_BODY_CHARS] + "\n...(truncated)\n"
            parts.append(txt)
        except Exception:
            # fallback to safe_str for bytes
            parts.append(safe_str(req.content))
    else:
        parts.append("(empty)")

    # Cache-related headers convenience
    parts.append("---- CACHE-RELATED HEADERS ----")
    for hname in ("Cache-Control", "Pragma", "Expires", "If-Modified-Since", "If-None-Match"):
        val = req.headers.get(hname)
        parts.append(f"{hname}: {safe_str(val)}")

    parts.append("---- CAPTURE END ----\n\n")

    # join and write
    try:
        with open(OUTFILE, "a", encoding="utf-8") as f:
            f.write("\n".join(parts))
    except Exception as e:
        # don't let the addon crash; log to stdout/stderr
        print("Failed to write capture:", e)
