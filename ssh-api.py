import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, subprocess, random, string

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
API_TOKEN = "SENHA_SUPER_SECRETA"  # 🔒 coloque sua senha/token aqui

def gerar_string(tamanho=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=tamanho))

class Handler(BaseHTTPRequestHandler):
    def _json(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_POST(self):
        if self.path not in ['/criar/teste', '/criar/ssh']:
            return self._json(404, {"erro": "Rota inválida"})

        # Verificação de token no cabeçalho
        token = self.headers.get('X-Api-Token')
        if token != API_TOKEN:
            return self._json(403, {"erro": "Token inválido"})

        usuario = gerar_string(random.randint(4, 8))
        senha = gerar_string(random.randint(4, 8))

        if self.path.endswith('teste'):
            validade = 3
            limite = 300
            script = f"{BASE_DIR}/criarteste.sh {usuario} {senha} {validade} {limite}"
        else:
            validade = 30
            limite = 1
            script = f"{BASE_DIR}/criarusuario.sh {usuario} {senha} {validade} {limite}"

        try:
            subprocess.check_call(script, shell=True)
            resp = {
                "status": "ok",
                "usuario": usuario,
                "senha": senha,
                "limite_conexoes": limite
            }

            if self.path.endswith('teste'):
                resp["validade_horas"] = validade
            else:
                resp["validade_dias"] = validade

            self._json(200, resp)
            
        except subprocess.CalledProcessError:
            self._json(500, {"erro": "Falha ao executar o script"})

def main():
    print("🚀 API rodando em http://0.0.0.0:9090")
    HTTPServer(('0.0.0.0', 9090), Handler).serve_forever()

if __name__ == "__main__":
    main()
