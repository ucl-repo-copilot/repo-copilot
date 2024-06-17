from ast import FunctionDef
from astunparse import unparse


class Method:
    """
    Represents a method in a class.

    Attributes:
        name (str): The name of the method.
        node (FunctionDef): The AST node representing the method.
        internal (list): A list of internal methods.
        external (list): A list of external methods.
        content (str): The original source code of the method.
        docs (str): The documentation for the method.
    """

    def __init__(self, name, node: FunctionDef, internal=[], external=[], docs=""):
        self.name = name
        self.internal = internal
        self.external = external
        self.content = unparse(node)
        self.docs = docs
