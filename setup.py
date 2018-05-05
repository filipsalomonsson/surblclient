#!/usr/bin/env python
from setuptools import setup, find_packages

import surblclient

setup(name="surblclient",
      version=surblclient.VERSION,
      description="Simple client library for the surbl.org blacklists",
      long_description=surblclient.__doc__,
      author="Filip Salomonsson",
      author_email="filip.salomonsson@gmail.com",
      url="http://github.com/filipsalomonsson/surblclient",
      py_modules=["surblclient"],
      )
