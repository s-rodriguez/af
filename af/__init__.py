import logging
import os
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


def af_directory():
    """Returns the location of the installed af package

    :rtype: str

    """
    return os.path.dirname(os.path.abspath(__file__))


def af_user_directory():
    """Returns the location of the af user directory

    :rtype: str

    """
    return os.path.abspath(os.path.join(os.path.expanduser('~'), 'af'))


def create_basic_directories():
    """Creates the basic user directories to use

    """
    directories = ['logs', 'reports']
    for directory in directories:
        dir_path = os.path.join(af_user_directory(), directory)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)


create_basic_directories()
LOG_FILENAME = os.path.join(af_user_directory(), 'logs', 'af_session.log')
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
)


  # TODO: REMOVE METHOD
def report():
    from af.utils.tests.report_test import report_test
    report_test()


def main(cls=None, method=None, resource=None):
    """Main entry point for the anonymization framework. Starts the framework to be used by console

    """
  # TODO: REMOVE METHOD AND CREATE MAIN FUNCTION
    from af.utils.tests.af_test import af_test
    af_test()

if __name__ == "__main__":
    """Calls the main entry point for the anonymization framework

    """
    main()
