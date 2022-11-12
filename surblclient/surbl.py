#!/usr/bin/env python
#
# Copyright (c) 2022 Filip Salomonsson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import print_function

import socket
import re

import importlib_resources

from .blacklist import Blacklist

_test_domains = {"surbl.org", "multi.surbl.org"}


def domains_from_resource(filename):
    files = importlib_resources.files("surblclient")
    resource = files / "data" / "surbl" / filename
    return set(resource.read_text().split())


class SURBL(Blacklist):
    domain = "multi.surbl.org."
    flags = [(8, "ph"), (16, "mw"), (64, "abuse"), (128, "cr")]

    _pseudo_tlds = (
        domains_from_resource("two-level-tlds")
        | domains_from_resource("three-level-tlds")
        | _test_domains
    )

    def get_base_domain(self, domain):
        while domain.count(".") > 1:
            _, _, rest = domain.partition(".")
            if rest in self._pseudo_tlds:
                return domain
            domain = rest
        return domain
