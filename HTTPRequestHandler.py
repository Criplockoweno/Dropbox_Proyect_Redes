class HTTPRequestHandler():
    
    def __init__(self, request):
        self.request = request
        self.FORMAT = 'utf-8'
    
    def parse_request(self, request):
        headers = {}
        lines = request.split('\n')
        print(lines)

        if(lines[0].find('----WebKitFormBoundary')!=-1):
            # Split the data by the boundary string
            parts = request.split('------WebKitFormBoundary')

            # Find the part that contains the file data
            for part in parts:
                if 'Content-Disposition: form-data; name="myFile"' in part:
                    # Extract the filename and file contents
                    filename = part.split('filename="')[1].split('"')[0]
                    filedata = part.split('\r\n\r\n')[1].split('\r\n------')[0]
                    print(filedata)
            headers.update({'Method': 'Webkit', 'Path': '/', 'Protocol': 'HTTP/1.1'})
        else:
            method, path, protocol = lines[0].split(" ")
            headers.update({'Method': method, 'Path': path, 'Protocol': protocol})
            for line in lines[1:]:
                if line.strip() != '':
                    key, value = line.split(': ')
                    headers[key] = value.strip()
        

        return headers

    # def parse_request(self, request_lines):
    #     # Parse method, path and protocol from the first line
    #     method, path, protocol = request_lines[0].split(" ")

    #     # Parse headers from the request
    #     headers = {}
    #     for line in request_lines[1:]:
    #         if line == "\r\n":
    #             break
    #         key, value = line.split(": ")
    #         headers[key] = value.strip()

    #     # Check if the request has a body (i.e., if it's a POST request)
    #     if "Content-Length" in headers:
    #         content_length = int(headers["Content-Length"])
    #         body = "".join(request_lines[-content_length:])
    #     else:
    #         body = None

    #     # Return a dictionary with the relevant values
    #     return {"method": method, "path": path, "protocol": protocol, "headers": headers, "body": body}

    
    def handle_request(self):
        headers = self.parse_request(self.request)
        response = ""
        if headers['Method'] == 'GET':
            response = self.do_GET()
        
        #SAVE FILE
        if headers['Method'] == 'POST':
            response = self.do_POST()

        if headers['Method'] == 'Webkit':
            response = self.do_POST()
        return response
        
    def do_GET(self):
        with open("index.html", "r", encoding=self.FORMAT) as f:
            html = f.read()
        response = ('HTTP/1.1 200 OK\r\n' 
            + 'Content-Type: text/html\r\n' 
            + 'Content-Length: {}\r\n'.format(len(html)) 
            + '\r\n' + html)
        return response
    
    def do_POST(self):
        with open('test', "wb") as f:
            f.write(self.request.encode(self.FORMAT))        
        response = "HTTP/1.1 200 OK\r\n\r\nFile uploaded successfully"
        return response
    
    # def do_POST(self):
    #     header = self.parse_request(self.request);
    #     content_length = int(header['Content-Length'])
    #     with open('test', 'wb') as f:
    #         f.write(self.rfile.read(content_length))
    #         print(content_length)
    #     response = "HTTP/1.1 200 OK\r\n\r\nFile uploaded successfully"
    #     return response


