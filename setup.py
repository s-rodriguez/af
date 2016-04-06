from setuptools import setup, find_packages
import versioneer
from af.af_cmd_class import Tox


def get_cmd_class():
    cmd_class = versioneer.get_cmdclass()
    cmd_class['test'] = Tox
    return cmd_class

setup(
    name='af',
    version=versioneer.get_version(),
    tests_require=['tox'],
    install_requires=[],
    cmdclass=get_cmd_class(),
    description='Anonymization Framework',
    author='Sebastian Rodriguez, Gustavo Silva de Sousa',
    author_email='sebastianr213@gmail.com, gustavosilvadesousa@gmail.com',
    url='http://github.com/s-rodriguez/af/',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    test_suite='af.tests.test_af',
    extras_require={
        'testing': ['pytest'],
    },
    zip_safe=False,
    entry_points={
       'console_scripts': [
           'af = af:main'
       ]
    },
)
