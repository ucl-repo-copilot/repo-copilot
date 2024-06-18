from datetime import datetime
import re
import os
import json

from ast_custom.ast_parser import ASTParser
from graph.graph import Graph
from graph.graph_encoder import GraphEncoder
from graph.method import Method
from graph.class_ import Class
from graph.file import File


def save_graph_to_json(graph):
    time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    path = f'./graph/output/{time}.json'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as file:
        json.dump(graph.to_dict(), file, cls=GraphEncoder, indent=4)


def build_graph(root_folder, exclude_dirs_regex=r'env') -> Graph:
    print(f'Building graph for {root_folder}')
    graph = Graph()
    map = {}  # {file_path: {method_name: [calls]}}

    # 1. Find all files in the root folder
    for file_path in __get_python_files_in_dir(root_folder, exclude_dirs_regex):
        # 2. Parse each file
        parsed = ASTParser(file_path)

        # 3. Add internal calls to the graph, will be used to find external methods
        graph.add_internal_method(parsed.internal_calls)
        graph.add_internal_class([class_.name for class_ in parsed.classes])

        # 4. Store the method calls for each file (used for building relationships between functions)
        relative_path = os.path.relpath(
            file_path, root_folder).replace(os.sep, '/')
        map[relative_path] = parsed

        # 4. Build the classes
        classes = []
        for class_node, class_methods in parsed.classes.items():  # Iterate over ClassDef nodes
            methods = []
            for method in class_methods:  # Iterate over FunctionDef nodes
                methods.append(Method(method.name, node=method,
                               internal=[], external=[]))

            classes.append(Class(name=class_node.name,
                                 assignements=parsed.assigns,
                                 node=class_node,
                                 methods=methods))

        # 5. Build the methods
        methods = []
        for method in parsed.methods:
            methods.append(Method(name=method.name, node=method,
                           internal=[], external=[]))

        # 6. Add the file to the graph
        graph.add_file(File(name=os.path.basename(file_path),
                            path=relative_path,
                            imports=parsed.imports,
                            classes=classes,
                            methods=methods))

    print(f'Graph built successfully!')
    graph.build_relationships(map)
    return graph


def __get_python_files_in_dir(directory, exclude_dirs_regex=r'env'):
    python_files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        dirnames[:] = [d for d in dirnames if not re.search(
            exclude_dirs_regex, d)]
        for filename in filenames:
            if filename.endswith('.py'):
                python_files.append(os.path.join(dirpath, filename))
    return python_files
