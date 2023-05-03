from FileManager import FileManager
from HTMLPreprocessing import HTMLPreprocessing

class HTTPRequestHandler():
    
    def __init__(self, request):
        self.request = request
        self.FORMAT = 'utf-8'
    
    def parse_request(self, request):
        headers = {}
        lines = request.split('\n')

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
            response = self.do_GET(headers)
        
        if headers['Method'] == 'POST':
            response = self.do_POST(headers)

        if headers['Method'] == 'Webkit':
            response = self.handle_webkit_request(headers)
        return response
        
    def do_GET(self, headers):
        if headers['Path'] == '/':
            with open("index.html", "r", encoding=self.FORMAT) as f:
                html = HTMLPreprocessing(f.read()).get_processed_html()
            response = ('HTTP/1.1 200 OK\r\n' 
                + 'Content-Type: text/html\r\n' 
                + 'Content-Length: {}\r\n'.format(len(html)) 
                + '\r\n' + html)
            return response
    
    def do_POST(self, headers):
        if headers['Path'] == '/upload':
            response = "HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n"
            return response
    
    def handle_webkit_request(self, headers):
        file_manager = FileManager('./files')
        file_manager.save_file_on_directory(headers['filename'], headers['filedata'])      
        response = "HTTP/1.1 200 OK\r\n\r\nFile writed successfully"
        return response
    

