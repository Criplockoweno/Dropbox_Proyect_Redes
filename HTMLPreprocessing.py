from bs4 import BeautifulSoup
from FileManager import FileManager
import base64


class HTMLPreprocessing:

    def __init__(self, html):
        self.html = html

    def get_processed_html(self):
        return self.process_html()

    def encode_file_content(self, file_path):
        with open(file_path, 'rb') as f:
            content = f.read()
            encoded_content = base64.b64encode(content).decode('utf-8')
        return encoded_content

    def process_html(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        file_manager = FileManager('./files')
        for filename in file_manager.get_files_on_directory():
            path, size, date = file_manager.get_file_data(filename)
            encoded_content = self.encode_file_content(path)
            list_file_html = self.get_file_html(
                filename, size, encoded_content, date)
            file_list_container = soup.find('div', {'id': 'filesList'})
            file_list_container.append(
                BeautifulSoup(list_file_html, 'html.parser'))
        return soup.prettify(formatter="html")

    def get_file_html(self, file_name: str, size: str, encoded_content: str, submission_date: str):
        return f"""<div class="card my-2">
                    <div class="card-body d-flex justify-content-between align-items-center">
                        <p class="card-text my-0">{file_name}</p>
                        <a class="my-0" target="_blank" href="/{file_name}">
                            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-file-arrow-down-fill" viewBox="0 0 16 16">
                                <path d="M12 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2zM8 5a.5.5 0 0 1 .5.5v3.793l1.146-1.147a.5.5 0 0 1 .708.708l-2 2a.5.5 0 0 1-.708 0l-2-2a.5.5 0 1 1 .708-.708L7.5 9.293V5.5A.5.5 0 0 1 8 5z"/>
                            </svg>
                        </a>
                    </div>
                    <div class="card-footer d-flex justify-content-between text-body-secondary">
                        <p class="mb-0">{size}</p>
                        <p class="mb-0">Submitted on {submission_date}</p>
                    </div>
                </div>"""
