from file import File

class Graph:
    def __init__(self):
        self.files = []
        self.internal = set()
        
    def __str__(self):
        return f'Graph(files={self.files})'

    def add_file(self, file_ : File):
        self.files.append(file_)
        
    def add_internal(self, internal):
        self.internal.update(internal)
        
    def to_dict(self):
        return {
            'files': self.files,
            'internal': list(self.internal)
        }