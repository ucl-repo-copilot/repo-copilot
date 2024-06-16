from ast import ClassDef
from method import Method
from astunparse import unparse

class Class:
    def __init__(self, name, node : ClassDef, methods : list[Method]):
        self.name = name
        self.content = unparse(node)
        self.methods = methods