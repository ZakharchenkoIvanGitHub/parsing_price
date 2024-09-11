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




model = "NE63050S18JE-1070F"


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
    search_page.enter_model(model)
    search_page.click_search_button()
    time.sleep(2)
    search_page.click_compare_button()
    time.sleep(2)
    cards = search_page.get_product_cards()

    i=0
    for item in cards:
        if i:
            price = item.find_element(By.XPATH,"//div[@class = 'p-c-price__price__link']")

            print(item.text)
            print(price.text)
            print()
        i=1



    print("Ждемс")
    time.sleep(30)
    web_driver.quit()
