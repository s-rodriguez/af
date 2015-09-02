

class Foo(object):

    def __init__(self, number=1, name="Foo1"):
        self.number = number
        self.name = name

    def get_number(self):
        return self.number

    def get_name(self):
        return self.name

    def print_foo(self):
        return "{number} - {name}".format(number=self.number, name=self.name)

