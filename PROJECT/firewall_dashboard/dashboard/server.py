import json, csv, os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

BASE = os.path.dirname(__file__)
CSV_FILE = os.path.join("..", "traffic_events.csv")
USERS = os.path.join(BASE, "users.json")

class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.file("templates/login.html")
        elif self.path == "/dashboard":
            self.file("templates/index.html")
        elif self.path == "/profile":
            self.file("templates/profile.html")
        elif self.path == "/api/attacks":
            self.json(self.read_csv())
        elif self.path.startswith("/static/"):
            self.static()
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/login":
            length = int(self.headers["Content-Length"])
            data = parse_qs(self.rfile.read(length).decode())
            user = data.get("username", [""])[0]
            pwd = data.get("password", [""])[0]

            with open(USERS) as f:
                users = json.load(f)

            if user in users and users[user]["password"] == pwd:
                self.redirect("/dashboard")
            else:
                self.redirect("/")

    def read_csv(self):
        out = []
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE) as f:
                for r in csv.DictReader(f):
                    out.append(r)
        return out[-300:]

    def file(self, path):
        with open(os.path.join(BASE, path), "rb") as f:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f.read())

    def static(self):
        path = os.path.join(BASE, self.path.lstrip("/"))
        with open(path, "rb") as f:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f.read())

    def json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def redirect(self, loc):
        self.send_response(302)
        self.send_header("Location", loc)
        self.end_headers()

print("[+] IntelliWAF Dashboard running at http://localhost:9000")
HTTPServer(("0.0.0.0", 9000), Server).serve_forever()
