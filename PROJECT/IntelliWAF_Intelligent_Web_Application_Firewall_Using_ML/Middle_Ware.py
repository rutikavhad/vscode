from mitmproxy import http # this  MITMPROXY used to extract data using proxy server
from datetime import datetime # used to which time data collected
import os # for save  file 

OUTFILE = "Data_captures.txt"
MAX_BODY_CHARS = 200000  # prevents to captures large bodies data 

def OP_File(): #create file to store data in this file if file not exits
    if not os.path.exists(OUTFILE): 
        open(OUTFILE, "w", encoding="utf-8").close()

def Plain_String(x): # convert to human redable form as string
    if x is None:
        return "(none)"
    try:
        
        if hasattr(x, "items"):
            try:
                return ", ".join(f"{k}={v}" for k, v in x.items()) # used try & catch to avoid crash whiles writing file
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
                return f"[binary {len(x)} bytes]" #if can't convert into plain text then show binary values not errors
        return str(x)
    except Exception:
        return repr(x)

def format_headers(h):
    # h is a mitmproxy Headers object
    try:
        return "\n".join(f"{k}: {v}" for k, v in h.items())
    except Exception:
        return Plain_String(h)

def request(flow: http.HTTPFlow) -> None: # this used to get all info using mitmproxy 
    """
        Writes a plain-text block per request.
        In this function used mitmproxy prebuild methods to capthure requests
    """
    OP_File()
    req = flow.request
    parts = []
    parts.append("---- CAPTURE START ----")
    parts.append("timestamp: " + datetime.utcnow().isoformat() + "Z")

    # client ip
    try:
        client_addr = flow.client_conn.address
        client_ip = f"{client_addr[0]}:{client_addr[1]}" if client_addr else "(unknown)"
    except Exception:
        client_ip = "(unknown)"
    parts.append(f"client_ip: {client_ip}")
    #which method used
    parts.append(f"method: {Plain_String(req.method)}")
    #url in plain text
    parts.append(f"url: {Plain_String(req.pretty_url)}")
    #path of file  eg. /login
    parts.append(f"path: {Plain_String(req.path)}")
    #get headers data like user-agent, cookies, cache-control
    parts.append("---- HEADERS ----")
    parts.append(format_headers(req.headers))

    parts.append("---- QUERY ----")
    parts.append(Plain_String(req.query))
    #Get Data Like password and usernames also other info..
    parts.append("---- BODY ----")
    # req.content may be bytes; req.get_text() returns decoded text
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

    # Cache-related headers
    parts.append("---- CACHE-RELATED HEADERS ----")
    for hname in ("Cache-Control", "Pragma", "Expires", "If-Modified-Since", "If-None-Match"):
        val = req.headers.get(hname)
        parts.append(f"{hname}: {Plain_String(val)}")

    parts.append("---- CAPTURE END ----\n\n")

    # join and write
    try:
        with open(OUTFILE, "a", encoding="utf-8") as f:
            f.write("\n".join(parts))
    except Exception as e:
        print("Failed to write capture:", e)
