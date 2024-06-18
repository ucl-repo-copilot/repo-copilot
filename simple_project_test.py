import unittest

from graph.file import File
from graph.graph_manager import build_graph


class TestSimpleProject(unittest.TestCase):

    def test_simple_project(self):
        graph = build_graph('./program_examples/simple')
        self.assertIsNotNone(graph)

        files = graph.files
        self.assertEqual(len(files), 3)

        internal_methods = list(graph.internal_methods)
        self.assertCountEqual(internal_methods, ['A', 'A.methodA1', 'A.methodA2', 'a.methodA3',
                                                 'B', 'B.__init__', 'B.methodB1', 'B.methodB2',
                                                 'C', 'C.__init__', 'C.methodC1', 'C.methodC2', 'c.methodC3'])

        internal_classes = list(graph.internal_classes)
        self.assertCountEqual(internal_classes, ['A', 'B', 'C'])

        # Check a.py
        while files:
            file = files.pop()
            match file.name:
                case 'a.py': self.validate_a(file)
                case 'b.py': self.validate_b(file)
                case 'c.py': self.validate_c(file)
                case _: AttributeError(f"Unexpected file: {file.name}")
        pass

    def validate_a(self, file: File):
        self.assertEqual(file.name, 'a.py')
        self.assertEqual(file.module, 'a')
        self.assertEqual(file.path, 'a.py')
        self.assertEqual(file.imports, {'uuid4': 'uuid'})

        classes = file.classes
        self.assertEqual(len(classes), 1)
        a = classes[0]
        self.assertEqual(a.name, 'A')

        methods = a.methods
        self.assertEqual(len(methods), 2)

        method_a1 = methods[0]
        self.assertEqual(method_a1.name, 'methodA1')
        self.assertCountEqual(method_a1.internal, [])
        self.assertCountEqual(method_a1.external, ['str', 'print', 'uuid4'])

        method_a2 = methods[1]
        self.assertEqual(method_a2.name, 'methodA2')
        self.assertCountEqual(method_a2.internal, ['A.methodA1'])
        self.assertCountEqual(method_a2.external, [])

        module_methods = file.methods
        self.assertEqual(len(module_methods), 1)
        method_a3 = module_methods[0]
        self.assertEqual(method_a3.name, 'methodA3')
        self.assertCountEqual(method_a3.internal, [])
        self.assertCountEqual(method_a3.external, ['print'])

    def validate_b(self, file: File):
        self.assertEqual(file.name, 'b.py')
        self.assertEqual(file.module, 'b')
        self.assertEqual(file.path, 'b.py')
        self.assertEqual(
            file.imports, {'re': None, 'uuid': None, 'A': 'a', 'methodA3': 'a'})

        classes = file.classes
        self.assertEqual(len(classes), 1)
        b = classes[0]
        self.assertEqual(b.name, 'B')
        self.assertEqual(b.assignements, {'a': 'A'})

        methods = b.methods
        self.assertEqual(len(methods), 3)

        init_method = methods[0]
        self.assertEqual(init_method.name, '__init__')
        self.assertCountEqual(init_method.internal, ['A'])
        self.assertCountEqual(init_method.external, [])

        method_b1 = methods[1]
        self.assertEqual(method_b1.name, 'methodB1')
        self.assertCountEqual(method_b1.internal, ['A.methodA1'])
        self.assertCountEqual(method_b1.external, ['print'])

        method_b2 = methods[2]
        self.assertEqual(method_b2.name, 'methodB2')
        self.assertCountEqual(method_b2.internal, ['methodA3'])
        self.assertCountEqual(method_b2.external, [
                              'str', 're.compile', 'print', 'uuid.uuid4'])

    def validate_c(self, file: File):
        self.assertEqual(file.name, 'c.py')
        self.assertEqual(file.module, 'c')
        self.assertEqual(file.path, 'api/c.py')
        self.assertEqual(file.imports, {'A': 'a', 'B': 'b'})

        classes = file.classes
        self.assertEqual(len(classes), 1)
        c = classes[0]
        self.assertEqual(c.name, 'C')
        self.assertEqual(c.assignements, {'a': 'A', 'b': 'B'})

        methods = c.methods
        self.assertEqual(len(methods), 3)

        init_method = methods[0]
        self.assertEqual(init_method.name, '__init__')
        self.assertCountEqual(init_method.internal, ['A', 'B'])
        self.assertCountEqual(init_method.external, [])

        method_c1 = methods[1]
        self.assertEqual(method_c1.name, 'methodC1')
        self.assertCountEqual(method_c1.internal, ['A.methodA1', 'B.methodB1'])
        self.assertCountEqual(method_c1.external, ['print'])

        method_c2 = methods[2]
        self.assertEqual(method_c2.name, 'methodC2')
        self.assertCountEqual(method_c2.internal, ['A.methodA2', 'B.methodB2'])
        self.assertCountEqual(method_c2.external, ['print'])

        module_methods = file.methods
        self.assertEqual(len(module_methods), 1)
        method_c3 = module_methods[0]
        self.assertEqual(method_c3.name, 'methodC3')
        self.assertCountEqual(method_c3.internal, [])
        self.assertCountEqual(method_c3.external, ['print'])


if __name__ == '__main__':
    unittest.main()
