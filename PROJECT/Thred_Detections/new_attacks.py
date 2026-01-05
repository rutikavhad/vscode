import re
import math
from urllib.parse import unquote_plus

def security_scanner():
    # 1. SIGNATURES (Added: XXE, SSTI, CRLF, Prototype Pollution, Deserialization)
    sqli = [" or 1=1", "union select", "sleep(", "benchmark(", "--", "order by"]
    cmd = [";", "&&", "||", "|", "`", "$("]
    path = ["../", "..\\", "php://", "file://", "etc/passwd", "boot.ini"]
    xss = ["<script", "javascript:", "onerror=", "onload=", "alert("]
    nosql = ["$gt", "$ne", "$where", "$regex"]
    
    # Critical Server Attacks
    server_attack = [
        "{{", "${", "<%=",                # SSTI
        "<!entity", "<!doctype",          # XXE
        "%0d%0a", "\\r\\n",               # CRLF
        "__proto__", "constructor.prot",  # Prototype Pollution
        "o:", "a:", "s:", "ac ed 00 05"   # Deserialization (PHP/Java)
    ]
    
    blocked_ext = [".php", ".py", ".exe", ".jsp", ".sh", "js", ".bash", ".c", ".asm", ".java", ".class"]
    allowed_ext = [".png", ".jpg", ".jpeg", ".gif", ".pdf", ".txt", "text"]

    # 2. INPUT & NORMALIZATION
    raw_data = input("enter request: ")
    # Double decoding to catch hidden patterns
    text = unquote_plus(unquote_plus(raw_data)).lower()
    
    status = "normal"

    # 3. FILE UPLOAD CHECK (Your specific logic)
    if 'filename="' in raw_data:
        matches = re.findall(r'filename="([^"]+)"', raw_data, re.IGNORECASE)
        found_file_issue = False
        for fname in matches:
            fname = fname.lower()

            # block dangerous extensions
            for ext in blocked_ext:
                if fname.endswith(ext):
                    status = "file_upload_abuse"
                    found_file_issue = True
                    break

            # block double extensions
            if not found_file_issue and fname.count(".") >= 2:
                status = "file_upload_abuse"
                found_file_issue = True

            # allow safe extensions
            if not found_file_issue:
                safe = False
                for ext in allowed_ext:
                    if fname.endswith(ext):
                        status = "normal"
                        safe = True
                        break
                
                if not safe:
                    status = "file_upload_abuse"
                    found_file_issue = True
            
            if found_file_issue:
                break

    # 4. NON-FILE ATTACK CHECKS
    if status == "normal":
        found = []
        if any(s in text for s in sqli): found.append("sql_injection")
        if any(s in text for s in cmd): found.append("command_injection")
        if any(s in text for s in path): found.append("path_traversal")
        if any(s in text for s in xss): found.append("xss")
        if any(s in text for s in nosql): found.append("nosql_injection")
        if any(s in text for s in server_attack): found.append("critical_server_attack")
        
        if found:
            status = "|".join(found)

    # 5. FINAL RESULT
    if status != "normal":
        print(f"block: {status}")
    else:
        # Calculate Entropy for normal traffic
        if text:
            freq = {c: text.count(c) for c in set(text)}
            entropy = -sum((v/len(text)) * math.log2(v/len(text)) for v in freq.values())
            print(f"normal (entropy: {round(entropy, 2)})")
        else:
            print("normal")

security_scanner()



#SSTI: Patterns like {{7*7}} or ${7*7}.

#XXE: XML blocks containing <!ENTITY.

#CRLF: URL-encoded line breaks %0d%0a.

#Prototype Pollution: The dangerous __proto__ string.

#Deserialization: Standard serialization headers for PHP (o:, a:) and Java (ac ed 00 05).
