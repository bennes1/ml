
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import json
import cgi

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def do_HEAD(self):
        self._set_headers()
        
    # GET sends back a Hello world message
    def do_GET(self):
        from app.test import sample
        self.wfile.write(json.dumps(sample()).encode())
        
def run(server_class=HTTPServer, handler_class=Server, address='0.0.0.0', port=80):
    server_address = (address, port)
    httpd = server_class(server_address, handler_class)
    
    print ('Starting httpd on port %d...' % port)
    httpd.serve_forever()
    
if __name__ == "__main__":
    run()
