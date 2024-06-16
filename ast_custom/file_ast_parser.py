import ast
import os

class FileASTParser:
    def __init__(self, path):
        print(f"FileASTParser: {path}")
        self.path = path
        self.filename = os.path.basename(path).replace('.py', '')
        self.methods = set()  # Method of the file (not belonging to class) [methods1, methods2, ...]
        self.classes = {}  # {"class_node": [methods1, methods2, ...], ...}
        self.method_calls = {}  # All method relationships {"method_name": ["methods1", "methods2"], ...}
        self.visited = set()
        self.calls = set()
        self.__parse()

    def __parse(self):
        with open(self.path, 'r') as file:  
            tree = ast.parse(file.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                self.__visit_class(node)
            elif isinstance(node, ast.FunctionDef):
                self.__visit_method(node)

    def __visit_class(self, node : ast.ClassDef):
        self.classes[node] = self.__get_method_nodes(node)
        for method in self.classes[node]:
            self.__visit_method(method, node)
        self.calls.add(node.name) # Add class name to the calls, i.e. A()
            
    def __visit_method(self, node : ast.FunctionDef, parent=None):
        if node in self.visited: return
        if parent is None:
            self.methods.add(node)
        
        name = f"{parent.name}.{node.name}" if parent is not None else f"{self.filename}.{node.name}"
        self.method_calls[name] = set()
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                self.__visit_call(child, name)
        self.visited.add(node)
        self.calls.add(name) # Add method name to the calls, i.e. A.method1()
          
    def __visit_call(self, node : ast.Call, name : str):
        if isinstance(node.func, ast.Name):
            self.method_calls[name].add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            self.method_calls[name].add(node.func.attr)
        
    def __get_method_nodes(self, class_ : ast.ClassDef) -> list[ast.FunctionDef]:
        return [node for node in class_.body if isinstance(node, ast.FunctionDef)]