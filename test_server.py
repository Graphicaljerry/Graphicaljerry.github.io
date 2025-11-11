#!/usr/bin/env python3
"""
Simple photo analyzer server for local testing
"""
import http.server
import socketserver
import json
import urllib.request
import urllib.error
from pathlib import Path

# Load API key
try:
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from config_local import OPENAI_API_KEY
    print(f"API Key loaded: {OPENAI_API_KEY[:20]}...")
except ImportError:
    print("❌ ERROR: config_local.py not found!")
    print("Please copy config_local.example.py to config_local.py and add your API key")
    import sys
    sys.exit(1)

class PhotoHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        print(f"📨 POST request to: {self.path}")

        if self.path == '/analyze-photo.php':
            try:
                # Read request
                length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(length)
                print(f"📦 Received {length} bytes")

                data = json.loads(body.decode('utf-8'))
                image_data = data.get('image', '')

                if not image_data:
                    self.send_error_response({'error': 'No image data'}, 400)
                    return

                print(f"🖼️  Image data length: {len(image_data)}")

                # Call OpenAI
                print("☁️  Calling OpenAI API...")
                api_request = {
                    'model': 'gpt-4o-mini',
                    'messages': [{
                        'role': 'user',
                        'content': [
                            {'type': 'text', 'text': 'Please provide a detailed description of this image. Include what you see, the setting, colors, mood, and any notable details.'},
                            {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{image_data}'}}
                        ]
                    }],
                    'max_tokens': 500
                }

                req = urllib.request.Request(
                    'https://api.openai.com/v1/chat/completions',
                    data=json.dumps(api_request).encode('utf-8'),
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {OPENAI_API_KEY}'
                    }
                )

                try:
                    with urllib.request.urlopen(req, timeout=60) as response:
                        result = json.loads(response.read().decode('utf-8'))
                        print("✅ OpenAI API success!")

                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(json.dumps(result).encode('utf-8'))

                except urllib.error.HTTPError as e:
                    error_body = e.read().decode('utf-8')
                    print(f"❌ OpenAI API Error {e.code}: {error_body}")
                    self.send_error_response({'error': f'OpenAI API Error: {error_body}'}, e.code)

            except Exception as e:
                print(f"❌ Server Error: {str(e)}")
                import traceback
                traceback.print_exc()
                self.send_error_response({'error': str(e)}, 500)
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def send_error_response(self, data, code):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

PORT = 8001
Handler = PhotoHandler

# Get local IP address for network access
import socket
local_ip = socket.gethostbyname(socket.gethostname())

print(f"🚀 AI Photo Summarizer Server Starting...")
print(f"📍 Local URL: http://localhost:{PORT}/photo-summarizer.html")
print(f"🌐 Network URL: http://{local_ip}:{PORT}/photo-summarizer.html")
print(f"🔑 API Key: Configured")
print(f"\n✨ Access from any device on your WiFi using the Network URL!")
print(f"💡 On this computer, use either URL\n")

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
