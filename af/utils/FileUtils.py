import os

class FileUtils:

        def __init__(self):
            pass

        @staticmethod
        def get_file_name(file_path):
            return os.path.splitext(os.path.basename(file_path))[0]
        
        @staticmethod
        def get_file_directory(file_path):
            return os.path.dirname(file_path)

