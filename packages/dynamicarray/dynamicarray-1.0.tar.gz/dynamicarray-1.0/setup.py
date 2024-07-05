# setup.py

from setuptools import setup, Extension

module = Extension('dynamicarray',
                   sources=['dynamic_array.c'],
                   include_dirs=['/usr/include/python3.11'],
                   library_dirs=['/usr/lib/python3.11/config-3.11-x86_64-linux-gnu','/usr/lib/x86_64-linux-gnu'],
                   libraries=['python3.11'],

                   )

setup(name='dynamicarray',
      version='1.0',
      description='A simple dynamic array module implemented in C',
      ext_modules=[module])

