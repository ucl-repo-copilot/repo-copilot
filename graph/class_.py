from ast import ClassDef
from graph.method import Method
from astunparse import unparse


class Class:
    """
    Represents a class in the code.

    Attributes:
        name (str): The name of the class.
        content (str): The unparsed content of the class.
        methods (list[Method]): A list of Method objects representing the methods of the class.
        docs (str): The documentation of the class.
    """

    def __init__(self, name, assignements: dict[str, str], node: ClassDef, methods: list[Method]):
        self.name = name
        self.assignements = assignements
        self.content = unparse(node)
        self.methods = methods
        self.docs = ""
