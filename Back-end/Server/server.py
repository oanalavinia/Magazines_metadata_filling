from http.server import BaseHTTPRequestHandler, HTTPServer, CGIHTTPRequestHandler
from io import BytesIO
import os,re,time
from pymongo import MongoClient

class MagazineServ(BaseHTTPRequestHandler):
  def do_GET(self):
    file_to_open = ''
    os.chdir(r'C:\Users\TudorIacobuta\Desktop\Git Repositories\GitHub\Magazines_metadata_filling\Front-end')
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
    if file_name is not None:
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
    fn = os.path.join(path, time.strftime("%y-%m-%d-%H-%M-%S",time.localtime()) + "-" + fn[0])
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


os.chdir(r'..\..\Front-end')
RequestHandler = CGIHTTPRequestHandler
httpd = HTTPServer(('localhost', 8081), RequestHandler)
print("Server is running...")
httpd.serve_forever()




