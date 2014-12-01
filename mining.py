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
import numpy as np
from numpy import *
import matplotlib
import matplotlib.pyplot as plt
import tkinter


class StockMiner():
    def __init__(self, stock_name, stock_file_name):
        """
        Initializing function
        :param stock_name: Name of stock
        :param stock_file_name: Name of stock file
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
            numerator = sum([int(item["Volume"]) * float(item["Close"]) for item in value])
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
        if len(self.monthly_averages) < 6:
            raise ValueError("Invalid value. Requires more months.")
        six_best = sorted(self.monthly_averages, key=lambda averages: averages[1], reverse=True)[:6]
        return six_best

    def six_worst_months(self):
        """
        Using monthly averages, report the six worst months with the lowest average stock price.
        :return: The worst six months
        """
        if len(self.monthly_averages) < 6:
            raise ValueError("Invalid value. Requires more months.")
        six_worst = sorted(self.monthly_averages, key=lambda averages: averages[1])[:6]
        return six_worst

    def read_stock_data(self, file_name):
        """
        Read JSON from file.
        :return: Readable JSON file.
        """
        try:
            with open(file_name) as file_handle:
                file_contents = file_handle.read()
        except FileNotFoundError:
            raise FileNotFoundError("File not found")
        return json.loads(file_contents)


"""
BONUS: Compare Two Stocks
Given two stocks identify which of the two has the highest standard deviation of monthly averages.
Your function should return appropriate errors or messages, if it cannot provide a reasonable assessment.
"""


def std(stock):
    """
    Standard deviation function
    :return: The standard deviation of the stock
    """
    i = 0
    stock_ave = 0
    stock_dev = 0
    while i < len(stock):
        stock_ave += stock[i][1]
        i += 1
    mean1 = stock_ave / len(stock)
    for item in stock:
        stock_dev += (item[1] - mean1) ** 2
    return math.sqrt(stock_dev / len(stock))


def compare(stock1, stock1_file, stock2, stock2_file):
    """
    Function to compare two stocks
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


def visual(stock, stock_file):
    stock_list = StockMiner(stock, stock_file)
    time = []
    stock = []
    i = 0
    while i < len(stock_list.monthly_averages):
        time.append(stock_list.monthly_averages[i][0])
        stock.append(stock_list.monthly_averages[i][1])
        i += 1

    date = []
    for i in range(len(time)):
        YYYY, mm, dd = time[i].split("/") + ["1"]
        date.append(datetime.datetime(int(YYYY), int(mm), int(dd)))

    time_np = np.array(date)
    stock_np = np.array(stock)

    best_stocks = sorted(range(len(stock)), key=lambda i: stock[i])[-6:]
    worst_stocks = sorted(range(len(stock)), key=lambda i: stock[i])[:6]

    six_best_time = time_np[best_stocks]
    six_best_stock = stock_np[best_stocks]
    six_worst_time = time_np[worst_stocks]
    six_worst_stock = stock_np[worst_stocks]

    # Plot the three lines
    plt.plot(date, stock)
    plt.plot(six_best_time, six_best_stock, "g^")
    plt.plot(six_worst_time, six_worst_stock, "rs")

    # Include labels
    plt.title("Bonus 2: Stock Price Over Time")
    plt.xlabel("Time")
    plt.ylabel("Stock Price")
    plt.show()


"""
BONUS: Graphical User Interface
Create a graphical user interface for your program.
"""
# create a new window
window = tkinter.Tk()
# title the window
window.title("Stocks")
# resize the window
window.geometry("830x600")
#background colour
window.configure(background="#FFFFFF")

#functions
def best_six_months_display():
    text_box.delete(1.0, tkinter.END)
    text_box.insert(tkinter.CURRENT, "This is the best six months of the 'GOOG' stock \n\n")
    text_box.insert(tkinter.CURRENT, StockMiner("GOOG", "data/GOOG.json").six_best_months())
    text_box.insert(tkinter.CURRENT, "\n\n")
    text_box.insert(tkinter.CURRENT, "This is the best six months of the 'TSE-SO' stock \n\n")
    text_box.insert(tkinter.CURRENT, StockMiner("TSE-SO", "data/TSE-SO.json").six_best_months())


def worst_six_months_display():
    text_box.delete(1.0, tkinter.END)
    text_box.insert(tkinter.CURRENT, "This is the worst six months of the 'GOOG' stock \n\n")
    text_box.insert(tkinter.CURRENT, StockMiner("GOOG", "data/GOOG.json").six_worst_months())
    text_box.insert(tkinter.CURRENT, "\n\n")
    text_box.insert(tkinter.CURRENT, "This is the worst six months of the 'TSE-SO' stock \n\n")
    text_box.insert(tkinter.CURRENT, StockMiner("TSE-SO", "data/TSE-SO.json").six_worst_months())


def compare_stocks():
    text_box.delete(1.0, tkinter.END)
    text_box.insert(tkinter.CURRENT, compare("GOOG", "data/GOOG.json", "TSE-SO", "data/TSE-SO.json"))
    text_box.insert(tkinter.CURRENT,
                    " stock has the highest standard deviation of monthly averages among the two given stock files.")


def visualization_goog():
    text_box.delete(1.0, tkinter.END)
    text_box.insert(tkinter.CURRENT,
                    "A window will now open to show the GOOG stock graph, indicating its best and worst 6 months. \
                    \n \nOnce finished, close the window to return to this page.")
    text_box.insert(tkinter.CURRENT, visual("GOOG", "data/GOOG.json"))


def visualization_tse():
    text_box.delete(1.0, tkinter.END)
    text_box.insert(tkinter.CURRENT,
                    "A window will now open to show the TSE-SO stock graph, indicating its best and worst 6 months. \
                    \n \nOnce finished, close the window to return to this page.")
    text_box.insert(tkinter.CURRENT, visual("TSE-SO", "data/TSE-SO.json"))


def clear_text():
    text_box.delete(1.0, tkinter.END)
    text_box.insert(tkinter.CURRENT, "ALL CLEAR!")


#create the following widget(s)

#label
lbl = tkinter.Label(window, text="Click on the respective button to get the results", fg="#000000")

#text editor
text_box = tkinter.Text(window, wrap=tkinter.WORD, state=tkinter.NORMAL, bg="#000000", fg="#ffffff")

#buttons
btn_best_six = tkinter.Button(window, text="Best Six Months", command=lambda: best_six_months_display())

btn_worst_six = tkinter.Button(window, text="Worst Six Months",
                               command=lambda: worst_six_months_display())

btn_compare = tkinter.Button(window, text="Compare Two Stocks", command=lambda: compare_stocks())

btn_visual_goog = tkinter.Button(window, text="Graph GOOG Stock", command=lambda: visualization_goog())

btn_visual_tse = tkinter.Button(window, text="Graph TSE-SO Stock", command=lambda: visualization_tse())

clear_btn = tkinter.Button(window, text="Clear Screen", command=lambda: clear_text())


#add the widget(s) to window
lbl.pack(side="top")
text_box.pack(side="top")
btn_best_six.pack(side="left")
btn_worst_six.pack(side="left")
btn_compare.pack(side="left")
btn_visual_goog.pack(side="left")
btn_visual_tse.pack(side="left")
clear_btn.pack(side="left", expand="TRUE")


#draw window and start the app
window.mainloop()

