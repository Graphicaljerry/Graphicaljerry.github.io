#!/usr/bin/env python3
"""
Python backend server for AI Photo Summarizer
This is a development server alternative to the PHP backend.
"""

import http.server
import socketserver
import json
import urllib.request
import urllib.error
from urllib.parse import urlparse
import os
import sys

# Load API key from config file or environment variable
try:
    from config_local import OPENAI_API_KEY
except ImportError:
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    if not OPENAI_API_KEY:
        print("❌ ERROR: OpenAI API key not found!")
        print("Please either:")
        print("  1. Copy config_local.example.py to config_local.py and add your API key")
        print("  2. Set OPENAI_API_KEY environment variable")
        sys.exit(1)

class PhotoAnalyzerHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests to analyze photos"""
        if self.path == '/analyze-photo.php':
            self.handle_analyze_photo()
        else:
            self.send_error(404, "Not found")

    def handle_analyze_photo(self):
        """Process photo analysis request"""
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            if 'image' not in data:
                self.send_json_response({'error': 'No image data provided'}, 400)
                return

            base64_image = data['image']

            # Prepare OpenAI API request
            api_url = 'https://api.openai.com/v1/chat/completions'

            request_data = {
                'model': 'gpt-4o-mini',
                'messages': [
                    {
                        'role': 'user',
                        'content': [
                            {
                                'type': 'text',
                                'text': 'Please provide a detailed description of this image. Include what you see, the setting, colors, mood, and any notable details.'
                            },
                            {
                                'type': 'image_url',
                                'image_url': {
                                    'url': f'data:image/jpeg;base64,{base64_image}'
                                }
                            }
                        ]
                    }
                ],
                'max_tokens': 500
            }

            # Make request to OpenAI
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {OPENAI_API_KEY}'
            }

            request_body = json.dumps(request_data).encode('utf-8')
            req = urllib.request.Request(api_url, data=request_body, headers=headers)

            try:
                with urllib.request.urlopen(req, timeout=30) as response:
                    response_data = response.read()
                    self.send_json_response(json.loads(response_data), 200)
            except urllib.error.HTTPError as e:
                error_data = e.read().decode('utf-8')
                print(f"❌ OpenAI API Error: {error_data}")
                try:
                    self.send_json_response(json.loads(error_data), e.code)
                except:
                    self.send_json_response({'error': error_data}, e.code)
            except urllib.error.URLError as e:
                print(f"❌ Network Error: {str(e)}")
                self.send_json_response({'error': f'Network error: {str(e)}'}, 500)

        except Exception as e:
            print(f"❌ Server Error: {str(e)}")
            import traceback
            traceback.print_exc()
            self.send_json_response({'error': str(e)}, 500)

    def send_json_response(self, data, status_code):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def end_headers(self):
        # Add CORS headers to all responses
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def run_server(port=8000):
    """Start the development server"""
    handler = PhotoAnalyzerHandler

    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🚀 AI Photo Summarizer Server Running!")
        print(f"📍 Open your browser to: http://localhost:{port}/photo-summarizer.html")
        print(f"🔑 API Key configured and ready")
        print(f"\n✨ Upload a photo and it will be automatically analyzed!\n")
        print("Press Ctrl+C to stop the server")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped. Thanks for using AI Photo Summarizer!")

if __name__ == '__main__':
    run_server()
