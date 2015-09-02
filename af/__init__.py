from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


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
