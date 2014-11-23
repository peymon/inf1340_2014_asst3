#!/usr/bin/env python3

"""
Assignment 3 - Data Mining
INF1340H, Fall 2014
Deadline: December 1, 2014 at 11:59pm.

Objectives: perform data mining on the prices of stock data,
            calculate the monthly average prices of a stock,
            and report the 6 best and 6 worst months.
"""

__author__ = 'Peymon & Haoran & Olena'
__email__ = "OlePeyHao@olepeyhao.com"

__copyright__ = "Peymon & Haoran & Olena"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import json
import datetime

#stock_data = []
#monthly_averages = []


class StockMiner():
    """
    Information about a stock.
    """

    def __init__(self, stock_name, stock_file_name):
        """

        :param stock_name:
        :param stock_file_name:
        :   return:
        """
        self.stock_name = stock_name
        self.monthly_averages = []
        self.stock_data = self.read_json_from_file(stock_file_name)

        for item in self.stock_data:
            if type(item) is not dict:
                raise TypeError("Invalid type")

            ## Check for valid date
            #if valid_date = datetime.datetime.strptime(item["Date"], "%Y-%m-%d"):
            #    return True
            #else:
            #     return False

            if "Date" in item.keys():
                # Change valid date to YYYY/MM format
                y_m_format = datetime.datetime.strptime(item["Date"], "%Y-%m-%d").strftime("%Y-%m")

            else:
                raise ValueError ("Invalid value")

            """
            Calculation of monthly average prices of a stock.
            average price = (V1 * C1 + V2 * C2)/(V1 + C2), where V is volume price and C is close price.
            """
            if "Volume" in item.keys() and "Close" in item.keys:
                if type(item["Volume"]) is int and (type(item["Close"])) is int or type(item["Close"]) is float):
                    numerator += item["Volume"] * item["Close"]
                    denominator += item["Volume"]
            else:
                    raise TypeError ("Invalid Type)"

            """
            Create a tuple with two items: the average for that month and the date (only the month and year).
            Append the tuple for each month to a list.
            """
                self.monthly_averages.append(y_m_format, round(numerator/denominator, 2)))


    def six_best_months():
        """
        Using monthly averages, report the six best months with the highest average stock price.
        :return: The best six months
        """
        six_best = sorted(self.monthly_averages, key=lambda averages: averages[1], reverse=True)[:6]
        return six_best
        # return [('', 0.0), ('', 0.0), ('', 0.0), ('', 0.0), ('', 0.0), ('', 0.0)]


    def six_worst_months():
        """
        Using monthly averages, report the six worst months with the lowest average stock price.
        :return: The worst six months
        """
        six_worst = sorted(self.monthly_averages, key=lambda averages: averages[1])[:6]
        return six_worst
        #return [('', 0.0), ('', 0.0), ('', 0.0), ('', 0.0), ('', 0.0), ('', 0.0)]



#def read_json_from_file(file_name):
#    """
#    Read JSON from file.
#    :param file_name: JSON file
#    :return:
#    """
#    with open(file_name) as file_handle:
#        file_contents = file_handle.read()
#    return json.loads(file_contents)
