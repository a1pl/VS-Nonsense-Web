from http.server import SimpleHTTPRequestHandler, HTTPServer
import sys
import os

class CSPHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CSP header with unsafe-eval enabled
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self' 'unsafe-eval' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https:; font-src 'self' data:; img-src 'self' data: https:; media-src 'self' data: https:;"
        )
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()
    
    def log_message(self, format, *args):
        # Print CSP info when server starts
        print(f"[{self.client_address[0]}] {format % args}")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    
    host = "127.0.0.1"
    
    server = HTTPServer((host, port), CSPHTTPRequestHandler)
    print(f"Server running on http://{host}:{port}")
    print("CSP Header: script-src 'self' 'unsafe-eval' 'unsafe-inline'")
    print("Press Ctrl+C to stop")
    print()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        server.server_close()