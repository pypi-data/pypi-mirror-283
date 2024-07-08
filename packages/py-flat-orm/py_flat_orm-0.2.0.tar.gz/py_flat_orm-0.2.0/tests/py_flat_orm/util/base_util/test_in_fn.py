"""TestInFn"""

import unittest
from datetime import date, time, datetime
from decimal import Decimal, ROUND_HALF_UP

from py_flat_orm.util.base_util.in_fn import InFn
from test_data.domain.all_common_types_obj import AllCommonTypesObj
from test_data.domain.my_enum import MyEnum
from test_data.domain.my_person import MyPerson


class TestInFn(unittest.TestCase):
    """TestInFn"""

    def test_as_boolean(self):
        self.assertIsNone(InFn.as_boolean(None))
        self.assertTrue(InFn.as_boolean('true'))
        self.assertFalse(InFn.as_boolean('false'))
        self.assertFalse(InFn.as_boolean('any other string'))

    def test_as_decimal(self):
        self.assertEqual(InFn.as_decimal('123.456'), Decimal('123.456'))
        self.assertIsNone(InFn.as_decimal('not a number'))

    def test_as_decimal_with_scale(self):
        self.assertEqual(
            InFn.as_decimal_with_scale(2, ROUND_HALF_UP, '123.456'),
            Decimal('123.46')
        )
        self.assertIsNone(InFn.as_decimal_with_scale(2, ROUND_HALF_UP, 'not a number'))

    def test_as_double(self):
        self.assertEqual(InFn.as_double('123.456'), 123.456)
        self.assertIsNone(InFn.as_double('not a number'))

    def test_as_float(self):
        self.assertEqual(InFn.as_float('123.456'), 123.456)
        self.assertIsNone(InFn.as_float('not a number'))

    def test_as_integer(self):
        self.assertEqual(InFn.as_integer('123'), 123)
        self.assertIsNone(InFn.as_integer('not a number'))

    def test_as_long(self):
        self.assertEqual(InFn.as_long('123'), 123)
        self.assertIsNone(InFn.as_long('not a number'))

    def test_as_string(self):
        self.assertEqual(InFn.as_string(123), '123')
        self.assertEqual(InFn.as_string(None), None)

    def test_safe_get(self):
        self.assertEqual(InFn.safe_get(42, lambda: 1 / 0), 42)
        self.assertEqual(InFn.safe_get(42, lambda: 21 * 2), 42)

    def test_has_field(self):
        self.assertTrue(InFn.has_field('key', {'key': 'value'}))
        self.assertFalse(InFn.has_field('key', {}))

    def test_is_blank(self):
        self.assertFalse(InFn.is_blank("test"))
        self.assertFalse(InFn.is_blank(" test "))
        self.assertTrue(InFn.is_blank(""))
        self.assertTrue(InFn.is_blank("   "))
        self.assertTrue(InFn.is_blank(None))

    def test_is_not_blank(self):
        self.assertTrue(InFn.is_not_blank("test"))
        self.assertTrue(InFn.is_not_blank(" test "))
        self.assertFalse(InFn.is_not_blank(""))
        self.assertFalse(InFn.is_not_blank("   "))
        self.assertFalse(InFn.is_not_blank(None))

    def test_is_decimal(self):
        self.assertTrue(InFn.is_decimal('123.456'))
        self.assertFalse(InFn.is_decimal('not a number'))

    def test_is_boolean(self):
        self.assertTrue(InFn.is_boolean('true'))
        self.assertTrue(InFn.is_boolean('false'))
        self.assertFalse(InFn.is_boolean('maybe'))
        self.assertFalse(InFn.is_boolean(None))

    def test_is_double(self):
        self.assertTrue(InFn.is_double('123.456'))
        self.assertFalse(InFn.is_double('not a number'))

    def test_is_float(self):
        self.assertTrue(InFn.is_float('123.456'))
        self.assertFalse(InFn.is_float('not a number'))

    def test_is_integer(self):
        self.assertTrue(InFn.is_integer('123'))
        self.assertFalse(InFn.is_integer('123.456'))

    def test_is_null(self):
        self.assertTrue(InFn.is_none(None))
        self.assertFalse(InFn.is_none('123'))

    def test_is_number(self):
        self.assertTrue(InFn.is_number('123'))
        self.assertTrue(InFn.is_number('123.456'))
        self.assertFalse(InFn.is_number('not a number'))

    def test_get_enum_keys(self):
        expected_keys = ['ONE', 'TWO', 'THREE']
        result = InFn.get_enum_keys(MyEnum)
        self.assertListEqual(sorted(result), sorted(expected_keys))

    def test_get_keys(self):
        class DummyClass:
            def __init__(self):
                self.field1 = 'value1'
                self.field2 = 'value2'

        self.assertEqual(InFn.get_keys(DummyClass()), ['field1', 'field2'])

    def test_get_type(self):
        self.assertEqual(InFn.get_static_field_type(MyPerson, "id"), int | None)
        self.assertEqual(InFn.get_static_field_type(MyPerson, "age"), int)
        self.assertEqual(InFn.get_static_field_type(MyPerson, "name"), str)
        self.assertEqual(InFn.get_static_field_type(MyPerson, "is_male"), bool)
        self.assertEqual(InFn.get_static_field_type(MyPerson, "is_single"), bool | None)
        self.assertEqual(InFn.get_static_field_type(MyPerson, "long_v"), int)
        self.assertEqual(InFn.get_static_field_type(MyPerson, "long_v2"), int | None)

    # Optional: Use subTest for parameterized tests
    def test_get_type_parametrized(self):
        parameters = [
            ("id", int | None),
            ("age", int),
            ("name", str),
            ("is_male", bool),
            ("is_single", bool | None),
            ("long_v", int),
            ("long_v2", int | None)
        ]

        for field_name, expected_type in parameters:
            with self.subTest(field_name=field_name):
                self.assertEqual(InFn.get_static_field_type(MyPerson, field_name), expected_type)

    def test_camel_to_upper_snake_case(self):
        self.assertEqual(InFn.camel_to_upper_snake_case('camelCaseText'), 'CAMEL_CASE_TEXT')
        self.assertIsNone(InFn.camel_to_upper_snake_case(None))

    def test_prop_as_string(self):
        self.assertEqual(InFn.prop_as_string('key', {'key': 'value'}), 'value')
        self.assertIsNone(InFn.prop_as_string('key', {}))

    def test_camel_to_lower_hyphen_case(self):
        self.assertEqual(InFn.camel_to_lower_hyphen_case('camelCaseText'), 'camel-case-text')
        self.assertIsNone(InFn.camel_to_lower_hyphen_case(None))

    def test_hyphen_to_snake_case(self):
        self.assertEqual(InFn.hyphen_to_snake_case('hyphen-case-text'), 'hyphen_case_text')
        self.assertIsNone(InFn.hyphen_to_snake_case(None))

    def test_snake_to_hyphen_case(self):
        self.assertEqual(InFn.snake_to_hyphen_case('snake_case_text'), 'snake-case-text')
        self.assertIsNone(InFn.snake_to_hyphen_case(None))

    def test_prop_as_boolean(self):
        self.assertTrue(InFn.prop_as_boolean('key', {'key': 'true'}))
        self.assertFalse(InFn.prop_as_boolean('key', {'key': 'false'}))
        self.assertIsNone(InFn.prop_as_boolean('key', {}))

    def test_prop_as_decimal(self):
        self.assertEqual(InFn.prop_as_decimal('key', {'key': '123.456'}), Decimal('123.456'))
        self.assertIsNone(InFn.prop_as_decimal('key', {}))

    def test_prop_as_double(self):
        self.assertEqual(InFn.prop_as_double('key', {'key': '123.456'}), 123.456)
        self.assertIsNone(InFn.prop_as_double('key', {}))

    def test_prop_as_float(self):
        self.assertEqual(InFn.prop_as_float('key', {'key': '123.456'}), 123.456)
        self.assertIsNone(InFn.prop_as_float('key', {}))

    def test_prop_as_integer(self):
        self.assertEqual(InFn.prop_as_integer('key', {'key': '123'}), 123)
        self.assertIsNone(InFn.prop_as_integer('key', {}))

    def test_prop_as_long(self):
        self.assertEqual(InFn.prop_as_long('key', {'key': '123'}), 123)
        self.assertIsNone(InFn.prop_as_long('key', {}))

    def test_self(self):
        self.assertEqual(InFn.self('test'), 'test')

    def test_uniq_by(self):
        class DummyClass:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        c1 = DummyClass(1, 'c')
        b = DummyClass(2, 'b')
        c2 = DummyClass(3, 'c')
        items = [c1, b, c2]
        uniq_items = InFn.uniq_by(items, lambda i: i.y)
        self.assertEqual(uniq_items, [c1, b])

    def test_to_dict(self):
        class DummyClass:
            def __init__(self):
                self.field1 = 'value1'
                self.field2 = 'value2'

        expected_map = {'field1': 'value1', 'field2': 'value2'}
        self.assertEqual(InFn.to_dict(DummyClass()), expected_map)

    def test_prop(self):
        self.assertEqual(InFn.prop('key', {'key': 'value'}), 'value')
        self.assertIsNone(InFn.prop('key', {}))

    def test_set_primitive_field(self):
        obj = AllCommonTypesObj()

        # Set primitive fields using InFn.set_primitive_field
        InFn.set_primitive_field(obj, "int_field", 25.2)
        InFn.set_primitive_field(obj, "float_field", 1.75)
        InFn.set_primitive_field(obj, "bool_field", True)
        InFn.set_primitive_field(obj, "str_field", True)
        InFn.set_primitive_field(obj, "date_field", date(2024, 6, 19))
        InFn.set_primitive_field(obj, "time_field", date(2024, 6, 19))
        InFn.set_primitive_field(obj, "datetime_field", date(2024, 6, 19))

        # Assert the fields are set correctly
        self.assertEqual(obj.int_field, 25)
        self.assertEqual(obj.float_field, 1.75)
        self.assertEqual(obj.bool_field, True)
        self.assertEqual(obj.str_field, "True")
        self.assertEqual(obj.date_field, date(2024, 6, 19))
        self.assertEqual(obj.time_field, time(0, 0, 0))
        self.assertEqual(obj.datetime_field, datetime(2024, 6, 19, 0, 0, 0))

    def test_set_primitive_field_and_set_to_none(self):
        obj = AllCommonTypesObj()

        # Set primitive fields using InFn.set_primitive_field
        InFn.set_primitive_field(obj, "int_field", None)
        InFn.set_primitive_field(obj, "float_field", None)
        InFn.set_primitive_field(obj, "bool_field", None)
        InFn.set_primitive_field(obj, "str_field", None)
        InFn.set_primitive_field(obj, "date_field", None)
        InFn.set_primitive_field(obj, "time_field", None)
        InFn.set_primitive_field(obj, "datetime_field", None)

        # Assert the fields are set correctly
        self.assertEqual(obj.int_field, None)
        self.assertEqual(obj.float_field, None)
        self.assertEqual(obj.bool_field, None)
        self.assertEqual(obj.str_field, None)
        self.assertEqual(obj.date_field, None)
        self.assertEqual(obj.time_field, None)
        self.assertEqual(obj.datetime_field, None)

    def test_spaced_to_lower_snake_case(self):
        self.assertEqual(InFn.spaced_to_lower_snake_case('test case'), 'test_case')
        self.assertIsNone(InFn.spaced_to_lower_snake_case(None))

    def test_trim_to_empty_if_is_string(self):
        self.assertEqual(InFn.trim_to_empty_if_is_string('  test  '), 'test')
        self.assertEqual(InFn.trim_to_empty_if_is_string(123), 123)
        self.assertIsNone(InFn.trim_to_empty_if_is_string(None))

    def test_without_char(self):
        self.assertEqual(InFn.without_char('abc123'), '123')
        self.assertEqual(InFn.without_char(None), '')


if __name__ == '__main__':
    unittest.main()
