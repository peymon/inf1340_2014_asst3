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

__copyright__ = "2014 Peymon & Haoran & Olena"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import json
import datetime
import itertools
import math


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
        self.stock_data = self.read_stock_data(stock_file_name)

        self.change_date()
        self.get_averages()

    def change_date(self):
        numerator = 0
        denominator = 0
        for item in self.stock_data:
            if type(item) is not dict:
                raise TypeError("Invalid type")
            if "Date" in item.keys():
                # Change valid date to YYYY/MM format
                y_m_format = datetime.datetime.strptime(item["Date"], "%Y-%m-%d").strftime("%Y/%m")
                item["Date"] = y_m_format
            else:
                raise ValueError ("Invalid value")

    # average of stocks function
    def get_averages(self):
        monthly_numerator = []
        monthly_denominator = []
        """
            Calculation of monthly average prices of a stock.
            average price = (V1 * C1 + V2 * C2)/(V1 + C2), where V is volume price and C is close price.

            Create a tuple with two items: the average for that month and the date (only the month and year).
            Append the tuple for each month to a list.
         """
        for key, value in itertools.groupby(self.stock_data, lambda item: item["Date"]):
            numerator = sum([int(item["Volume"])*float(item["Close"]) for item in value])
            monthly_numerator.append((key, numerator))

        for key, value in itertools.groupby(self.stock_data, lambda item: item["Date"]):
            denominator = sum([int(item["Volume"]) for item in value])
            monthly_denominator.append((key, denominator))
        i=0
        while i < len(monthly_numerator):
            if monthly_numerator[i][0] == monthly_denominator[i][0]:
                self.monthly_averages.append((monthly_numerator[i][0], round(monthly_numerator[i][1]/monthly_denominator[i][1],2)))
            i += 1


    def six_best_months(self):
        """
        Using monthly averages, report the six best months with the highest average stock price.
        :return: The best six months
        """
        six_best = sorted(self.monthly_averages, key=lambda averages: averages[1], reverse=True)[:6]
        return six_best

    def six_worst_months(self):
        """
        Using monthly averages, report the six worst months with the lowest average stock price.
        :return: The worst six months
        """
        six_worst = sorted(self.monthly_averages, key=lambda averages: averages[1])[:6]
        return six_worst

    def read_stock_data(self, file_name):
        """
        Read JSON from file.
        :param file_name: JSON file
        :return:
        """
        with open(file_name) as file_handle:
            file_contents = file_handle.read()
        return json.loads(file_contents)


# standard definition function
def std(stock):
        i = 0
        stock_ave = 0
        stock_dev = 0
        while i < len(stock):
            stock_ave += stock[i][1]
            i += 1
        mean1 = stock_ave/len(stock)
        for item in stock:
            stock_dev += (item[1] - mean1)**2
        return math.sqrt(stock_dev/len(stock))


def compare(stock1, stock1_file, stock2, stock2_file):
        stock1_list = StockMiner(stock1, stock1_file)
        stock2_list = StockMiner(stock2, stock2_file)
        if std(stock1_list.monthly_averages) > std(stock2_list.monthly_averages):
            return [stock1]
        elif std(stock1_list.monthly_averages) < std(stock2_list.monthly_averages):
            return [stock2]
        else:
            return ["Same"]