from http.server import BaseHTTPRequestHandler, HTTPServer  
from io import BytesIO
import os,re,time

class MagazineServ(BaseHTTPRequestHandler):
  def do_GET(self):
    file_to_open = ''
    if self.path == '/':
      self.send_response(301)
      self.send_header('Location','http://localhost:8081/index.html')
    else:
      try:
          file_to_open = open(self.path[1:]).read()
          self.send_response(200)
      except:
          file_to_open = "Page not found"
          self.send_response(404)
    self.end_headers()
    self.wfile.write(bytes(file_to_open, 'utf-8'))


  def do_POST(self):
    if self.path == '/upload':
      out, info, file_name = self.deal_post_data()
      self.send_response(200)
    self.end_headers()
    file_name = file_name.split("-")[-1]
    self.wfile.write(bytes("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Magazines MetaData</title>
    </head>
    <body>
        File {} {}
    </body>
    </html>
    """.format(file_name, "successfully uploaded" if out else "failed to upload, reason {}".format(info)), encoding = "utf-8"))


  def deal_post_data(self):
    boundary = b"------WebKitFormBoundary"
    remainbytes = int(self.headers['content-length'])
    line = self.rfile.readline()
    remainbytes -= len(line)
    if not boundary in line:
        return (False, "Content NOT begin with boundary", None)
    line = self.rfile.readline()
    remainbytes -= len(line)
    fn = re.findall(r'Content-Disposition.*name="fileToUpload"; filename="(.*)"', str(line))
    if not fn:
        return (False, "Can't find out file name...", None)
    path = os.path.join(os.getcwd(), "files")
    fn = os.path.join(path, str(time.time()) + "-" + fn[0])
    line = self.rfile.readline()
    remainbytes -= len(line)
    line = self.rfile.readline()
    remainbytes -= len(line)
    try:
        out = open(fn, 'wb')
    except IOError:
        return (False, "Can't create file to write, do you have permission to write?", None)
            
    preline = self.rfile.readline()
    remainbytes -= len(preline)
    while remainbytes > 0:
        line = self.rfile.readline()
        remainbytes -= len(line)
        if boundary in line:
            preline = preline[0:-1]
            if preline.endswith(b'\r'):
                preline = preline[0:-1]
            out.write(preline)
            out.close()
            return (True, "File '%s' upload success!" % fn, fn)
        else:
            out.write(preline)
            preline = line
    return (False, "Unexpect Ends of data.", None)


httpd = HTTPServer(('localhost', 8081), MagazineServ)
print("Server is running...")
httpd.serve_forever()


