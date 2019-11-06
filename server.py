import SimpleHTTPServer
import SocketServer
import json
import hmac
import hashlib
import os

PORT = 4532

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def _set_headers(self, code):
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        content = "<html><body><h1>"+message+"</h1></body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_POST(self):
        content_len = int(self.headers.getheader('content-length', 0))
        verify = self.headers.getheader('X-Hub-Signature')
        post_body = self.rfile.read(content_len)
        loaded_json = json.loads(post_body)
        signature = hmac.new(SECRET,post_body, hashlib.sha1).hexdigest()
        if hmac.compare_digest(signature,verify[5:]):
            if loaded_json["repository"]["full_name"] == REPO:
                try: 
                    os.system("./deploy.sh")
                    self._set_headers(200)
                    self.wfile.write(self._html("POST Success!"))
                except:
                    self._set_headers(500)
                    self.wfile.write(self._html("Deploy failed!"))
            else:
                self._set_headers(500)
                self.wfile.write(self._html("POST OK, Wrong repository...!"))
        else:
            self._set_headers(500)
            self.wfile.write(self._html("POST OK, Hash check failed...!"))

try:  
   SECRET=os.environ["SECRET"]
   REPO=os.environ["REPO"]
except KeyError: 
   print "Please set the environment variable SECRET & REPO"
   sys.exit(1)

Handler = ServerHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()