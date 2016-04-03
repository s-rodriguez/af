import logging
import os
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


def af_directory():
    return os.path.dirname(os.path.abspath(__file__))


log_dir = os.path.join(os.path.expanduser('~'), 'af', 'logs')
if not os.path.isdir(log_dir):
    os.makedirs(log_dir)

LOG_FILENAME = os.path.join(log_dir, 'af_session.log')
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
)


def main(cls=None, method=None, resource=None):
    """
    Dummy Function to tests setup things, like Sphinx, tox, and others.

    :param cls: class associated with the request's endpoint
    :type cls: :class:`sandman.model.Model` instance
    :param string method: HTTP method of incoming request
    :param resource: *cls* instance associated with the request
    :type resource: :class:`sandman.model.Model` or None
    :rtype: bool
    """
    print "MAIN FUNCTION FOR THE AF"
    return True

if __name__ == "__main__":
    main()
