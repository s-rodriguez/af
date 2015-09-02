from setuptools import setup, find_packages
import versioneer

from _af_cmd_class import get_cmd_class

setup(
    name='af',
    version=versioneer.get_version(),
    tests_require=['pytest'],
    install_requires=[],
    cmdclass=get_cmd_class(),
    description='Anonymization Framework',
    author='Sebastian Rodriguez, Gustavo Silva de Sousa',
    author_email='sebastianr213@gmail.com, gustavosilvadesousa@gmail.com',
    url='http://github.com/s-rodriguez/af/',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    test_suite='af.test.test_af',
    extras_require={
        'testing': ['pytest'],
    },
    # Para futuros entry points
    # entry_points={
    #    'console_scripts': [
    #        'af = af:main'
    #    ]
    # },
)
