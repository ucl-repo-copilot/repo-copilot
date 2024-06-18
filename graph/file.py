from graph.class_ import Class
from graph.method import Method


class File:
    """
    Represents a file in a code repository.

    Attributes:
        name (str): The name of the file. (e.g. file.py)
        path (str): The path to the file. (e.g. /api/users/service.py)
        classes (list[Class]): A list of Class objects defined in the file.
        methods (list[Method]): A list of Method objects defined in the file.
    """

    def __init__(self, name, path, imports: dict[str, str], classes: list[Class], methods: list[Method]):
        self.name = name
        self.module = name.split('.')[0]
        self.path = path
        self.imports = imports
        self.classes = classes
        self.methods = methods
