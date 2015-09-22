import unittest
from api.lib.utils import verification_string_is_json, object_to_json
from api.models import App
from django.test import TestCase


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])


class TestUtilsMethods(TestCase):

    def test_verification_string_is_json(self):
        json_str = '{"name":"xiaomin"}'
        not_json_str = '{"name":"xiaomin"dd}'
        self.assertTrue(verification_string_is_json(json_str))
        self.assertFalse(verification_string_is_json(not_json_str))
        self.assertFalse(verification_string_is_json(""))

    def test_object_to_json_not_list(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_object_to_json_is_list(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
