import SimpleHTTPServer
import SocketServer
import json
import hmac
import os

PORT = 4532

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        content = "<html><body><h1>"+message+"</h1></body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_POST(self):
        content_len = int(self.headers.getheader('content-length', 0))
        verify = self.headers.getheader('X-Hub-Signature',0)
        post_body = self.rfile.read(content_len)
        print post_body
        loaded_json = json.loads(post_body)
        digest1 = hmac.new(SECRET,post_body)
        print(digest1.hexdigest())
        if hmac.compare_digest(digest1.hexdigest(),verify[5:]):
            if loaded_json["repository"]["full_name"] == REPO:
                print "execute deploy"
                self._set_headers()
                self.wfile.write(self._html("POST Success!"))
            else:
                self._set_headers()
                self.wfile.write(self._html("POST OK, Wrong repository...!"))
        else:
            self._set_headers()
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