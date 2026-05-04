"""
Auth & Authorization Endpoint Finder
=====================================
Only use on websites you own or have written permission to test.

Install: pip install requests beautifulsoup4
Usage:   python auth_endpoints.py https://example.com
"""

import re, time, sys
from urllib.parse import urljoin, urlparse
from collections import deque
import requests
from bs4 import BeautifulSoup

AUTH_KEYWORDS = [
    "login", "logout", "signin", "signout", "signup", "register",
    "auth", "oauth", "sso", "token", "refresh", "password", "forgot",
    "reset", "verify", "confirm", "2fa", "mfa", "otp",
    "admin", "dashboard", "panel", "manage",
    "profile", "account", "settings", "user", "users",
    "role", "permission", "privilege", "grant",
    "delete", "update", "edit", "create", "upload", "export", "import",
    "api/", "/v1/", "/v2/", "graphql",
]

JS_PATHS = re.compile(r'["\'`](/[a-zA-Z0-9_\-./?=&%]+)["\'`]')

def is_auth(url):
    return any(k in url.lower() for k in AUTH_KEYWORDS)

def extract(html, base, origin):
    found = set()
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(True):
        for attr in ["href", "src", "action"]:
            val = tag.get(attr, "")
            if val and not val.startswith(("#", "mailto:", "tel:", "javascript:")):
                full = urljoin(base, val).split("#")[0]
                if urlparse(full).netloc == origin:
                    found.add(full)
    for script in soup.find_all("script"):
        for m in JS_PATHS.findall(script.get_text()):
            full = urljoin(base, m).split("#")[0]
            if urlparse(full).netloc == origin:
                found.add(full)
    return found

def scan(start, max_pages=80, delay=0.4, cookie=""):
    origin = urlparse(start).netloc
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (AuthScanner)"
    if cookie:
        for p in cookie.split(";"):
            if "=" in p:
                k, v = p.strip().split("=", 1)
                session.cookies.set(k, v)

    visited, queue, auth_urls = set(), deque([start]), set()

    print(f"\nScanning: {start}\n")
    while queue and len(visited) < max_pages:
        url = queue.popleft()
        if url in visited: continue
        visited.add(url)
        try:
            r = session.get(url, timeout=8)
            new = extract(r.text, url, origin)
            for u in new:
                if u not in visited: queue.append(u)
                if is_auth(u): auth_urls.add(u)
            print(f"  [{r.status_code}] {url}")
        except: pass
        time.sleep(delay)

    print(f"\n{'='*55}")
    print(f"  AUTH / AUTHZ ENDPOINTS FOUND: {len(auth_urls)}")
    print(f"{'='*55}")
    for u in sorted(auth_urls):
        print(f"  {u}")
    print()

    with open("auth_urls.txt", "w") as f:
        f.write(f"Target: {start}\n\n")
        for u in sorted(auth_urls):
            f.write(u + "\n")
    print("Saved to auth_urls.txt\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python auth_endpoints.py <url> [cookie]")
        sys.exit(1)
    cookie = sys.argv[2] if len(sys.argv) > 2 else ""
    scan(sys.argv[1], cookie=cookie)