#!/usr/bin/env python3

""" Docstring """

__author__ = 'Peymon & Haoran & Olena'
__email__ = "OlePeyHao@olepeyhao.com"

__copyright__ = "2014 Peymon & Haoran & Olena"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line

from mining import *



def test_goog():
    google = StockMiner("GOOG", "data/GOOG.json")
    assert google.six_best_months() == [('2007/12', 693.76), ('2007/11', 676.55), ('2007/10', 637.38), ('2008/01', 599.42),
                                 ('2008/05', 576.29), ('2008/06', 555.34)]
    assert google.six_worst_months() == [('2004/08', 104.66),('2004/09', 116.38), ('2004/10', 164.52), ('2004/11', 177.09), ('2004/12', 181.01),
                                  ('2005/03', 181.18)]
def test_com():
    assert compare("GOOG", "data/GOOG.json", "TSE-SO", "data/TSE-SO.json") == ["TSE-SO"]
    assert compare("GOOG", "data/GOOG.json", "GOOG", "data/GOOG.json") == ["Same"]