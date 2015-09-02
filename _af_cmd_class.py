import sys
import versioneer
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


def get_cmd_class():
        cmd_class = versioneer.get_cmdclass()
        cmd_class['test'] = PyTest
        return cmd_class
