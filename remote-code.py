#!/usr/bin/which python

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import sys
import socket

DEFAULT_PORT = 1129 # デフォルトのポート番号(イイニク)

def bind_check(port=DEFAULT_PORT):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", port))
        s.close()
    except OSError as e:
        return False
    return True

class Server(BaseHTTPRequestHandler):
    def _send_response(self, message, code=200):
        response = {"code": code, "message": message}
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
        self.log_message(json.dumps(response))

    # GET
    def do_GET(self):
        self._send_response("Not Found", 404)

    # POST
    def do_POST(self):
        length = int(self.headers["content-length"])
        message = json.loads(self.rfile.read(length))
        print(message["command"])
        rtn = os.system(message["command"])
        print(rtn)
        if rtn == 0:
            self._send_response("OK")
        else:
            self._send_response("NG", 400)

def run(server_class=HTTPServer, handler_class=Server, port=DEFAULT_PORT):
    server_address = ("localhost", port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    if bind_check() == False:
        # 2重起動の防止
        sys.exit(0)
    run()
