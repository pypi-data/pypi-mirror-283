import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import threading
import os
from urllib.parse import urlsplit

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_request(self, requesttype):
        # Parse the URL
        url = self.path
        parsed_url = urlsplit(url)
        target_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

        # Get headers
        headers = {key: val for key, val in self.headers.items()}

        # Get request body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length else None

        print("Intercepted target URL: {}".format(target_url))

        # Forward the request
        if requesttype == "get":
            response = requests.get(target_url, headers=headers)
        elif requesttype == "post":
            response = requests.post(target_url, headers=headers)
        else:
            return("HTTP type not supported")

        # Send response back to the client
        self.send_response(response.status_code)
        for key, value in response.headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(response.content)
        

    def do_GET(self):
        self.do_request("get")

    def do_POST(self):
        self.do_request("post")

def start_proxy():
    print("Starting proxy")
    server_address = ('', 6665)
    httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
    httpd.serve_forever()

def init_proxy():
    proxy = "http://localhost:6665"
    proxy_thread = threading.Thread(target=start_proxy)
    proxy_thread.daemon = True
    proxy_thread.start()
    return proxy

def create_proxied_session():
    proxy = init_proxy()
    session = requests.Session()
    session.proxies = {
        'http': proxy,
        'https': proxy,
    }
    return session