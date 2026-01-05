import re
from urllib.parse import unquote_plus

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
sqli = [" or 1=1", "union select", "sleep(", "benchmark(", "--","order by"]
cmd = [";", "&&", "||", "|", "`", "$("]
path = ["../", "..\\", "php://", "file://", "data://", "/etc/passwd","/config/","boot.ini"]
xss = ["<script", "</script>", "javascript:", "onerror=", "onload=","alert("]
nosql = ["$gt", "$ne", "$where", "$regex"]

allowed_txt = [".png", ".jpg", ".jpeg", ".gif", ".pdf", ".txt","text"]
blocked_txt = [".php", ".py", ".exe", ".jsp", ".sh","js",".bash",".c",".asm",".java",".class","xml]

# =========================
# FILE UPLOAD CHECK (ONLY)
# =========================
def check_file_upload(req):
    """
    Returns:
      - "NORMAL" if safe file upload
      - "FILE_UPLOAD_ABUSE" if malicious
      - None if not a file upload
    """
    ct = req.headers.get("Content-Type", "").lower()
    if "multipart/form-data" not in ct:
        return None

    try:
        body = req.get_text(strict=False) or ""
    except:
        return "FILE_UPLOAD_ABUSE"

    matches = re.findall(r'filename="([^"]+)"', body, re.IGNORECASE)

    for fname in matches:
        fname = fname.lower()

        # block dangerous extensions
        for ext in blocked_txt:
            if fname.endswith(ext):
                return "FILE_UPLOAD_ABUSE"

        # block double extensions
        if fname.count(".") >= 2:
            return "FILE_UPLOAD_ABUSE"

        # allow safe extensions
        for ext in allowed_txt:
            if fname.endswith(ext):
                return "NORMAL"

        # unknown extension → block
        return "FILE_UPLOAD_ABUSE"

    return "NORMAL"

# =========================
# NON-FILE ATTACK CHECKS
# =========================
def check_other_attacks(req):
    attacks = []
    inputs = []

    for v in req.query.values():
        inputs.append(v)

    try:
        body = req.get_text(strict=False) or ""
        inputs.append(body)
    except:
        pass

    norm_inputs = [normalize(i) for i in inputs]

    if any(any(s in d for s in sqli) for d in norm_inputs):
        attacks.append("SQL_INJECTION")

    if any(any(s in d for s in cmd) for d in norm_inputs):
        attacks.append("COMMAND_INJECTION")

    if any(any(s in d for s in path) for d in norm_inputs):
        attacks.append("PATH_TRAVERSAL")

    if any(any(s in d for s in xss) for d in norm_inputs):
        attacks.append("XSS")
    if any(any(s in d for s in nosql) for d in norm_inputs):
        attacks.append("NOSQL")
    return attacks
