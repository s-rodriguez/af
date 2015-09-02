import unittest
from af.dummy_directory.dummy_class import Foo


class TestDummyClass(unittest.TestCase):

    def test_print_ok(self):
        number = 3
        name = 5
        print_dummy_expected = "{number}1 - {name}".format(number=number, name=name)
        d = Foo(number, name)
        self.assertEqual(print_dummy_expected, d.print_foo(), "Different printing")
