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
import numpy
from numpy import *
import matplotlib
import matplotlib.pyplot as plt

class StockMiner():

    def __init__(self, stock_name, stock_file_name):
        """
        :param stock_name: Name of stock
        :param stock_file_name: Name of stock file
        :   return:
        """
        self.stock_name = stock_name
        self.monthly_averages = []
        self.stock_data = self.read_stock_data(stock_file_name)

        self.change_date()
        self.get_averages()

    def change_date(self):
        """
        Change a valid date (YYYY-MM-DD) to YYYY/MM format
        :return: Formatted date
        """
        numerator = 0
        denominator = 0
        for item in self.stock_data:
            if type(item) is not dict:
                raise TypeError("Invalid type")
            if "Date" in item.keys():
                y_m_format = datetime.datetime.strptime(item["Date"], "%Y-%m-%d").strftime("%Y/%m")
                item["Date"] = y_m_format
            else:
                raise ValueError("Invalid value")

    # average of stocks function
    def get_averages(self):
        """
        Calculation of monthly average prices of a stock.
        Average price = (V1 * C1 + V2 * C2)/(V1 + C2), where V is volume price and C is close price.
        Create a tuple with two items: the average for that month and the date (only the month and year).
        Append the tuple for each month to a list.
        :return: A list of tuples for each month
        """
        monthly_numerator = []
        monthly_denominator = []
        for key, value in itertools.groupby(self.stock_data, lambda item: item["Date"]):
            numerator = sum([int(item["Volume"])*float(item["Close"]) for item in value])
            monthly_numerator.append((key, numerator))

        for key, value in itertools.groupby(self.stock_data, lambda item: item["Date"]):
            denominator = sum([int(item["Volume"]) for item in value])
            monthly_denominator.append((key, denominator))
        i = 0
        while i < len(monthly_numerator):
            if monthly_numerator[i][0] == monthly_denominator[i][0]:
                self.monthly_averages.append((monthly_numerator[i][0], round(monthly_numerator[i][1] /
                                                                             monthly_denominator[i][1], 2)))
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
        :param file_name: JSON file.
        :return: Readable JSON file.
        """
        with open(file_name) as file_handle:
            file_contents = file_handle.read()
        return json.loads(file_contents)


"""
BONUS: Compare Two Stocks
Given two stocks identify which of the two has the highest standard deviation of monthly averages.
Your function should return appropriate errors or messages, if it cannot provide a reasonable assessment.
"""


def std(stock):
        """
        Standard deviation function
        :param stock: Name of stock
        :return: The standard deviation of the stock
        """
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
        """
        Function to compare two stocks
        :param stock1: Name of one stock
        :param stock1_file: File of one stock
        :param stock2: Name of the second stock
        :param stock2_file: File of second stock
        :return: The stock that has the highest standard deviation of monthly averages
        """
        stock1_list = StockMiner(stock1, stock1_file)
        stock2_list = StockMiner(stock2, stock2_file)
        if std(stock1_list.monthly_averages) > std(stock2_list.monthly_averages):
            return [stock1]
        elif std(stock1_list.monthly_averages) < std(stock2_list.monthly_averages):
            return [stock2]
        else:
            return ["Same"]


"""
BONUS: Visualize
Create a visualization of the average monthly stock prices over time.
Indicate the six best months and six worst months.
"""

"""
stock_list = StockMiner(stock, stock_file)
time = [stock_list.monthly_averages[i][0] for i in range(stock_list.span())]
stock_price = [stock_list.monthly_averages[i][1] for i in range(stock_list.span())]

date = list()
for i in range(len(time)):
    YYYY, mm = time[i].split("/")
    date.append(datetime.datetime(int(YYYY), int(mm)))

time_np = np.array(date)
stock_price_np = np.array(stock_price)

best_stocks = sorted(range(len(stock_price)), key=lambda i: stock_price[i])[-6:]
worst_stocks = sorted(range(len(stock_price)), key=lambda i: stock_price[i])[:6]

six_best_time = time_np[best_stocks]
six_best_price = stock_price_np[best_stocks]
six_worst_time = time_np[worst_stocks]
six_worst_price = stock_price_np[worst_stocks]

#Plot the three lines
plt.plot(time, stock_price)
plt.plot(six_best_time, six_best_price, "g^")
plt.plot(six_worst_time, six_worst_price, "rs")

#Include labels
plt.title("Bonus 2: Stock Price Over Time")
plt.xlabel("Time")
plt.ylabel("Stock Price")
plt.savefig("example2.png")
plt.show()
"""

"""
BONUS: Graphical User Interface
Create a graphical user interface for your program.
"""