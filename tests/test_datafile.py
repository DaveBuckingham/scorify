# coding: utf8
# Part of the scorify package
# Copyright 2014 Board of Regents of the University of Wisconsin System

import pytest

from scorify import datafile, scoresheet


@pytest.fixture
def good_data():
    return [
        ['ppt','happy1','happy2','sad1','sad2','extra'],
        ['skip','skip','skip','skip','skip','skip'],
        ['a','5','2','1','4','3']
    ]

@pytest.fixture
def data_with_funny_lengths():
    return [
        ['a', 'b'],
        [1,2,3],
        [4]
    ]


@pytest.fixture
def layout_section_with_skip():
    ls = scoresheet.LayoutSection()
    ls.append_from_strings(['header'])
    ls.append_from_strings(['skip'])
    ls.append_from_strings(['data'])
    return ls


@pytest.fixture
def layout_section_no_skip():
    ls = scoresheet.LayoutSection()
    ls.append_from_strings(['header'])
    ls.append_from_strings(['data'])
    return ls


def test_read_populates_header_data(good_data, layout_section_with_skip):
    df = datafile.Datafile(good_data, layout_section_with_skip)
    df.read()
    assert df.header == good_data[0]
    assert df.data[0] == dict(zip(df.header, good_data[2]))


def test_read_handles_odd_lengths(
        data_with_funny_lengths, layout_section_no_skip):
    df = datafile.Datafile(data_with_funny_lengths, layout_section_no_skip)
    df.read()
    assert len(df.data[0].values()) == len(df.header)
    assert len(df.data[1].values()) == len(df.header)
