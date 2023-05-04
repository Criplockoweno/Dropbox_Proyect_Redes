from FileManager import FileManager
from HTMLPreprocessing import HTMLPreprocessing
import re


class HTTPRequestHandler():

    def __init__(self, request, conn):
        self.request = request
        self.conn = conn

    def handle_chunked_request(self, request, content_length):
        while content_length > 0:
            chunk = self.conn.recv(4096)
            content_length -= len(chunk)
            request += chunk
        return request

    def handle_file_request(self, request, headers):
        boundaries = '--' + \
            re.search(r'boundary=([^;\\]+)', headers['Content-Type']).group(1)
        request_body = request.split(b'\r\n\r\n', 1)[1]
        start = request_body.find(boundaries.encode('utf-8')) + len(boundaries)
        end = request_body.find(boundaries.encode('utf-8'), start)
        bh, filedata = request_body[start:end].split(b'\r\n\r\n', 1)
        bh = bh.decode('utf-8').split('\r\n')
        body_headers = {}
        for line in bh:
            if line.strip() != '':
                key, value = line.split(': ')
                body_headers[key] = value.strip()
        filename = re.search(
            r'filename=([^;\\]+)', body_headers['Content-Disposition']).group(1).replace('"', '')
        content_type = body_headers['Content-Type']
        return filename, filedata, content_type

    def parse_request(self, request):
        headers = {}
        lines = request.decode('utf-8').split('\r\n')
        method, path, protocol = lines[0].split(" ")
        headers.update({'Method': method, 'Path': path, 'Protocol': protocol})
        for line in lines[1:]:
            if line.strip() != '':
                key, value = line.split(': ')
                headers[key] = value.strip()
        if 'Content-Length' in headers:
            request = self.handle_chunked_request(
                request, int(headers['Content-Length']))
        return headers, request

    def handle_request(self):
        headers, request = self.parse_request(self.request)
        response = ""

        if headers['Method'] == 'GET':
            response = self.do_GET(headers)

        if headers['Method'] == 'POST':
            response = self.do_POST(headers, request)

        return response

    def do_GET(self, headers):
        if headers['Path'] == '/':
            with open("index.html", "r", encoding='utf-8') as f:
                html = HTMLPreprocessing(f.read()).get_processed_html()
            response = ('HTTP/1.1 200 OK\r\n'
                        + 'Content-Type: text/html\r\n'
                        + 'Content-Length: {}\r\n'.format(len(html))
                        + '\r\n' + html)
            return response

    def do_POST(self, headers, request):
        if headers['Path'] == '/upload':
            filename, filedata, content_type = self.handle_file_request(
                request, headers)
            file_manager = FileManager('./files/')
            file_manager.save_file_on_directory(
                filename, filedata, content_type)
            response = "HTTP/1.1 301 Moved Permanently\r\nLocation: / \r\n\r\n"
            return response
