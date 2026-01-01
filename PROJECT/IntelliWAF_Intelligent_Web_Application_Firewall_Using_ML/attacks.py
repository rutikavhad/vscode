import re
import time
from urllib.parse import unquote_plus

# =========================
# DDOS CONFIG
# =========================
MAX_REQUESTS = 50
TIME_WINDOW = 60
BLOCK_TIME = 120

request_log = {}
blocked_ips = {}


# =========================
# DDOS CHECK
# =========================
def check_ddos(client_ip):
    now = time.time()

    if client_ip in blocked_ips:
        if now < blocked_ips[client_ip]:
            return True
        else:
            del blocked_ips[client_ip]

    if client_ip not in request_log:
        request_log[client_ip] = []

    request_log[client_ip] = [
        t for t in request_log[client_ip]
        if now - t <= TIME_WINDOW
    ]

    request_log[client_ip].append(now)

    if len(request_log[client_ip]) > MAX_REQUESTS:
        blocked_ips[client_ip] = now + BLOCK_TIME
        del request_log[client_ip]
        return True

    return False


# =========================
# NORMALIZATION
# =========================
def normalize(text):
    if not text:
        return ""
    for _ in range(3):
        text = unquote_plus(text)
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# =========================
# SIGNATURES
# =========================
SQLI_SIGNS = [" or 1=1", "union select", "sleep(", "benchmark(", "--"]
CMD_SIGNS  = [";", "&&", "||", "|", "`", "$("]
PATH_SIGNS = ["../", "..\\", "php://", "file://", "data://", "/etc/passwd"]
XSS_SIGNS  = ["<script", "</script>", "javascript:", "onerror=", "onload="]

ALLOWED_UPLOAD_EXT = [".png", ".jpg", ".jpeg", ".gif", ".pdf", ".txt", "text"]
BLOCKED_UPLOAD_EXT = [
    ".php", ".py", ".exe", ".jsp", ".sh",
    "js", ".bash", ".c", ".asm", ".java", ".class"
]


# =========================
# FILE UPLOAD CHECK
# =========================
def check_file_upload(req):
    ct = req.headers.get("Content-Type", "").lower()
    if "multipart/form-data" not in ct:
        return None

    try:
        body = req.get_text(strict=False) or ""
    except:
        return "FILE_UPLOAD_ABUSE"

    files = re.findall(r'filename="([^"]+)"', body, re.IGNORECASE)

    for fname in files:
        fname = fname.lower()

        for ext in BLOCKED_UPLOAD_EXT:
            if fname.endswith(ext):
                return "FILE_UPLOAD_ABUSE"

        if fname.count(".") >= 2:
            return "FILE_UPLOAD_ABUSE"

        for ext in ALLOWED_UPLOAD_EXT:
            if fname.endswith(ext):
                return "NORMAL"

        return "FILE_UPLOAD_ABUSE"

    return "NORMAL"


# =========================
# OTHER ATTACKS
# =========================
def check_other_attacks(req):
    found = []
    inputs = []

    for v in req.query.values():
        inputs.append(v)

    try:
        body = req.get_text(strict=False) or ""
        inputs.append(body)
    except:
        pass

    norm_inputs = [normalize(i) for i in inputs]

    if any(any(s in d for s in SQLI_SIGNS) for d in norm_inputs):
        found.append("SQL_INJECTION")

    if any(any(s in d for s in CMD_SIGNS) for d in norm_inputs):
        found.append("COMMAND_INJECTION")

    if any(any(s in d for s in PATH_SIGNS) for d in norm_inputs):
        found.append("PATH_TRAVERSAL")

    if any(any(s in d for s in XSS_SIGNS) for d in norm_inputs):
        found.append("XSS")

    return found


# =========================
# FINAL DETECTOR
# =========================
def detect_attack_type(req, client_ip):
    if check_ddos(client_ip):
        return "DDOS"

    file_result = check_file_upload(req)
    if file_result == "FILE_UPLOAD_ABUSE":
        return "FILE_UPLOAD_ABUSE"
    if file_result == "NORMAL":
        return "NORMAL"

    others = check_other_attacks(req)
    if others:
        return "|".join(others)

    return "NORMAL"
