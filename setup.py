import os
import codecs
from setuptools import setup

__author__ = "Calgary Michael"
__contact__ = "cseth.michael@gmail.com"
__version__ = "0.0.1"

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='modmmocker',
    version=__version__,
    description='A Proof of Concept mocker for PyMODM',
    long_description=long_description,
    url='https://github.com/CalgaryMichael/modmmocker',
    author=__author__,
    author_email=__contact__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Apache License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='mongo mock test',
    py_modules=["modmmocker"],
    install_requires=[
        'mypy==0.590',
        'pymodm==0.4.0',
        'pymongo==3.6.1',
        'typed-ast==1.1.0',
        '-e git+https://github.com/CalgaryMichael/mongomock.git@issue-382#egg=mongomock'
    ],
    extras_require={
        'test': ['mock'],
    }
)
