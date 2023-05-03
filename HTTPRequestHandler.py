from HTMLPreprocessing import HTMLPreprocessing

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
            headers.update({'Method': 'Webkit', 'Path': '/', 'Protocol': 'HTTP/1.1', 'Content-Disposition': 'form-data', 'filename': filename, 'filedata': filedata})
        else:
            method, path, protocol = lines[0].split(" ")
            headers.update({'Method': method, 'Path': path, 'Protocol': protocol})
            for line in lines[1:]:
                if line.strip() != '':
                    key, value = line.split(': ')
                    headers[key] = value.strip()
        

        return headers

    
    def handle_request(self):
        headers = self.parse_request(self.request)
        response = ""
        if headers['Method'] == 'GET':
            response = self.do_GET()
        
        if headers['Method'] == 'POST':
            response = self.do_POST()

        if headers['Method'] == 'Webkit':
            response = self.writeData()
        return response
        
    def do_GET(self):
        with open("index.html", "r", encoding=self.FORMAT) as f:
            html = HTMLPreprocessing(f.read()).get_processed_html()
        response = ('HTTP/1.1 200 OK\r\n' 
            + 'Content-Type: text/html\r\n' 
            + 'Content-Length: {}\r\n'.format(len(html)) 
            + '\r\n' + html)
        return response
    
    def do_POST(self):
        response = "HTTP/1.1 200 OK\r\n\r\nFile uploaded successfully"
        return response
    
    def writeData(self):
        headers = self.parse_request(self.request)
        with open('./files/' + headers['filename'], "wb") as f:
            f.write(headers['filedata'].encode(self.FORMAT))        
        response = "HTTP/1.1 200 OK\r\n\r\nFile writed successfully"
        return response
    

