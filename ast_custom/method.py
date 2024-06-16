from ast import FunctionDef
from astunparse import unparse

class Method:
    def __init__(self, name, node : FunctionDef, internal=[], external=[], docs=""):
        self.name = name
        self.internal = internal
        self.external = external
        self.content = unparse(node)
        self.docs = docs