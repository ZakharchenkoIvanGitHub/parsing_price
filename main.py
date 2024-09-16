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




#model = "NNEAT7100HD46-2080H BULK"

model_lst = ["NED47TSS19T2-1043J",
             "NE63050S18JE-1070F",
             "NE64060T19P1-1070D",
             "CM8066201927306",
             "NNEAT7100HD46-2080H BULK"]



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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    web_driver = create_driver()
    search_page = OperationsHelper(web_driver)
    search_page.go_to_site()

    for model in model_lst:
        search_page.enter_model(model)
        print(f"Поиск товара - {model}")
        search_page.click_search_button()
        time.sleep(2)


        if search_page.compare_button_found(): # Кнопка сравнить цены
            search_page.click_compare_button()
            time.sleep(2)
            name = search_page.get_name()
            print(f"Нашел!  {name}")
            cards = search_page.get_product_cards()
            for item in cards:
                price = search_page.get_price(item)
                shop = search_page.get_shop(item)
                print(f"{shop} - {price.text}")
            print()
        elif search_page.model_not_found():
            print(f"Товар {model} не найден/n")

        else:
            print("!!!!!!!!!!!!!!!!!!!Доработать обработку!!!!!!!!!!!!!!!!!!!!!/n")


    print("Ждемс")
    time.sleep(30)
    web_driver.quit()
