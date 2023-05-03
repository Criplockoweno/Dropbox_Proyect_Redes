from base64 import b64encode
import os
import time

class FileManager():
    def __init__(self, directory):
        self.directory = directory
    
    def get_file_data(self, filename):
        path = os.path.join(self.directory, filename)
        size = self.get_file_size_str(os.path.getsize(path))
        date = time.ctime(os.path.getctime(path))
        return path, size, date
    
    def encode_file_content(self, file_path):
        with open(file_path, 'rb') as f:
            content = f.read()
            encoded_content = b64encode(content).decode('utf-8')
        return encoded_content
    
    def get_files_on_directory(self):
        return [filename for filename in os.listdir(self.directory)]
    
    def get_file_size_str(self, size_bytes):
        units = ('B', 'KB', 'MB', 'GB')
        size_thresholds = (1, 1024, 1024**2, 1024**3)

        for i, threshold in enumerate(size_thresholds):
            if size_bytes < threshold:
                size = size_bytes / size_thresholds[i-1]
                unit = units[i-1]
                break
        else:
            size = size_bytes / size_thresholds[-1]
            unit = units[-1]
            
        size_str = f"{size:.1f} {unit}"
        return size_str
    
    def save_file_on_directory(self, file_name, file_data):
        with open(os.path.join(self.directory, file_name), "wb") as f:
            f.write(file_data.encode('utf-8'))  