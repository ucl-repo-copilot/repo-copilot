from graph.method import Method


class Element:
    def __init__(self, class_name: str, method: Method):
        self.class_name = class_name
        self.method = method

    # TODO: Store path to the file
    def get_file_name(self):
        return self.file_name

    def get_class_name(self):
        return self.class_name

    def get_method(self):
        return self.method
