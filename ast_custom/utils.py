import re, os, json

from graph_encoder import GraphEncoder
import graph
from file_ast_parser import FileASTParser
from method import Method
from class_ import Class
from file import File
from graph import Graph

def build_graph_and_relationships(root_folder, exclude_dirs_regex=r'env'):
    graph = build_graph(root_folder, exclude_dirs_regex)
    graph.build_relationships()
    return graph

def build_graph(root_folder, exclude_dirs_regex=r'env') -> Graph:
    graph = Graph()
    map = {} # {file_path: {method_name: [calls]}}
    
    # 1. Find all files in the root folder
    for file_path in __get_python_files_in_dir(root_folder, exclude_dirs_regex):
        # 2. Parse each file
        parsed = FileASTParser(file_path)
        
        # 3. Add internal calls to the graph, will be used to find external methods
        graph.add_internal_method(parsed.internal_calls)
        graph.add_internal_class([class_.name for class_ in parsed.classes])
        
        # 4. Store the method calls for each file (used for building relationships between functions)
        relative_path = os.path.relpath(file_path, root_folder).replace(os.sep, '/')
        map[relative_path] = parsed
        
        # print(parsed.method_calls)

        # 4. Build the classes
        classes = []
        for class_node, class_methods in parsed.classes.items(): # Iterate over ClassDef nodes
            methods = []
            for method in class_methods: # Iterate over FunctionDef nodes
                # method_name = f"{class_node.name}.{method.name}"
                # calls = parsed.method_calls.get(f"{class_node.name}.{method.name}", {})
                # print(f"Method: {method_name}, Calls: {calls}")
                methods.append(Method(method.name, node=method, internal=[], external=[]))
            classes.append(Class(name=class_node.name, node=class_node, methods=methods))

        # 5. Build the methods
        methods = []
        for method in parsed.methods:
            # method_name = f"{parsed.module_name}.{method.name}"
            # calls = parsed.method_calls.get(method_name, [])
            # print(f"Method: {method_name}, Calls: {calls}")
            methods.append(Method(name=method.name, node=method, internal=[], external=[]))

        # 6. Add the file to the graph
        graph.add_file(File(name=os.path.basename(file_path), path=relative_path, classes=classes, methods=methods))
        # print()
    
    graph.build_relationships(map)
    return graph    

def __get_python_files_in_dir(directory, exclude_dirs_regex=r'env'):
    python_files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        dirnames[:] = [d for d in dirnames if not re.search(exclude_dirs_regex, d)]
        for filename in filenames:
            if filename.endswith('.py'):
                python_files.append(os.path.join(dirpath, filename))
    return python_files

graph = build_graph('c:/Coding/repo-copilot/ast_custom/example')
with open('graph.json', 'w') as file:
    json.dump(graph, file, cls=GraphEncoder, indent=4)