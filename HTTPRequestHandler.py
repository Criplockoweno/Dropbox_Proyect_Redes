from HTMLPreprocessing import HTMLPreprocessing

class HTTPRequestHandler():
    
    def __init__(self, request):
        self.request = request
        self.FORMAT = 'utf-8'
    
    def parse_request(self, request):
        headers = {}
        lines = request.split('\n')
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
        return response
        
    def do_GET(self):
        with open("index.html", "r", encoding=self.FORMAT) as f:
            html = HTMLPreprocessing(f.read()).get_processed_html()
        response = ('HTTP/1.1 200 OK\r\n' 
            + 'Content-Type: text/html\r\n' 
            + 'Content-Length: {}\r\n'.format(len(html)) 
            + '\r\n' + html)
        return response
