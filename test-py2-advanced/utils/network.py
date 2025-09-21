#!/usr/bin/env python2
"""
Network utilities with Python 2 patterns
"""

import urllib.request, urllib.error, urllib.parse
import urllib.parse
import http.cookiejar
import http.client
import http.server
import socketserver

def download_file(url, filename):
    """Download file using Python 2 urllib2"""
    print("Downloading from:", url)
    
    try:
        # Parse URL
        parsed = urllib.parse.urlparse(url)
        print("Scheme:", parsed.scheme)
        print("Host:", parsed.netloc)
        
        # Create request
        request = urllib.request.Request(url)
        request.add_header('User-Agent', 'Python2-Test-Client/1.0')
        
        # Open URL
        response = urllib.request.urlopen(request, timeout=10)
        
        print("Response code:", response.getcode())
        print("Content type:", response.info().gettype())
        
        # Read content
        content = response.read()
        
        # Write to file
        with open(filename, 'wb') as f:
            f.write(content)
            
        print("Downloaded %d bytes to %s" % (len(content), filename))
        
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e.code, e.reason)
    except urllib.error.URLError as e:
        print("URL Error:", e.reason)
    except Exception as e:
        print("Download failed:", e)

def create_simple_server():
    """Create simple HTTP server using Python 2 classes"""
    
    class MyHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            print("GET request received for:", self.path)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Send response
            response = """
            <html>
            <body>
            <h1>Python 2 Test Server</h1>
            <p>Path: %s</p>
            <p>Server running on Python 2</p>
            </body>
            </html>
            """ % self.path
            
            self.wfile.write(response)
        
        def log_message(self, format, *args):
            print("Server log:", format % args)
    
    # Create server
    try:
        server = socketserver.TCPServer(('localhost', 8000), MyHandler)
        print("Server created on port 8000")
        return server
    except Exception as e:
        print("Failed to create server:", e)
        return None

def test_http_client():
    """Test HTTP client with Python 2 httplib"""
    print("Testing HTTP client...")
    
    try:
        # Create connection
        conn = http.client.HTTPConnection('httpbin.org', timeout=10)
        
        # Make request
        conn.request('GET', '/get')
        response = conn.getresponse()
        
        print("Status:", response.status, response.reason)
        print("Headers:")
        for header, value in response.getheaders():
            print("  %s: %s" % (header, value))
        
        # Read response
        data = response.read()
        print("Response length:", len(data))
        
        conn.close()
        
    except http.client.HTTPException as e:
        print("HTTP Exception:", e)
    except Exception as e:
        print("Connection failed:", e)

if __name__ == "__main__":
    print("Network utilities test")
    print("=" * 40)
    
    # Test URL parsing
    test_url = "http://example.com/path?param=value#fragment"
    parsed = urllib.parse.urlparse(test_url)
    print("URL parts:")
    print("  scheme:", parsed.scheme)
    print("  netloc:", parsed.netloc)
    print("  path:", parsed.path)
    print("  query:", parsed.query)
    print("  fragment:", parsed.fragment)
    
    print()
    test_http_client()