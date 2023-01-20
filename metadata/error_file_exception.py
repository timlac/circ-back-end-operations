class ErrorFileException(Exception):
    def __init__(self, filename, message="\nFilename {} contains error marker, skipping file"):
        self.filename = filename
        self.message = message
        super().__init__(self.message.format(self.filename))