from .parser import ParserMultiDimensional
from django.test import tag
from lib.test import BaseTest


class Parser(BaseTest):

    def setUp(self):
        self.parser = ParserMultiDimensional("")

    def test_split(self):
        key = self.parser.split_key("langs[0][id]")
        self.assertEqual(['langs', '[0]', '[id]'], key)
        key = self.parser.split_key("langs[][id]")
        self.assertEqual(['langs', '[]', '[id]'], key)
        key = self.parser.split_key("langs[][id][0000][lengh]")
        self.assertEqual(['langs', '[]', '[id]', '[0000]', '[lengh]'], key)
        key = self.parser.split_key("langs[][id][0000]lengh")
        self.assertEqual(['langs', '[]', '[id]', '[0000]', 'lengh'], key)
        key = self.parser.split_key("langs[]element")
        self.assertEqual(['langs', '[]', 'element'], key)

    def test_split_space(self):
        key = self.parser.split_key("    langs        [0]   [id]      ")
        self.assertEqual(['langs', '[0]', '[id]'], key)
        key = self.parser.split_key("    langs        [0        ]   [        id]      ")
        self.assertEqual(['langs', '[0]', '[id]'], key)
        key = self.parser.split_key("    langs        [       0    ]   [   id   ]      ")
        self.assertEqual(['langs', '[0]', '[id]'], key)
        key = self.parser.split_key("    langs        [  0]       ")
        self.assertEqual(['langs', '[0]'], key)
        key = self.parser.split_key("    langs        [  ]       ")
        self.assertEqual(['langs', '[]'], key)
        key = self.parser.split_key("    langs        [  ]    [       ]   ")
        self.assertEqual(['langs', '[]', '[]'], key)
        key = self.parser.split_key("    langs        [ lo lo ]    [   op op    op   ]   ")
        self.assertEqual(['langs', '[lolo]', '[opopop]'], key)

    def test_valid_key(self):
        self.assertTrue(self.parser.valid_key("    langs        [0]   [id]      "))
        self.assertTrue(self.parser.valid_key("    langs        [   0]   [id]      "))
        self.assertTrue(self.parser.valid_key("    langs   [0 ]   [  id  ]      "))
        self.assertTrue(self.parser.valid_key("    langs   [0 ]   [  id  ][ loloolo ]      "))
        self.assertTrue(self.parser.valid_key("    langs   [0 ]   "))
        self.assertTrue(self.parser.valid_key("    langs     "))
        self.assertTrue(self.parser.valid_key("    l     "))
        self.assertTrue(self.parser.valid_key("    l[l][l]     "))

    def test_invalid_key(self):
        self.assertFalse(self.parser.valid_key("    l[l [l]     "))
        self.assertFalse(self.parser.valid_key("    l[l l]]     "))
        self.assertFalse(self.parser.valid_key("    [l] [l]     "))
        self.assertFalse(self.parser.valid_key("    [ ]     "))
        self.assertFalse(self.parser.valid_key("    [d  ] loll     "))
        self.assertFalse(self.parser.valid_key("  lolo  [d  ] loll     "))
        self.assertFalse(self.parser.valid_key("  lolo [     "))
        self.assertFalse(self.parser.valid_key("  lolo ]     "))
        self.assertFalse(self.parser.valid_key("  lolo[ l{ ]     "))
        self.assertFalse(self.parser.valid_key("  lolo[ 4lolo ]     "))
        self.assertFalse(self.parser.valid_key("  lolo[ 4lolo ]     "))
        self.assertFalse(self.parser.valid_key("  lolo[ 4lolo ]     "))
        self.assertFalse(self.parser.valid_key("  lolo[ 4lolo ]     "))
        self.assertFalse(self.parser.valid_key("  lolo[ 4lolo ]    [ "))
        self.assertFalse(self.parser.valid_key("  lolo[ 4lolo ] [[]]     "))
        self.assertFalse(self.parser.valid_key("      "))
        self.assertFalse(self.parser.valid_key("  3443343    "))
        self.assertFalse(self.parser.valid_key("  fwe [***]   "))

    def test_conv_list_index(self):
        self.assertEqual(self.parser.conv_list_index("[7777]"), 7777)
        self.assertEqual(self.parser.conv_list_index("[]"), -1)
        self.assertEqual(self.parser.conv_list_index("[23]"), 23)
        self.assertEqual(self.parser.conv_list_index("[0]"), 0)

    def test_conv_object_index(self):
        self.assertEqual(self.parser.conv_object_index("[anme]"), 'anme')
        self.assertEqual(self.parser.conv_object_index("[lalallala]"), 'lalallala')
        self.assertEqual(self.parser.conv_object_index("[dddd0]"), 'dddd0')
        self.assertEqual(self.parser.conv_object_index("[name]"), 'name')

    def test_conv_index(self):
        self.assertEqual(self.parser.conv_index("[7777]"), 7777)
        self.assertEqual(self.parser.conv_index("[]"), -1)
        self.assertEqual(self.parser.conv_index("[23]"), 23)
        self.assertEqual(self.parser.conv_index("[0]"), 0)
        self.assertEqual(self.parser.conv_index("[anme]"), 'anme')
        self.assertEqual(self.parser.conv_index("[lalallala]"), 'lalallala')
        self.assertEqual(self.parser.conv_index("[dddd0]"), 'dddd0')
        self.assertEqual(self.parser.conv_index("[name]"), 'name')

    def test_parser_object(self):
        data = {
            'title[id][length]': 'lalal'
        }
        parser = ParserMultiDimensional(data)
        self.assertTrue(parser.is_valid())
        result = parser.construct(data)
        expected = {
            'title': {
                'id': {
                    'length': 'lalal'
                }
            }
        }
        self.assertDictEqual(result, expected)

    def test_parser_object2(self):
        data = {
            'title[id][length]': 'lalal',
            'title[id][value]': 'lalal'
        }
        parser = ParserMultiDimensional(data)
        result = parser.construct(data)
        expected = {
            'title': {
                'id': {
                    'length': 'lalal',
                    'value': 'lalal'
                }
            }
        }
        self.assertDictEqual(result, expected)

    def test_parser_object3(self):
        data = {
            'title[id][length]': 'lalal',
            'title[id][value]': 'lalal',
            'title[id][value]': 'lalal',
            'title[value]': 'lalal'
        }
        parser = ParserMultiDimensional(data)
        self.assertTrue(parser.is_valid())
        result = parser.construct(data)
        expected = {
            'title': {
                'id': {
                    'length': 'lalal',
                    'value': 'lalal'
                },
                'value': 'lalal'
            }
        }
        self.assertDictEqual(result, expected)

    def test_parser_object4(self):
        data = {
            'title[id][length]': 'lalal',
            'title[id][value]': 'lalal',
            'title[id][value]': 'lalal',
            'title[value]': 'lalal',
            'sub': 'lalal',
            'title[id][recusrive][only][field]': 'icci'
        }
        parser = ParserMultiDimensional(data)
        self.assertTrue(parser.is_valid())
        result = parser.construct(data)
        expected = {
            'title': {
                'id': {
                    'length': 'lalal',
                    'value': 'lalal',
                    'recusrive': {
                        'only': {
                            'field': 'icci'
                        }
                    }
                },
                'value': 'lalal'
            },
            'sub': 'lalal'
        }
        self.assertDictEqual(result, expected)

    def test_parser_object_reasing(self):
        data = {
            'title[id][length]': 'lalal',
            'title[id][  length  ]': 'lalal',
        }
        parser = ParserMultiDimensional(data)
        self.assertTrue(parser.is_valid())
        result = parser.construct(data)
        expected = {
            'title': {
                'id': {
                    'length': 'lalal'
                }
            }
        }
        self.assertEqual(expected, result)

    def test_parser_object_reasing2(self):
        data = {
            'title[id][length]': 'lalal',
            'title[value]': 'lalal',
            'sub': 'lalal',
            'title[id][recusrive][only][field]': 'icci',
        }
        parser = ParserMultiDimensional(data)
        self.assertTrue(parser.is_valid())
        result = parser.construct(data)
        expected = {
            'title': {
                'id': {
                    'length': 'lalal',
                    'recusrive': {
                        'only': {
                            'field': 'icci'
                        },
                    },
                },
                'value': 'lalal',
            },
            'sub': 'lalal',
        }
        self.assertEqual(expected, result)

    def test_parser_classic(self):
        data = {
            'title': 'lalal'
        }
        parser = ParserMultiDimensional(data)
        self.assertTrue(parser.is_valid())
        result = parser.construct(data)
        expected = {
            'title': 'lalal'
        }
        self.assertDictEqual(result, expected)

    def test_parser_classic_double_assign(self):
        data = {
            'title   ': 'lalal',
            'title': 'dddddddddddddd'
        }
        parser = ParserMultiDimensional(data)
        self.assertTrue(parser.is_valid())
        result = parser.construct(data)
        expected = {'title': 'lalal'}
        self.assertEqual(result, expected)

    def test_parser_list(self):
        data = {
            'title': 'lalal',
            'list[]': 'icicici'
        }
        parser = ParserMultiDimensional(data)
        result = parser.construct(data)
        expected = {
            'title': 'lalal',
            'list': [
                'icicici'
            ]
        }
        self.assertTrue(parser.is_valid())
        self.assertEqual(result, expected)

    def test_parser_list_index_out_of_range(self):
        data = {
            'title': 'lalal',
            'list[2]': 'icicici'
        }
        parser = ParserMultiDimensional(data)
        self.assertTrue(parser.is_valid())
        result = parser.construct(data)
        expected = {
            'title': 'lalal',
            'list': [
                "icicici"
            ]
        }
        self.assertEqual(result, expected)

    def test_parser_list_object_index(self):
        data = {
            'title': 'lalal',
            'list[length][]': 'icicici'
        }
        parser = ParserMultiDimensional(data)
        result = parser.construct(data)
        expected = {
            'title': 'lalal',
            'list': {
                'length': [
                    'icicici'
                ]
            }
        }
        self.assertTrue(parser.is_valid())
        self.assertEqual(result, expected)

    def test_parser_list_double_assign(self):
        data = {
            'title': 'lalal',
            'list[]': 'icicici',
            'list[ ]': 'new',
            'list[1]': 'neeew',
        }
        parser = ParserMultiDimensional(data)
        self.assertTrue(parser.is_valid())
        result = parser.construct(data)
        expected = {
            'title': 'lalal',
            'list': [
                'icicici',
                'neeew'
            ]
        }
        self.assertEqual(result, expected)

    def test_real(self):
        data = {
            'title': 'title',
            'date': "time",
            'langs[0][id]': "id",
            'langs[0][title]': 'title',
            'langs[0][description]': 'description',
            'langs[0][language]': "language",
            'langs[1][id]': "id1",
            'langs[1][title]': 'title1',
            'langs[1][description]': 'description1',
            'langs[1][language]': "language1"
        }
        parser = ParserMultiDimensional(data)
        self.assertTrue(parser.is_valid())
        result = parser.construct(data)
        expected = {
            'title': 'title',
            'date': "time",
            'langs': [
                {
                    'id': 'id',
                    'title': 'title',
                    'description': 'description',
                    'language': 'language'
                },
                {
                    'id': 'id1',
                    'title': 'title1',
                    'description': 'description1',
                    'language': 'language1'
                }
            ]
        }
        self.assertEqual(result, expected)
