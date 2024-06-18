import unittest

from graph.file import File
from graph.graph_manager import build_graph


class TestSimpleProject(unittest.TestCase):

    def test_simple_project(self):
        graph = build_graph('./program_examples/users')
        self.assertIsNotNone(graph)

        files = graph.files
        self.assertEqual(len(files), 5)

        internal_methods = list(graph.internal_methods)
        self.assertCountEqual(internal_methods, ['DataProcessor.process_data', 
                                                 'DataProcessor.check_emails',
                                                 'DataProcessor',
                                                 'main.main', 
                                                #  'main.__name__',
                                                 'User',
                                                 'User.__init__', 
                                                 'User.__str__', 
                                                 'User.update_email',
                                                 'utils.validate_email'])

        internal_classes = list(graph.internal_classes)
        self.assertCountEqual(internal_classes, ['DataProcessor', 'User'])

        # Check a.py
        while files:
            file = files.pop()
            match file.name:
                case '__init__.py': pass
                case 'data_processor.py': self.validate_data_processor(file)
                case 'main.py': self.validate_main(file)
                case 'user.py': self.validate_user(file)
                case 'utils.py': self.validate_utils(file)
                case _: AttributeError(f"Unexpected file: {file.name}")
        pass

    def validate_data_processor(self, file: File):
        self.assertEqual(file.name, 'data_processor.py')
        self.assertEqual(file.module, 'data_processor')
        self.assertEqual(file.path, 'data_processor.py')
        self.assertEqual(file.imports, {'validate_email': 'utils'})

        classes = file.classes
        self.assertEqual(len(classes), 1)
        a = classes[0]
        self.assertEqual(a.name, 'DataProcessor')

        methods = a.methods
        self.assertEqual(len(methods), 2)

        process_data = methods[0]
        self.assertEqual(process_data.name, 'process_data')
        self.assertCountEqual(process_data.internal, [])
        self.assertCountEqual(process_data.external, ['upper'])

        check_emails = methods[1]
        self.assertEqual(check_emails.name, 'check_emails')
        self.assertCountEqual(check_emails.internal, ['utils.validate_email'])
        self.assertCountEqual(check_emails.external, [])

        module_methods = file.methods
        self.assertEqual(len(module_methods), 0)

    def validate_main(self, file: File):
        self.assertEqual(file.name, 'main.py')
        self.assertEqual(file.module, 'main')
        self.assertEqual(file.path, 'main.py')
        self.assertEqual(
            file.imports, {'User': 'user', 'DataProcessor': 'data_processor'})

        classes = file.classes
        self.assertEqual(len(classes), 0)

        module_methods = file.methods
        self.assertEqual(len(module_methods), 1)
        main = module_methods[0]
        self.assertEqual(main.name, 'main')
        self.assertCountEqual(
            main.internal, ['User', 'DataProcessor', 'DataProcessor.process_data'])
        self.assertCountEqual(main.external, ['print'])

    def validate_user(self, file: File):
        self.assertEqual(file.name, 'user.py')
        self.assertEqual(file.module, 'user')
        self.assertEqual(file.path, 'user.py')
        self.assertEqual(file.imports, {'uuid' : None})

        classes = file.classes
        self.assertEqual(len(classes), 1)
        User = classes[0]
        self.assertEqual(User.name, 'User')
        self.assertEqual(User.assignements, {'id': 'uuid.uuid4'})

        methods = User.methods
        self.assertEqual(len(methods), 3)

        init_method = methods[0]
        self.assertEqual(init_method.name, '__init__')
        self.assertCountEqual(init_method.internal, [])
        self.assertCountEqual(init_method.external, ['uuid.uuid4'])

        str_method = methods[1]
        self.assertEqual(str_method.name, '__str__')
        self.assertCountEqual(str_method.internal, [])
        self.assertCountEqual(str_method.external, [])

        update_email = methods[2]
        self.assertEqual(update_email.name, 'update_email')
        self.assertCountEqual(update_email.internal, [])
        self.assertCountEqual(update_email.external, [])

        module_methods = file.methods
        self.assertEqual(len(module_methods), 0)

    def validate_utils(self, file: File):
        self.assertEqual(file.name, 'utils.py')
        self.assertEqual(file.module, 'utils')
        self.assertEqual(file.path, 'utils.py')
        self.assertEqual(file.imports, {'re' : None})

        classes = file.classes
        self.assertEqual(len(classes), 0)

        module_methods = file.methods
        self.assertEqual(len(module_methods), 1)
        validate_email = module_methods[0]
        self.assertEqual(validate_email.name, 'validate_email')
        self.assertCountEqual(validate_email.internal, [])
        self.assertCountEqual(validate_email.external, ['re.match'])


if __name__ == '__main__':
    unittest.main()
