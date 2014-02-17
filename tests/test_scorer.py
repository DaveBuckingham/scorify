# -*- coding: utf-8 -*-
# Part of the scorify package
# Copyright 2014 Board of Regents of the University of Wisconsin System

import pytest

import math
from scorify import datafile, scoresheet, scorer


@pytest.fixture
def transforms():
    ts = scoresheet.TransformSection()
    ts.append_from_strings(['-', 'map(1:5,5:1)'])
    return ts


@pytest.fixture
def scores_1():
    ss = scoresheet.ScoreSection()
    ss.append_from_strings(['happy1', 'happy'])
    ss.append_from_strings(['happy2', 'happy', '-'])
    return ss

@pytest.fixture
def scores_2():
    ss = scoresheet.ScoreSection()
    ss.append_from_strings(['happy1', 'happy'])
    ss.append_from_strings(['happy2', 'happy', '-'])
    ss.append_from_strings(['sad1', 'sad'])
    ss.append_from_strings(['sad2', 'sad', '-'])
    return ss

@pytest.fixture
def data_1():
    df = datafile.Datafile(None, None)
    df.header = ['ppt', 'happy1', 'sad1', 'happy2', 'sad2']
    df.append_data(['a', '5', '2', '2', '4'])
    df.append_data(['b', '2', '3', '4', '1'])
    return df

@pytest.fixture
def data_with_bad():
    df = datafile.Datafile(None, None)
    df.header = ['ppt', 'happy1', 'sad1', 'happy2', 'sad2']
    df.append_data(['a', 'bad', '2', 'bad', '4'])
    return df

@pytest.fixture
def bad_scored(data_with_bad, transforms, scores_1):
    return scorer.Scorer.score(data_with_bad, transforms, scores_1)

@pytest.fixture
def measures_1():
    ms = scoresheet.MeasureSection()
    ms.append_from_strings(['happy', 'mean(happy)'])
    return ms

@pytest.fixture
def measures_2():
    ms = scoresheet.MeasureSection()
    ms.append_from_strings(['affect', 'sum(happy, sad)'])
    return ms

@pytest.fixture
def scored_data_1(data_1, transforms, scores_1):
    return scorer.Scorer.score(data_1, transforms, scores_1)

@pytest.fixture
def scored_data_2(data_1, transforms, scores_2):
    return scorer.Scorer.score(data_1, transforms, scores_2)

def test_scorer_scores(data_1, transforms, scores_1):
    res = scorer.Scorer.score(data_1, transforms, scores_1)
    assert res.header == ['happy1: happy', 'happy2: happy']
    d = res.data[0]
    assert d['happy1: happy'] == '5'
    assert d['happy2: happy'] == 4


def test_scorer_assigns_nan_on_bad_score(data_with_bad, transforms, scores_1):
    res = scorer.Scorer.score(data_with_bad, transforms, scores_1)
    d = res.data[0]
    assert math.isnan(d['happy2: happy'])


def test_scorer_measures(scored_data_1, measures_1):
    assert scored_data_1.header == ['happy1: happy', 'happy2: happy']
    scorer.Scorer.add_measures(scored_data_1, measures_1)
    assert scored_data_1.header == ['happy1: happy', 'happy2: happy', 'happy']
    assert scored_data_1.data[0]['happy'] == 4.5


def test_scorer_assigns_nan_on_bad_measure(bad_scored, measures_1):
    scorer.Scorer.add_measures(bad_scored, measures_1)
    assert math.isnan(bad_scored.data[0]['happy'])

def test_measures_multi_names(scored_data_2, measures_2):
    scorer.Scorer.add_measures(scored_data_2, measures_2)
    d = scored_data_2.data[0]
    assert d['affect'] == 5+4+2+2