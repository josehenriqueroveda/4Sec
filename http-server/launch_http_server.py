import http.server
import socketserver

PORT = 9000
IP = "127.0.0.1"
Handler = http.server.SimpleHTTPRequestHandler


class SecureHandler(Handler):
    """A secure version of the SimpleHTTPRequestHandler that disables directory listing."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=None, **kwargs)


with socketserver.TCPServer((IP, PORT), SecureHandler) as httpd:
    print(
        """
  _      _    _                                              
 | |    | |  | |                                             
 | |__  | |_ | |_  _ __    ___   ___  _ __ __   __ ___  _ __ 
 | '_ \ | __|| __|| '_ \  / __| / _ \| '__|\ \ / // _ \| '__|
 | | | || |_ | |_ | |_) | \__ \|  __/| |    \ V /|  __/| |   
 |_| |_| \__| \__|| .__/  |___/ \___||_|     \_/  \___||_|   
                  | |                                        
                  |_|   
    """
    )
    print(f"Serving at http://{IP}:{PORT}/")
    httpd.serve_forever()
