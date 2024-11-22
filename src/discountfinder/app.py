"""
Find a discount for a store
"""
import inspect
import time
from datetime import datetime
from types import NoneType

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import pandas as pd
import csv
from .utils import *

csvFileName = '/resources/discounts.csv'
iconsPath = 'resources/icons/'
PRODUCT_NAME_COL = 1
club_lut = {("1", "בהצדעה")}

class DiscountProc:
    def __init__(self, file_path, toga_app):
        self.file_path = file_path
        self.df = pd.read_csv(f"{file_path}{csvFileName}", sep='\t')
        self.dict_list = []
        self.dialog_info_msg = ""
        self.toga_app = toga_app
        self.name_input = None
        self.table = None
    def main_loop(self):
        print(f"{inspect.currentframe().f_lineno}{time.time()}")
        self.init_data_dict()
        print(f"{inspect.currentframe().f_lineno}{time.time()}")
        name_label = toga.Label(
            "חיפוש: ",
            style=Pack(padding=(0, 5)),
        )
        self.name_input = toga.TextInput(style=Pack(flex=1), on_change=self.text_input_on_change)

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(self.name_input)
        name_box.add(name_label)

        self.table = toga.DetailedList(style=Pack(flex=1), on_select=self.list_on_select)
        self.init_table()

        main_box = toga.Box(style=Pack(direction=COLUMN))
        main_box.add(name_box)
        main_box.add(self.table)
        self.toga_app.main_window = toga.MainWindow(title=self.toga_app.formal_name)
        self.toga_app.main_window.content = main_box
        self.toga_app.main_window.show()

    def init_data_dict(self):
        for index, row in self.df.iterrows():
            time1 = time.perf_counter()
            '''
            print(f"Index: {index}, Row Data: {row.to_dict()}")
            # Access column values by name
            print(f"Value in 'column_name': {row['Name']}")
            '''
            if len(row) < 3:
                print("warning, row less than 4 columns")
                continue
            icon = toga.Icon(self.file_path / iconsPath / row['Icon'])
            time2 = time.perf_counter()
            elapsed_time = time2 - time1  # Calculate elapsed time
            print(f"{inspect.currentframe().f_lineno}: {elapsed_time:.5f} seconds")
            title = row['Name']
            subtitle = row['Discount']
            data_dict = {"icon": icon, "title": title, "subtitle": subtitle}
            time1 = time.perf_counter()
            elapsed_time = time1 - time2  # Calculate elapsed time
            print(f"{inspect.currentframe().f_lineno}: {elapsed_time:.5f} seconds")
            self.dict_list.append(data_dict)
            time2 = time.perf_counter()
            elapsed_time = time2 - time1  # Calculate elapsed time
            print(f"{inspect.currentframe().f_lineno}: {elapsed_time:.5f} seconds")

    async def text_input_on_change(self, widget):
        print("text_input_on_change")
        self.init_table(self.name_input.value)

    def init_table(self, title_str = ''):
        if title_str == '':
            self.table.data = []
            return

        data = []
        for data_dict in self.dict_list:
            product = data_dict["title"]
            if title_str in product:
                data.append(data_dict)
        self.table.data = data

    async def list_on_select(self, widget):
        print("list_on_select")
        self.dialog_info_msg = self.table.selection.title
        await self.discount_info_dialog()

    async def discount_info_dialog(self):
        if self.dialog_info_msg != "":
            await self.toga_app.main_window.dialog(toga.InfoDialog(
                self.dialog_info_msg, "This is discount"
            ))
            self.dialog_info_msg = ""
        else:
            await self.toga_app.main_window.dialog(toga.InfoDialog(
                "None", "This is discount"
            ))

class DiscountFinder(toga.App):
    def startup(self):
        dp = DiscountProc(self.paths.app, self)
        dp.main_loop()

def main():
    return DiscountFinder()
