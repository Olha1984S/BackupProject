class CopyFileError(Exception):

    def __init__(self, file_path, original_error):
        self.file_path = file_path
        self.original_error = original_error