import os
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from search_page import OperationsHelper

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pandas as pd





#model = "NNEAT7100HD46-2080H BULK"

# model_lst = ["NED47TSS19T2-1043J",
#              "NE63050S18JE-1070F",
#              "NE64060T19P1-1070D",
#              "CM8066201927306",
#              "NNEAT7100HD46-2080H BULK"]

model_lst = []


def get_random_chrome_user_agent():
   user_agent = UserAgent(browsers='chrome', os='windows', platforms='pc')
   return user_agent.random


def create_driver(user_id=2):
   options = webdriver.ChromeOptions()
   options.add_argument("start-maximized")
   options.add_experimental_option("excludeSwitches", ["enable-automation"])
   options.add_experimental_option('useAutomationExtension', False)

   script_dir = os.path.dirname(os.path.abspath(__file__))
   base_directory = os.path.join(script_dir, 'users')
   user_directory = os.path.join(base_directory, f'user_{user_id}')

   options.add_argument(f'user-data-dir={user_directory}')
   options.add_argument('--disable-gpu')
   options.add_argument('--disable-dev-shm-usage')
#   options.add_argument("--disable-notifications")
   options.add_argument("--disable-popup-blocking")
   options.add_argument('--no-sandbox')
   options.add_argument("--disable-blink-features=AutomationControlled")
   #options.add_argument('--headless')


   driver = webdriver.Chrome(options=options)



   ua = get_random_chrome_user_agent()
   stealth(driver=driver,
           user_agent=ua,
           languages=["ru-RU", "ru"],
           vendor="Google Inc.",
           platform="Win32",
           webgl_vendor="Intel Inc.",
           renderer="Intel Iris OpenGL Engine",
           fix_hairline=True,
           run_on_insecure_origins=True
           )

   driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
      'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
      '''
   })
   return driver

def parsing ():
    if len(model_lst) == 0:
        text_editor.insert("end", "Данные о моделях не загружены\n\n", "red")
        return
    text_editor.insert("end", f"Запускаю парсинг\n", "green")
    web_driver = create_driver()
    search_page = OperationsHelper(web_driver)
    search_page.go_to_site()

    for model in model_lst:
        search_page.enter_model(model)
        text_editor.insert("end", f"Поиск товара - {model}\n", "green")
        search_page.click_search_button()
        time.sleep(2)


        if search_page.compare_button_found(): # Кнопка сравнить цены
            search_page.click_compare_button()
            time.sleep(2)
            name = search_page.get_name()
            text_editor.insert("end", f"Нашел!  {name}\n", "green")
            cards = search_page.get_product_cards()
            for item in cards:
                price = search_page.get_price(item)
                shop = search_page.get_shop(item)
                text_editor.insert("end", f"{shop} - {price.text}\n", "black")


        elif search_page.model_not_found():
            text_editor.insert("end", f"Товар {model} не найден\n\n", "red")
        else:
            text_editor.insert("end", "!!!!!!!!!!!!!!!!!!!Доработать обработку!!!!!!!!!!!!!!!!!!!!!\n\n", "red")


    print("Ждемс")
    time.sleep(30)
    web_driver.quit()


# открываем файл в текстовое поле
def open_file():
    global model_lst
    filepath = filedialog.askopenfilename()
    if filepath != "":
        df_orders = pd.read_excel(filepath)
        model_lst = [row[0] for i, row in df_orders.iterrows() if row[0] and isinstance(row[0], str) and not row[0] in ["SVGA","CPU","SSD","Код","DDR"] and row[0].find("https")==-1]
        text_editor.insert("end", f"Загрузил из файла модели. {len(model_lst)} шт. \n\n", "green")






        # with open(filepath, "r") as file:
        #     text = file.read()
        #     text_editor.delete("1.0", END)
        #     text_editor.insert("1.0", text)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = Tk()
    root.title("Анализ фильтров")
    root.geometry("1100x600")

    columns = ("name")
    tree = ttk.Treeview(columns=columns, show="headings")
    tree.pack(anchor=NW,fill= Y,expand=True)
    tree.heading("name", text="Имя")
 #  tree.bind("<<TreeviewSelect>>", item_selected)
    tree.column(width=600, column=0)


    text_editor = Text(font="Arial 12")
    text_editor.place(x=600,width=500)

    open_button = ttk.Button(text="Открыть файл", command=open_file)
    open_button.pack(anchor=SW)

    parsing_button = ttk.Button(text="Парсить", command=parsing)
    parsing_button.pack(anchor=SW)


    text_editor.tag_configure("red",  foreground="red")
    text_editor.tag_configure("black", foreground="black")
    text_editor.tag_configure("green", foreground="green")

    root.mainloop()





