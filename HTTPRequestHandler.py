from FileManager import FileManager
from HTMLPreprocessing import HTMLPreprocessing
from os.path import exists, getsize
from urllib.parse import unquote
import re


class HTTPRequestHandler():
    saveFolder = './files/'

    def __init__(self, request, conn):
        self.request = request
        self.conn = conn
        self.FORMAT = 'UTF-8'

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
        print(headers['Method'])
        if headers['Method'] == 'GET':
            response = self.do_GET(headers['Path'])

        if headers['Method'] == 'POST':
            response = self.do_POST(headers, request)
            # response = self.writeData()

        if headers['Method'] == 'Webkit':
            response = self.writeData()
        return response

    def do_GET(self, path):
        print('Path: ' + path)
        if path == '/':
            with open("index.html", "r", encoding=self.FORMAT) as f:
                html = HTMLPreprocessing(f.read()).get_processed_html()
            response = ('HTTP/1.1 200 OK\r\n'
                        + 'Content-Type: text/html\r\n'
                        + 'Content-Length: {}\r\n'.format(len(html))
                        + '\r\n' + html)
        else:
            fileName = unquote(path[1:])
            fileName = self.saveFolder + fileName
            print(fileName)
            if exists(fileName):
                with open(fileName, 'rb') as file:
                    binary_file = file.read()
                    print(type(binary_file))
                    print('Lenght file: {}'.format(getsize(fileName)))
                    print('Lenght binary: {}'.format(len(binary_file)))
                    response = ('HTTP/1.1 200 OK\r\n'
                                + 'Content-Type: application/octet-stream\r\n'
                                + 'Content-Length: {}\r\n'.format(len(binary_file))
                                + '\r\n')
                    response = bytes(response, 'UTF-8') + binary_file
                    # print(response.decode('UTF-8'))
                    file.close()
            else:
                response = ('HTTP/1.1 404 NOT FOUND\r\n'
                            + 'Content-Type: text/html\r\n'
                            + 'Content-Length: {}\r\n'.format(len('Not found ' + fileName))
                            + '\r\n' + 'Not found ' + fileName)

        return response

    def writeData(self):
        headers = self.parse_request(self.request)
        with open(self.saveFolder + headers['filename'], "wb") as f:
            f.write(headers['filedata'].encode(self.FORMAT))
        response = "HTTP/1.1 200 OK\r\n\r\nFile writed successfully"
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
