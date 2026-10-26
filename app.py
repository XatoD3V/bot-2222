import os, json
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

NAME = os.environ.get("SERVER_NAME", "servidor")
DIRS = {"compartido": "/data/compartido", "local": "/data/local"}
for d in DIRS.values():
    os.makedirs(d, exist_ok=True)

class Handler(BaseHTTPRequestHandler):
    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/":
            self._json(200, {"atendido_por": NAME,
                             "usa": "GET /archivos | POST /guardar?nombre=a.txt&donde=compartido|local"})
        elif u.path == "/archivos":
            self._json(200, {"atendido_por": NAME,
                             **{k: sorted(os.listdir(v)) for k, v in DIRS.items()}})
        else:
            self._json(404, {"error": "no existe"})

    def do_POST(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path != "/guardar":
            return self._json(404, {"error": "no existe"})
        nombre = os.path.basename(q.get("nombre", ["archivo.txt"])[0])
        donde = q.get("donde", ["compartido"])[0]
        if donde not in DIRS or not nombre:
            return self._json(400, {"error": "parametros invalidos"})
        data = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        with open(os.path.join(DIRS[donde], nombre), "wb") as f:
            f.write(data)
        self._json(201, {"atendido_por": NAME, "guardado": nombre, "en": donde})

ThreadingHTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
