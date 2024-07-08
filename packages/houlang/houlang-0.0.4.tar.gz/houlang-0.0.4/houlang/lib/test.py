import unittest

from package.houlang.lib.classes import ClassMapper

class ClassMapperTest(unittest.TestCase):

    class_list_a = [
        {'label': 'a', 'type': 'foo'},
    ]

    class_list_b = [
        {'label': 'b', 'type': 'bar'},
        {'label': 'c', 'type': 'baz'},
        {'label': 'd', 'type': 'qux'},
        {'label': 'e', 'type': 'quux'},
    ]

    merge_classes = [
        'b:c',
    ]

    remove_classes = [
        'e',
    ]

    def setUp(self):
        self.cm = ClassMapper(self.class_list_a, self.merge_classes, self.remove_classes)

    def test_class_list_init(self):
        self.assertEqual(self.cm.label_l, ['a'])
        self.assertEqual(self.cm.label_type, ['foo'])

    def test_class_list_update(self):
        self.cm.update(self.class_list_b)
        self.assertEqual(self.cm.label_l, ['a', 'c', 'd'])

    def test_label_to_type(self):
        self.assertEqual(self.cm.label_to_type('a'), 'foo')

    def test_label_to_index(self):
        self.assertEqual(self.cm.label_to_index('a'), 0)

    def test_to_list(self):
        self.cm.update(self.class_list_b)
        self.assertEqual(self.cm.to_list(), [
            {'label': 'a', 'type': 'foo'},
            {'label': 'c', 'type': 'bar'},
            {'label': 'd', 'type': 'qux'},
        ])

if __name__ == '__main__':
    unittest.main()