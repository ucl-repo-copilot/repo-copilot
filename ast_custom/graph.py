import re
from file_ast_parser import FileASTParser
from file import File

class Graph:
    def __init__(self):
        self.files = []
        self.internal_methods = set()
        self.internal_classes = set()
        
    def __str__(self):
        return f'Graph(files={self.files})'

    def add_file(self, file_ : File):
        self.files.append(file_)
        
    def add_internal_method(self, internal):
        self.internal_methods.update(internal)
        
    def add_internal_class(self, internal):
        self.internal_classes.update(internal)
        
    def to_dict(self):
        return {
            'files': self.files,
            'internal_methods': list(self.internal_methods),
            'internal_classes': list(self.internal_classes)
        }
        
    # map = {file_path: {parser}}
    def build_relationships(self, map : dict[str, FileASTParser]):
        print(f"Internal Methods: {self.internal_methods} ({len(self.internal_methods)})")
        print(f"Internal Classes: {self.internal_classes} ({len(self.internal_classes)})")
        
        for file in self.files:
            parser = map.get(file.path, {})
            method_calls = parser.method_calls
            assigns = parser.assigns
            imports = parser.imports
            
            print(f'Method calls: {method_calls}')
            print(f'Assignements: {assigns}')
            print(f'Imports: {imports}')
            print()
            for method in file.methods:
                module_name = parser.module_name
                caller = f"{module_name}.{method.name}"
                callees = []
                for callee in parser.method_calls.get(caller, []):
                    if callee.startswith('self.'):
                        callees.append(callee.replace('self.', f'{module_name}.'))
                    else:
                        callees.append(callee)
                        
                method.internal = [callee for callee in callees if self.__is_internal(callee, imports)]
                method.external = [callee for callee in callees if self.__is_external(callee, imports)]
                print(f">Method: {caller}, Internal: {method.internal}, External: {method.external}")
            for class_ in file.classes:
                for method in class_.methods:
                    caller = f"{class_.name}.{method.name}"
                    callees = []
                    for callee in parser.method_calls.get(caller, []):
                        if re.match(r'self\..*\..*', callee): # self.obj.method
                            callee = callee.replace('self.', '')
                            variable = callee.split('.')[0]
                            if variable in parser.assigns:
                                callees.append(callee.replace(variable, parser.assigns[variable]))
                            else:
                                AttributeError(f"Variable {variable} not found in assigns!")
                        elif callee.startswith('self.'):
                           callees.append(callee.replace('self.', f'{class_.name}.'))         
                        else:
                            callees.append(callee)          
                    
                    # print(f"Method: {caller}, Callees: {callees}")
                    method.internal = [callee for callee in callees if self.__is_internal(callee, imports)]
                    method.external = [callee for callee in callees if self.__is_external(callee, imports)]
                    print(f">Method: {caller}, Internal: {method.internal}, External: {method.external}")
            
            print()
            
    def __is_internal(self, method_name : str, imports : dict[str, list[str]] = {}):
        imported_from = None if method_name not in imports else imports[method_name]
        return method_name in self.internal_methods \
            or (imported_from is not None and imported_from in self.internal_classes) \
            or (imported_from is not None and f'{imported_from}.{method_name}' in self.internal_methods)
    
    def __is_external(self, method_name : str, imports : dict[str, list[str]] = {}):
        return not self.__is_internal(method_name, imports)
                 