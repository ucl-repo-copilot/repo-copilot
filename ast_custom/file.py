from class_ import Class
from method import Method

class File:
    def __init__(self, name, path, classes : list[Class], methods : list[Method]):
        self.name = name
        self.path = path
        self.classes = classes
        self.methods = methods