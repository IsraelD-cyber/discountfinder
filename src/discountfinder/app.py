"""
Find a discount for a store
"""
import concurrent.futures
import inspect
import time
from functools import partial
#import webbrowser

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from .utils import *

# time elapsed
'''
time1 = time.perf_counter()
icon = toga.Icon(row['Icon'])
time2 = time.perf_counter()
elapsed_time = time2 - time1  # Calculate elapsed time
print(f"{inspect.currentframe().f_lineno}: {elapsed_time:.5f} seconds")
'''

csvFileName = '/resources/discounts.csv'
iconsPath = 'resources/icons/'
PRODUCT_NAME_COL = 1
club_lut = {("1", "בהצדעה")}
WEB_PAGE = 'https://behatsdaa.org.il/'
MAX_ITEMS_IN_DATA_LIST = 10

def init_product_item(row):
    icon = toga.Icon(row[2])
    title = row[0]
    subtitle = row[1]

    return {"icon": icon, "title": title, "subtitle": subtitle}

class DiscountProc:
    def __init__(self, file_path, toga_app):
        self.app_path = file_path
        self.df = read_csv_to_tuples(f"{self.app_path}{csvFileName}", sep='\t')
        self.dict_list = []
        self.dialog_info_msg = ""
        self.toga_app = toga_app
        self.name_input = None
        self.table = None
        self.webview = toga.WebView()
        self.main_container = None

    def main_loop(self):

        self.init_data_dict()
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

        self.main_container = toga.OptionContainer(
            content=[
                ("חיפוש", main_box),
                ("אתר אינטרנט", self.webview),
            ]
        )

        self.toga_app.main_window = toga.MainWindow(title=self.toga_app.formal_name)
        self.toga_app.main_window.content = self.main_container
        self.toga_app.main_window.show()

    def init_data_dict(self):
        time1 = time.perf_counter()
        #pre process
        for row in self.df:
            row[2] = self.app_path / iconsPath / row[2]

        #process
        with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
            # Map the function to each row and collect results
            self.dict_list = list(executor.map(init_product_item, self.df))
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

        time1 = time.perf_counter()

        # process
        self.table.data = []
        for index, row in enumerate(self.df):
            product_name = row[0]
            if title_str in product_name:
                self.table.data.append(self.dict_list[index])
            if len(self.table.data) == MAX_ITEMS_IN_DATA_LIST:
                print(f"data_list length:{MAX_ITEMS_IN_DATA_LIST}")
                break

        time2 = time.perf_counter()
        elapsed_time = time2 - time1  # Calculate elapsed time
        print(f"{inspect.currentframe().f_lineno}: {elapsed_time:.5f} seconds")

    async def list_on_select(self, widget):
        print("list_on_select")
        self.dialog_info_msg = self.table.selection.title
        await self.discount_info_dialog()

    async def discount_info_dialog(self):
        if self.dialog_info_msg != "":
            if await self.toga_app.main_window.dialog(toga.InfoDialog(
                self.dialog_info_msg, "This is discount"
                )) is None:
                await self.discount_question_dialog()

            self.dialog_info_msg = ""

        else:
            await self.toga_app.main_window.dialog(toga.InfoDialog(
                "None", "This is discount"
            ))

    async def discount_question_dialog(self):
        if await self.toga_app.main_window.dialog(toga.QuestionDialog("Toga", "Open Browser?")):
            self.webview.url = WEB_PAGE
            self.main_container.current_tab = 1
        else:
            self.toga_app.main_window.info_dialog(
                "Shucks...", "Well aren't you a spoilsport... :-("
            )

class DiscountFinder(toga.App):
    def startup(self):
        logging.basicConfig(
            level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            handlers=[
                logging.FileHandler(f"{self.paths.app}/log/app.log", mode='w'),  # Log to a file named 'app.log'
                logging.StreamHandler()  # Log to the console
            ]
        )

        dp = DiscountProc(self.paths.app, self)
        dp.main_loop()

def main():
    return DiscountFinder()
