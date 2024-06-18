import ast
import os
import astpretty
from ordered_set import OrderedSet

# TODO: Not sure how to deal with user = User(), user = factory.getFactory().getUser(), etc. etc.
# TODO: Handle scoped assignments, i.e. self.x = y, self.x = self.y, etc.
# TODO: Finish Users project test

class ASTParser:
    def __init__(self, path):
        basename = os.path.basename(path)
        self.path = path
        self.module_name = basename.replace('.py', '')
        # Method of the file (not belonging to class) [methods1, methods2, ...]
        self.methods = OrderedSet()
        self.classes = {}  # {"class_node": [methods1, methods2, ...], ...}
        # All method relationships {"method_name": ["methods1", "methods2"], ...}
        self.method_calls = {}
        self.visited = set()
        self.internal_calls = OrderedSet()
        self.assigns = {}
        self.imports = {}
        self.tree = None
        self.__parse()

    def print_ast(self):
        astpretty.pprint(self.tree)

    def __parse(self):
        with open(self.path, 'r') as file:
            self.tree = ast.parse(file.read())

        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                self.__visit_class(node)
            elif isinstance(node, ast.FunctionDef):
                self.__visit_method(node)
            elif isinstance(node, ast.Import):
                self.__visit_import(node)
            elif isinstance(node, ast.ImportFrom):
                self.__visit_import_from(node)

    def __visit_class(self, node: ast.ClassDef):
        self.classes[node] = self.__get_method_nodes(node)
        for method in self.classes[node]:
            self.__visit_method(method, node)
        # Add class name to the calls, i.e. A()
        self.internal_calls.add(node.name)

    def __visit_method(self, node: ast.FunctionDef, parent=None):
        if node in self.visited:
            return
        if parent is None:
            self.methods.add(node)

        scope_assignements = {}

        name = f"{parent.name}.{node.name}" if parent is not None else f"{
            self.module_name}.{node.name}"
        self.method_calls[name] = OrderedSet()
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                self.__visit_call(child, name, scope_assignements)
            elif isinstance(child, ast.Assign) and node.name == "__init__":
                self.__visit_init_assign(child)
            elif isinstance(child, ast.Assign):
                self.__visit_scoped_assign(child, scope_assignements)
                
        self.visited.add(node)
        # Add method name to the calls, i.e. A.method1()
        self.internal_calls.add(name)

    def __visit_call(self, node: ast.Call, name: str, scope_assignements={}):
        if isinstance(node.func, ast.Name):
            self.method_calls[name].add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            value = node.func.value
            attribute = node.func.attr

            if isinstance(value, ast.Name):
                self.method_calls[name].add(f"{value.id}.{attribute}")
                # self.method_calls[name].add(f".{value.id}.{attribute}") # self.method1()
            elif isinstance(value, ast.Attribute):
                self.method_calls[name].add(f"{value.value.id}.{value.attr}.{attribute}")  # A.method1.method2()
                # self.method_calls[name].add(f"{value.attr}.{attribute}")
            elif isinstance(value, ast.Call):
                self.method_calls[name].add(
                    f"{value.func.id}.{attribute}")  # A().method1()
            else:
                self.method_calls[name].add(attribute)  # method1()

    def __visit_init_assign(self, node: ast.Assign):
        key = node.targets[0].attr if isinstance(node.targets[0], ast.Attribute) else node.targets[0].id
        value = node.value
        
        if isinstance(value, ast.Name) or isinstance(value, ast.Attribute):
            return # Skip any assignments of the form x = y
        
        if isinstance(value, ast.Call) and isinstance(value.func, ast.Attribute):
            self.assigns[key] = f'{node.value.func.value.id}.{node.value.func.attr}'
        elif isinstance(value, ast.Call) and isinstance(value.func, ast.Name):
            self.assigns[key] = value.func.id
        else:
            AttributeError(f"Unexpected assignment: {node}")

    def __visit_scoped_assign(self, node: ast.Assign, scope_assignements: dict):
        key = node.targets[0].attr if isinstance(node.targets[0], ast.Attribute) else node.targets[0].id
        value = node.value
        
        if isinstance(value, ast.Name) or isinstance(value, ast.Attribute):
            return # Skip any assignments of the form x = y
        if isinstance(value, ast.Call) and isinstance(value.func, ast.Attribute):
            scope_assignements[key] = f'{node.value.func.value.id}.{node.value.func.attr}'
        elif isinstance(value, ast.Call) and isinstance(value.func, ast.Name):
            scope_assignements[key] = value.func.id
        else:
            AttributeError(f"Unexpected assignment: {node}")
            

    def __visit_import(self, node: ast.Import):
        for alias in node.names:
            self.imports[alias.name] = alias.asname

    def __visit_import_from(self, node: ast.ImportFrom):
        module = node.module.split('.')[-1]
        for alias in node.names:
            self.imports[alias.asname if alias.asname is not None else alias.name] = module

    def __get_method_nodes(self, class_: ast.ClassDef) -> list[ast.FunctionDef]:
        return [node for node in class_.body if isinstance(node, ast.FunctionDef)]
    
    
