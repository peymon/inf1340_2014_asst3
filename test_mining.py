#!/usr/bin/env python3

"""
Assignment 3 - Data Mining
INF1340H, Fall 2014
Deadline: December 1, 2014 at 11:59pm.

 Test Cases
"""

__author__ = 'Peymon & Haoran & Olena'
__email__ = "OlePeyHao@olepeyhao.com"

__copyright__ = "2014 Peymon & Haoran & Olena"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line

import pytest
from mining import *


def test_goog():
    """
    GOOG tests
    1. Six best months
    2. Six worst months
    3. Item not in dictionary, raise TypeError
    4. No file to read, raise FileNotFoundError
    """
    google = StockMiner("GOOG", "data/GOOG.json")
    assert google.six_best_months() == [('2007/12', 693.76), ('2007/11', 676.55), ('2007/10', 637.38),
                                        ('2008/01', 599.42), ('2008/05', 576.29), ('2008/06', 555.34)]
    assert google.six_worst_months() == [('2004/08', 104.66), ('2004/09', 116.38), ('2004/10', 164.52),
                                         ('2004/11', 177.09), ('2004/12', 181.01), ('2005/03', 181.18)]
    with pytest.raises(TypeError):
        google.change_date("1990-03-13")
    with pytest.raises(FileNotFoundError):
        google.read_stock_data("")


def test_tse_so():
    """
    TSE-SO tests
    1. Six best months
    2. Six worst months
    3. Item not in dictionary, raise TypeError
    4. No file to read, raise FileNotFoundError
    """
    tseso = StockMiner("TSE-SO", "data/TSE-SO.json")
    assert tseso.six_best_months() == [('2007/12', 20.98), ('2007/11', 20.89), ('2013/05', 19.96), ('2013/06', 19.94),
                                       ('2013/04', 19.65), ('2007/10', 19.11)]
    assert tseso.six_worst_months() == [('2009/03', 1.74), ('2008/11', 2.08), ('2008/12', 2.25), ('2009/02', 2.41),
                                        ('2009/04', 2.75), ('2009/01', 3.14)]
    with pytest.raises(TypeError):
        tseso.change_date("1990-03-13")
    with pytest.raises(FileNotFoundError):
        tseso.read_stock_data("")
    #with pytest.raises(TypeError):
    #    tseso.change_date("0000-00-00")


def test_com():
    """
    BONUS: Compare Two Stocks tests
    1. GOOG has a higher standard deviation
    2. Two stocks have the same standard deviation
    """
    assert compare("GOOG", "data/GOOG.json", "TSE-SO", "data/TSE-SO.json") == ["GOOG"]
    assert compare("GOOG", "data/GOOG.json", "GOOG", "data/GOOG.json") == ["Same"]