#!/usr/bin/env python3
"""Simple HTTP server for the QuantumYield dashboard.
Serves the reports folder and exposes /_files to list broker_trades CSVs.
Usage:  python3 server.py          (default port 8080)
        python3 server.py 9000     (custom port)
"""
import json, os, re, sys
from http.server import SimpleHTTPRequestHandler, HTTPServer

CSV_PATTERN = re.compile(r'^broker_trades_\d{4}-\d{2}-\d{2}.*\.csv$', re.IGNORECASE)

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split('?')[0] == '/_files':
            files = sorted(f for f in os.listdir('.') if CSV_PATTERN.match(f))
            data = json.dumps(files).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            super().do_GET()

    def log_message(self, fmt, *args):
        pass  # suppress per-request noise

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"Dashboard → http://localhost:{port}/index.html")
HTTPServer(('', port), Handler).serve_forever()
