#!/usr/bin/env python
"""Test suite for surblclient.py"""

# Copyright (c) 2009 Filip Salomonsson
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

import unittest

class TestSurblclient(unittest.TestCase):
    def testPass(self):
        domains = ("google.com", "yahoo.com", "apple.com")
        for domain in domains:
            self.assertFalse(domain in surbl)
            self.assertFalse(surbl.lookup(domain))

    def testSurblTestPoints(self):
        domains = ("test.surbl.org", "surbl-org-permanent-test-point.com")
        all = ['sc', 'ws', 'ph', 'ob', 'ab', 'jp']
        for domain in domains:
            subdomain = "foo.bar.baz." + domain
            self.assertTrue(domain in surbl)
            self.assertEquals(surbl.lookup(domain), (domain, all))
            self.assertTrue(subdomain in surbl)
            self.assertEquals(surbl.lookup(subdomain), (domain, all))


if __name__ == '__main__':
    import sys
    from surblclient import surbl
    unittest.main()
