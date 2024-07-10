from setuptools import setup, find_packages, Command

import os
import re


class CoverageCommand(Command):
    description = "coverage report"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('coverage run --source zru setup.py test')
        os.system('coverage html')


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('zru')

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


setup(
    name='zru-python',
    version=version,
    url='https://github.com/zrupay/zru-python',
    license='BSD',
    description='ZRU Python Bindings',
    long_description=README,
    long_description_content_type="text/markdown",
    author='ZRU',
    author_email='support@zrupay.com',
    download_url='https://github.com/zrupay/zru-python/archive/v1.0.0.tar.gz',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'requests'
    ],
    keywords=['zru', 'payments'],
    extras_require={
        'test': ['mock', 'coverage'],
    },
    cmdclass={
        'coverage': CoverageCommand
    },

    test_suite="tests",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
