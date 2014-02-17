# -*- coding: utf-8 -*-
# Part of the scorify package
# Copyright 2014 Board of Regents of the University of Wisconsin System

from __future__ import with_statement

import pytest

from scorify import directives


def test_layout_accepts_header_skip_data():
    with pytest.raises(directives.DirectiveError):
        l = directives.Layout('foo')
    assert directives.Layout('header')
    assert directives.Layout('data')
    assert directives.Layout('skip')
    assert directives.Layout(' skip ')
    assert directives.Layout('SKIP')


def test_transforming_works():
    tx = directives.Transform('', '')
    assert tx.transform(1) == 1
    tx = directives.Transform('', 'map(1:5,2:6)')
    assert tx.transform(1) == 2


def test_measure():
    m = directives.Measure('foo', 'mean(c_foo)')
    assert m.agg_fx
    assert m.to_use == ['c_foo']
    with pytest.raises(directives.DirectiveError):
        directives.Measure('foo', 'bar')