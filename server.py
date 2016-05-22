import http.server
import urllib.parse
import os

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.log_message("uri: " + urllib.parse.urlparse(self.path)[2])
        parsed = urllib.parse.urlparse(self.path)[2].split("/")
        # add something to check if it's an api request
        if not "api" in parsed:
            self.get_file(parsed)

    def get_file(self, parsedURI):
    	# append index.html or .html if necessary
        if '' == parsedURI[len(parsedURI) - 1]:
            parsedURI[len(parsedURI) - 1] = "index.html"
        if not '.' in parsedURI[len(parsedURI) - 1]:
            parsedURI[len(parsedURI) - 1] += ".html"
        # check if the path exists
        p = os.getcwd() + "/".join(parsedURI)
        self.log_message("full path: " + p)
        # if it does, f = the file, send good headers
        if os.path.isfile(p):
            f = open(p, 'rb', 0)
            self.send_response_only(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
        else:
            #file dne, send 400NotFound and 400 response
            f = open(os.getcwd() + "/400NotFound.html", 'rb', 0)
            self.send_response_only(400)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()

        # send whichever file and the http 'end of message'
        self.wfile.write(f.read())

    def get_api(self, parsedURI):
        pass

# server address
server_address = ('localhost', 8000)

# how we're going to handle requests
requestHandler =  MyRequestHandler #http.server.SimpleHTTPRequestHandler
#requestHandler = http.server.SimpleHTTPRequestHandler

# create our server
server = http.server.HTTPServer(server_address, requestHandler)

# run the server
server.serve_forever()
