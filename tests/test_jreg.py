#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from jreg import jreg


def test_basic_initialization():
    j = jreg.JavaRegex()
    result = j.match('.*', 'abc')
    assert result == 'abc'


def test_custom_class():
    j = jreg.JavaRegex(custom_regex_checker_class_path=os.path.abspath(os.path.join(os.path.dirname(__file__), "./RegexTester.class")))
    result = j.match('.*', 'abc')
    assert result == 'abc'


def test_no_matches_with_custom_class():
    j = jreg.JavaRegex(custom_regex_checker_class_path=os.path.abspath(os.path.join(os.path.dirname(__file__), "./RegexTester.class")))
    result = j.match('[A-Z]', '0123456789')
    assert result == 'No matches found!'
