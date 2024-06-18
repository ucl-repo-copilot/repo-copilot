import re

from ordered_set import OrderedSet
from graph.class_ import Class
from ast_custom.ast_parser import ASTParser
from graph.method import Method
from graph.file import File
import cache.cache as cache
from cache.element import Element

class Graph:
    """
    Represents a graph that stores relationships between files, methods, and classes.

    Attributes:
        files (list): A list of File objects representing the files in the graph.
        internal_methods (set): A set of internal method names.
        internal_classes (set): A set of internal class names.
    """

    def __init__(self):
        self.files = []
        self.internal_methods = OrderedSet()
        self.internal_classes = OrderedSet()

    def add_file(self, file_: File):
        self.files.append(file_)

    def add_internal_method(self, internal):
        self.internal_methods.update(internal)

    def add_internal_class(self, internal):
        self.internal_classes.update(internal)

    def to_dict(self):
        return {
            "files": self.files,
            "internal_methods": list(self.internal_methods),
            "internal_classes": list(self.internal_classes)
        }

    def build_relationships(self, map: dict[str, ASTParser]):
        """
        Builds the relationships between files, methods, and classes in the graph.

        Args:
            map (dict[str, FileASTParser]): A dictionary mapping file paths to FileASTParser objects.
        """
        print(f"Building relationships")

        # Iterate over all files in the graph
        for file in self.files:
            parser = map.get(file.path, {})  # Get the AST parser

            # Build relationships for all methods and classes in the file
            for method in file.methods:
                self.__build_method_relationships(method, parser)
                cache.set(f'{file.module}.{method.name}', Element(file.module, method))
            for class_ in file.classes:
                self.__build_class_method_relationships(class_, parser)
            
        print("Relationships built successfully!")

    def __build_method_relationships(self, method: Method, parser: ASTParser):
        """
        Builds the relationships for a given method that is in a module (not part of a class).

        Args:
            method (Method): The method to build relationships for.
            parser (FileASTParser): The AST parser for the file containing the method.
        """
        module_name = parser.module_name
        caller = f"{module_name}.{method.name}"
        # Find all callees (methods being called within) for the method
        for callee in parser.method_calls.get(caller, []):
            # If the callee is a method of the same class, replace self with module name
            if callee.startswith('self.'):
                callee = callee.replace('self.', f'{module_name}.')

            # Save to internal/external
            if self.__is_internal(callee, parser.imports):
                method.internal.append(callee)
            else:
                method.external.append(callee)

    def __build_class_method_relationships(self, class_: Class, parser: ASTParser):
        """
        Builds the relationships for all methods in a given class.

        Args:
            class_ (Class): The class to build relationships for.
            parser (FileASTParser): The AST parser for the file containing the class.
        """
        for method in class_.methods:
            caller = f"{class_.name}.{method.name}"
            cache.set(caller, Element(class_.name, method))
            for callee in parser.method_calls.get(caller, []):
                if re.match(r'self\..*\..*', callee):  # self.obj.method
                    callee = callee.replace('self.', '')
                    variable = callee.split('.')[0]
                    if variable in parser.assigns:  # Replace variable with value from assignements
                        callee = callee.replace(
                            variable, parser.assigns[variable])
                    else:
                        AttributeError(
                            f"Variable {variable} not found in assigns!")
                elif callee.startswith('self.'):
                    callee = callee.replace('self.', f'{class_.name}.')

                # Save to internal/external
                if self.__is_internal(callee, parser.imports):
                    method.internal.append(callee)
                else:
                    method.external.append(callee)

    def __is_internal(self, method_name: str, imports: dict[str, list[str]] = {}) -> bool:
        """
        Args:
            method_name (str): The name of the method.
            imports (dict[str, list[str]]): A dictionary mapping imported method names to imported modules.

        Returns:
            bool: True if the method is internal, False otherwise.

        1. Check if the method is in the internal methods
        2. Check if there is an import for an internal class
        3. Check if there is an import for an internal method, in the form of class.method
        """
        imported_from = imports.get(method_name, None)
        return method_name in self.internal_methods \
            or (imported_from is not None and imported_from in self.internal_classes) \
            or (imported_from is not None and f'{imported_from}.{method_name}' in self.internal_methods)
