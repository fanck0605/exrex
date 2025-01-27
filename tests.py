#!/usr/bin/env python

# This file is part of exrex.
#
# exrex is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# exrex is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with exrex. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2012- by Adam Tauber, <asciimoo@gmail.com>

import re
import unittest

from exrex import generate, count, getone, CATEGORIES, simplify

try:
    import re._parser as sre_parse
except ImportError: # Python < 3.11
    from re import sre_parse

RS = {
    '(a|b)': ['a', 'b'],
    '[ab][cd]': ['ac', 'ad', 'bc', 'bd'],
    'a|ab': ['a', 'ab'],
    '[0-2]': ['0', '1', '2'],
    '(foo|bar)(20|)16': ['foo2016', 'foo16', 'bar2016', 'bar16'],
    '[12]{1,2}': ['1', '2', '11', '12', '21', '22'],
    '((hai){2}|world)!': ['haihai!', 'world!'],
    '[ab]{1,3}': ['a', 'b', 'aa', 'ab', 'ba', 'bb', 'aaa', 'aab', 'aba', 'abb', 'baa', 'bab', 'bba', 'bbb'],
    '\d': list(map(str, range(0, 10))),
    'a[b]?(c){0,1}': ['a', 'ac', 'ab', 'abc'],
    '(a(b(c(d(e(f))))))': ['abcdef'],
    '(a(b(c(d(e(f){1,2}))))){1,2}': ['abcdef', 'abcdeff', 'abcdefabcdef',
                                     'abcdefabcdeff', 'abcdeffabcdef', 'abcdeffabcdeff'],
    '[^a]': [x for x in CATEGORIES['category_any'] if x != 'a'],
    '[^asdf]': [x for x in CATEGORIES['category_any'] if x not in 'asdf'],
    'asdf': ['asdf'],
    '(as|df)': ['as', 'df'],
    '[áíő]': [u'á', u'í', u'ő'],
    '(a|b)(1|2)\\1\\2\\1\\2': ['a1a1a1', 'a2a2a2', 'b1b1b1', 'b2b2b2'],
    '(?=x)': ['x'],
    '\\da{2}': ['0aa', '1aa', '2aa', '3aa', '4aa', '5aa', '6aa', '7aa', '8aa', '9aa'],
    '\\w': CATEGORIES[sre_parse.CATEGORY_WORD],
    '\\W': CATEGORIES[sre_parse.CATEGORY_NOT_WORD]
}

BIGS = [
    '^a*$',
    '^[a-zA-Z]+$',
    '^(foo){3,}$',
    '^([^/]+)(.*)$',
    '^[^/]+(.*)$',
    '^([^/]+).*$',
    '^[^asdf]+$',
    '^a{5,}?',
    '^a[^bcd]*?e',
    '^([^0-9]{2,}|(a|s|d|f|g)+|[a-z]+)+$',
    '^([^ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz]|asdf)+$',
    '^(1[0-2]|0[1-9])(:[0-5]\d){2} (A|P)M$',
    '(.*)\\1'
]


class TestExrex(unittest.TestCase):
    def test_gen(self):
        for regex, result in RS.items():
            with self.subTest(regex):
                self.assertEqual(list(generate(regex)), result)

    def test_count(self):
        for regex, result in RS.items():
            with self.subTest(regex):
                self.assertEqual(count(regex), len(result))

    def test_getone(self):
        tries = 200
        for regex, _ in RS.items():
            with self.subTest(regex):
                for _ in range(tries):
                    s = getone(regex)
                    self.assertTrue(re.match(regex, s, re.U))

        for regex in BIGS:
            with self.subTest(regex):
                for _ in range(tries):
                    s = getone(regex)
                    self.assertTrue(re.match(regex, s, re.U))

    def test_simplify(self):
        for regex, result in RS.items():
            with self.subTest(regex):
                new_regex = simplify(regex)
                r = list(generate(new_regex))
                self.assertEqual(r, result)


if __name__ == '__main__':
    unittest.main()
