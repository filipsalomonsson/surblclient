#!/usr/bin/env python
from distutils.core import setup
# patch distutils if it can't cope with the "classifiers" or
# "download_url" keywords
from sys import version
if version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

import surblclient

setup(name='Surblclient',
      version='0.1',
      description="Simple client library for the surbl.org blacklists",
      long_description=surblclient.__doc__,
      author="Filip Salomonsson",
      author_email="filip.salomonsson@gmail.com",
      py_modules=['surblclient'],
      )
