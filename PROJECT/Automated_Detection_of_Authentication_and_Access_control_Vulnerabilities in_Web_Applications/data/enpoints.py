"""
Endpoint Discovery Tool — USE ONLY ON SITES YOU OWN OR HAVE WRITTEN PERMISSION TO TEST.
pip install requests beautifulsoup4 colorama
"""

import re, sys, json, time, argparse
from urllib.parse import urljoin, urlparse
from collections import deque

import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

init(autoreset=True)

JS_URL  = re.compile(r"""["'`](/[a-zA-Z0-9_\-./]*(?:\?[^"'`]*)?)["'`]""")
API_PAT = re.compile(r"""["'`]((?:/api/|/v\d+/|/rest/|/graphql|/gql)[^\s"'`]*)["'`]""")
JS_HTTP = re.compile(r"""(?:fetch|axios|http|ajax)\s*\(\s*["'`]([^"'`]+)["'`]""", re.I)

RISK_RULES = [
    ({"admin","panel","manage","dashboard","config"},              "HIGH",   "admin"),
    ({"login","signin","auth","token","oauth","sso"},              "HIGH",   "authentication"),
    ({"password","reset","forgot","2fa","mfa","otp","verify"},    "HIGH",   "credential-flow"),
    ({"delete","remove","destroy"},                                "HIGH",   "destructive-action"),
    ({"upload","import","export","backup","restore"},              "MEDIUM", "data-transfer"),
    ({"profile","account","settings","user","role","permission"},  "MEDIUM", "authorization"),
    ({"/api/","/v1/","/v2/","/v3/","/rest/","/graphql","/gql"},   "MEDIUM", "api"),
    ({"logout","signout"},                                         "MEDIUM", "session-management"),
]

SKIP_EXT = {"png","jpg","jpeg","gif","svg","ico","css","woff","woff2","ttf","eot","mp4","pdf"}


def classify(url):
    full = (urlparse(url).path + "?" + urlparse(url).query).lower()
    risk, tags = "LOW", []
    for keywords, lvl, tag in RISK_RULES:
        if any(k in full for k in keywords):
            if lvl == "HIGH" or (lvl == "MEDIUM" and risk == "LOW"):
                risk = lvl
            tags.append(tag)
    return risk, tags


def extract(text, base, origin, is_js=False):
    eps = set()
    soup = None if is_js else BeautifulSoup(text, "html.parser")

    if soup:
        for tag in soup.find_all(True):
            for attr in ("href","src","action","data-url","data-href","data-endpoint"):
                val = tag.get(attr, "")
                if val and not val.startswith(("#","mailto:","tel:","javascript:")):
                    add_if_same(urljoin(base, val), origin, eps)
        text = " ".join(s.get_text() for s in soup.find_all("script"))

    for pat in (JS_URL, API_PAT, JS_HTTP):
        for m in pat.findall(text):
            add_if_same(urljoin(base, m), origin, eps)

    return eps


def add_if_same(url, origin, eps):
    url = url.split("#")[0]
    if urlparse(url).netloc == urlparse(origin).netloc:
        eps.add(url)


def crawl(start, max_pages=100, delay=0.5, headers=None, cookies=None, verbose=True):
    origin  = "{0.scheme}://{0.netloc}".format(urlparse(start))
    session = requests.Session()
    session.headers.update(headers or {"User-Agent": "Mozilla/5.0 (SecurityResearch/1.0)"})
    if cookies: session.cookies.update(cookies)

    visited, all_eps, queue = set(), set(), deque([start])
    crawled = 0

    print(f"\n{Fore.CYAN}{'='*55}\n  Target: {start}  |  Max: {max_pages} pages\n{'='*55}{Style.RESET_ALL}\n")

    while queue and crawled < max_pages:
        url = queue.popleft()
        if url in visited: continue
        visited.add(url)
        try:
            r = session.get(url, timeout=10, allow_redirects=True)
            crawled += 1
            ct = r.headers.get("Content-Type","")
            if verbose:
                c = Fore.GREEN if r.status_code == 200 else Fore.YELLOW
                print(f"  {c}[{r.status_code}]{Style.RESET_ALL} {url}")

            is_js = "javascript" in ct or url.endswith(".js")
            new_eps = extract(r.text, url, origin, is_js)

            for ep in new_eps:
                ext = urlparse(ep).path.rsplit(".", 1)[-1].lower()
                if ep not in visited and ep not in queue and ext not in SKIP_EXT:
                    queue.append(ep)
            all_eps.update(new_eps)
        except requests.RequestException as e:
            if verbose: print(f"  {Fore.RED}[ERR]{Style.RESET_ALL} {url} — {e}")
        time.sleep(delay)

    results = []
    for ep in sorted(all_eps):
        risk, tags = classify(ep)
        results.append({"url": ep, "risk": risk, "tags": tags})
    results.sort(key=lambda x: {"HIGH":0,"MEDIUM":1,"LOW":2}[x["risk"]])

    return {"target": start, "pages_crawled": crawled,
            "total_endpoints": len(results), "endpoints": results}


def print_report(data):
    eps   = data["endpoints"]
    high  = [e for e in eps if e["risk"]=="HIGH"]
    med   = [e for e in eps if e["risk"]=="MEDIUM"]
    low   = [e for e in eps if e["risk"]=="LOW"]

    print(f"\n{Fore.CYAN}{'='*55}")
    print(f"  Pages: {data['pages_crawled']}  |  Endpoints: {data['total_endpoints']}"
          f"  |  H:{len(high)} M:{len(med)} L:{len(low)}")
    print(f"{'='*55}{Style.RESET_ALL}\n")

    for label, color, group in (
        ("HIGH RISK — Auth / Admin / Destructive", Fore.RED,    high),
        ("MEDIUM RISK — API / Authorization / Data", Fore.YELLOW, med),
        ("LOW RISK", Fore.GREEN, low),
    ):
        if not group: continue
        print(f"{color}◆ {label}{Style.RESET_ALL}")
        for e in group:
            tags = ", ".join(e["tags"]) or "—"
            print(f"  {color}[{e['risk'][:3]}]{Style.RESET_ALL}  {e['url']}")
            if e["tags"]: print(f"         Tags: {tags}")
        print()


def save_results(data, base="endpoints"):
    with open(f"{base}.json","w") as f: json.dump(data, f, indent=2)
    with open(f"{base}.txt","w") as f:
        f.write(f"Endpoint Discovery Report\nTarget: {data['target']}\nTotal: {data['total_endpoints']}\n\n")
        for e in data["endpoints"]:
            f.write(f"[{e['risk']:6}] {e['url']}  (tags: {', '.join(e['tags']) or 'none'})\n")
    print(f"{Fore.CYAN}Saved:{Style.RESET_ALL} {base}.json  /  {base}.txt\n")


def main():
    p = argparse.ArgumentParser(description="Endpoint Discovery — authorized testing only")
    p.add_argument("url")
    p.add_argument("--max-pages", type=int,   default=100)
    p.add_argument("--delay",     type=float, default=0.5)
    p.add_argument("--output",    default="endpoints")
    p.add_argument("--cookie",    default="")
    p.add_argument("--quiet",     action="store_true")
    args = p.parse_args()

    cookies = dict(part.strip().split("=",1) for part in args.cookie.split(";") if "=" in part)
    data = crawl(args.url, args.max_pages, args.delay, cookies=cookies, verbose=not args.quiet)
    print_report(data)
    save_results(data, args.output)

if __name__ == "__main__":
    main()