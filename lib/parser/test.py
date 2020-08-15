from .mixins import ParserKeyDimensional
from .exeptions import ParserError
import unittest


class Parser(unittest.TestCase):

    def test_is_list(self):
        parser = ParserKeyDimensional()
        self.assertTrue(parser.is_list(""))
        self.assertTrue(parser.is_list(None))
        self.assertTrue(parser.is_list("55555"))
        self.assertTrue(parser.is_list("0"))
        self.assertFalse(parser.is_list("-0"))
        self.assertFalse(parser.is_list("dd"))

    def test_is_object(self):
        parser = ParserKeyDimensional()
        self.assertFalse(parser.is_object(""))
        self.assertFalse(parser.is_object(None))
        self.assertFalse(parser.is_object("55555"))
        self.assertTrue(parser.is_object("ferfef"))
        self.assertTrue(parser.is_object("dfFFRGRtrgrt"))
        self.assertTrue(parser.is_object("f"))
        self.assertTrue(parser.is_object("f4"))
        self.assertTrue(parser.is_object("F4"))
        self.assertFalse(parser.is_object("effef+fe"))

    def test_list(self):
        data = "data[0]"
        parser = ParserKeyDimensional(data)
        ret = parser.split()
        self.assertEqual(ret, ['data', '[0]'])
        self.assertTrue(parser.is_valid(ret))
        ret = parser.construct({}, ret, "value")
        self.assertEqual(ret, {'data': ["value"]})

    def test_list_list(self):
        data = "data[0][0]"
        parser = ParserKeyDimensional(data)
        ret = parser.split()
        self.assertEqual(ret, ['data', '[0]', '[0]'])
        self.assertTrue(parser.is_valid(ret))
        ret = parser.construct({}, ret, "value")
        self.assertEqual(ret, {'data': [["value"]]})

    def test_list_list_index_null(self):
        data = "data[0][]"
        parser = ParserKeyDimensional(data)
        ret = parser.split()
        self.assertEqual(ret, ['data', '[0]', '[]'])
        self.assertTrue(parser.is_valid(ret))
        ret = parser.construct({}, ret, "value")
        self.assertEqual(ret, {'data': [["value"]]})

    def test_list_index_null_object(self):
        data = "data[][title]"
        parser = ParserKeyDimensional(data)
        ret = parser.split()
        self.assertEqual(ret, ['data', '[]', '[title]'])
        self.assertTrue(parser.is_valid(ret))
        ret = parser.construct({}, ret, "value")
        self.assertEqual(ret, {'data': [{'title': 'value'}]})

    def test_space(self):
        data = "data[  title  ]"
        parser = ParserKeyDimensional(data)
        ret = parser.split()
        self.assertEqual(ret, ['data', '[  title  ]'])
        self.assertTrue(parser.is_valid(ret))
        ret = parser.construct({}, ret, "value")
        self.assertEqual(ret, {'data': {'title': 'value'}})

    def test_space_list_space_index_null(self):
        data = "data[  title  ][     ]"
        parser = ParserKeyDimensional(data)
        ret = parser.split()
        self.assertEqual(ret, ['data', '[  title  ]', '[     ]'])
        self.assertTrue(parser.is_valid(ret))
        ret = parser.construct({}, ret, "value")
        self.assertEqual(ret, {'data': {'title': ['value']}})

    def test_wrong_name(self):
        data = "data[  ti tle  ][     ]"
        parser = ParserKeyDimensional(data)
        ret = parser.split()
        self.assertEqual(ret, ['data', '[  ti tle  ]', '[     ]'])
        self.assertFalse(parser.is_valid(ret))

    def test_object_object(self):
        data = "data[  title  ][  ggg   ]"
        parser = ParserKeyDimensional(data)
        ret = parser.split()
        self.assertEqual(ret, ['data', '[  title  ]', '[  ggg   ]'])
        self.assertTrue(parser.is_valid(ret))
        ret = parser.construct({}, ret, "value")
        self.assertEqual(ret, {'data': {'title': {'ggg': 'value'}}})

    def test_object_list_object(self):
        data = "data[  title  ][][  ggg   ]"
        parser = ParserKeyDimensional(data)
        ret = parser.split()
        self.assertEqual(ret, ['data', '[  title  ]', '[]', '[  ggg   ]'])
        self.assertTrue(parser.is_valid(ret))
        ret = parser.construct({}, ret, "value")
        self.assertEqual(ret, {'data': {'title': [{'ggg': 'value'}]}})

    def test_list_list_list(self):
        data = "data[    ][][  0  ]"
        parser = ParserKeyDimensional(data)
        ret = parser.split()
        self.assertEqual(ret, ['data', '[    ]', '[]', '[  0  ]'])
        self.assertTrue(parser.is_valid(ret))
        ret = parser.construct({}, ret, "value")
        self.assertEqual(ret, {'data': [[['value']]]})

    def test_index_out_of_range(self):
        data = "data[5]"
        parser = ParserKeyDimensional(data)
        ret = parser.split()
        self.assertEqual(ret, ['data', '[5]'])
        self.assertTrue(parser.is_valid(ret))
        try:
            parser.construct({}, ret, "value")
        except Exception as e:
            self.assertIsInstance(e, ParserError)

    def test_before_valid(self):
        data = "data[++fer]"
        parser = ParserKeyDimensional(data)
        ret = parser.split()
        try:
            parser.construct({}, ret, "value")
        except Exception as e:
            self.assertIsInstance(e, ValueError)


if __name__ == '__main__':
    unittest.main()
