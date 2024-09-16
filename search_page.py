from BaseApp import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging
import yaml


class TestSearchLocators:
    """
    Хранит данные о локаторах для поиска тестируемых элементов в виде коллекции словаря
    """
    ids = dict()
    with open("locators.yaml", encoding="utf-8") as f:
        locators = yaml.safe_load(f)
    for locator in locators["xpath"].keys():
        ids[locator] = (By.XPATH, locators["xpath"][locator])


#    for locator in locators["css"].keys():
#        ids[locator] = (By.CSS_SELECTOR, locators["css"][locator])

class OperationsHelper(BasePage):
    """
    Реализует вспомогательные методы для поиска и взаимодействия с элементами веб страницы
    """
  #  with open("config.yaml", encoding="utf-8") as f:
   #     testdata = yaml.safe_load(f)

    # @staticmethod
    # def input_city_to_xpath(locator, city):
    #     """
    #     Вставляет название города в xpath локатора
    #     :param locator: локатор для поиска элемента
    #     :param city: название города
    #     :return: измененный локатор
    #     """
    #     ind = locator[1].find("''")
    #     xpath = f"{locator[1][:ind + 1]}{city}{locator[1][ind + 1:]}"
    #     return locator[0], xpath
    #
    # @staticmethod
    # def get_lat_lon(url):
    #     """
    #     Получает из url адреса широту и долготу
    #     :param url: url адрес
    #     :return:широта и долгота
    #     """
    #     ind = url.find("lat")
    #     lat = url[ind + 4:ind + 15]
    #     ind = url.find("lon")
    #     lon = url[ind + 4:ind + 15]
    #     return lat, lon
    #
    # @staticmethod
    # def get_city_name(full_name):
    #     """
    #     Получает название города
    #     :param full_name: полное название города с указанием региона
    #     :return: название города
    #     """
    #     ind = full_name.find(",")
    #     name = full_name[:ind] if ind != -1 else full_name
    #     return name
    #
    def enter_text_info_field(self, locator, word, description=None):
        """
        Вводит строку текста в поле найденному по локатору
        :param locator: локатор для поиска элемента
        :param word: строка текста
        :param description: описание локатора
        :return: True в случае успеха
        """
        if description:
            element_name = description
        else:
            element_name = locator
        logging.debug(f"Send {word} to element {element_name}")
        field = self.find_element(locator)
        if not field:
            logging.error(f"Element {element_name} not found")
            return False
        try:
            field.clear()
            field.send_keys(word)
        except:
            logging.exception(f"Exception while operation with {element_name}")
            return True
    #
    def click_button(self, locator, description=None):
        """
        Кликает по элементу найденному по локатору
        :param locator: локатор для поиска элемента
        :param description: описание локатора
        :return: True в случае успеха
        """
        if description:
            element_name = description
        else:
            element_name = locator
        button = self.find_element(locator)
        if not button:
            return False
        try:
            button.click()
        except:
            logging.exception("Exception witch click")
        logging.debug(f"Click to element {element_name} button")
        return True

    def get_text_from_element(self, locator, description=None):
        """
        Получает хранящийся в элементе текст
        :param locator: локатор для поиска элемента
        :param description: описание локатора
        :return: True в случае успеха
        """
        if description:
            element_name = description
        else:
            element_name = locator
        field = self.find_element(locator, time=3)
        if not field:
            return None
        try:
            text = field.text
        except:
            logging.exception(f"Exception while get text from {element_name}")
            return None
        logging.debug(f"Find text {text} in field {element_name}")
        return text
    #
    # def get_attribute_from_element(self, locator, attribute, description=None):
    #     """
    #     Получает значение атрибута элемента
    #     :param locator:  локатор для поиска элемента
    #     :param attribute: название атрибута
    #     :param description: описание локатора
    #     :return: значение атрибута
    #     """
    #     if description:
    #         element_name = description
    #     else:
    #         element_name = locator
    #     field = self.find_element(locator, time=3)
    #     if not field:
    #         return None
    #     try:
    #         attr = field.get_attribute(attribute)
    #     except:
    #         logging.exception(f"Exception while get text from {element_name}")
    #         return None
    #     logging.debug(f"Find attribute {attribute} in field {element_name}")
    #     return attr
    #
    # ENTER TEXT
    def enter_model(self, model):
        """
        Вводит название модели в поле ввода
        :param model: название модели
        """
        self.enter_text_info_field(TestSearchLocators.ids["LOCATOR_INPUT_MODEL"], model, description="input_city")

    # # CLICK
    # def press_enter_city(self):
    #     """
    #     Эмулирует нажатие клавиши ENTER
    #     """
    #     self.find_element(TestSearchLocators.ids["LOCATOR_INPUT_CITY"]).send_keys(Keys.ENTER)
    #
    def click_search_button(self):
        """
        Кликает по кнопке поиска
        """
        self.click_button(TestSearchLocators.ids['LOCATOR_SEARCH_BUTTON'],
                          description="click_search_button")
    def click_compare_button(self):
        """
        Кликает по кнопке "Сравнить цены"
        """
        self.click_button(TestSearchLocators.ids['LOCATOR_BUTTON_COMPARE'],
                          description="click_compare_button")
    # GET TEXT
    def get_product_card(self):
        """
        Возвращает первую карточку товара
        """
        return self.find_element(TestSearchLocators.ids["LOCATOR_PRODUCT_CARD"])

    def get_product_cards(self):
        """
        Возвращает список карточек товара
        """

        return self.find_elements(TestSearchLocators.ids["LOCATOR_PRODUCT_CARD"])
        #return self.driver.find_elements(By.XPATH,"//div[@class = 'p-c-price l-container']")

    def get_name(self):
        """
        Возвращает наименование товара
        """
        return self.get_text_from_element(TestSearchLocators.ids["LOCATOR_NAME_PRODUCT"], description="get_name")

    @staticmethod
    def get_price(card):
        """
        Возвращает цену товара из карточки
        """
        return card.find_element(By.XPATH,TestSearchLocators.ids["LOCATOR_PRICE"][1])

    @staticmethod
    def get_shop(card):
        """
        Возвращает название магазина
        """
        return card.find_element(By.XPATH,TestSearchLocators.ids["LOCATOR_SHOP_NAME"][1]).get_attribute("title")



    def model_not_found(self):
        """
        Возвращает TRUE если модель не нашлась
        """
        res = self.find_elements(TestSearchLocators.ids["LOCATOR_EMPTY_STATE"],2)

        if res:
            return True
        else:
            return False

    def compare_button_found(self):
        """
        Возвращает TRUE если кнопка сравнить цены нашлась
        """
        res = self.find_elements(TestSearchLocators.ids["LOCATOR_BUTTON_COMPARE"],2)

        if res:
            return True
        else:
            return False

    #
    # def get_condition(self):
    #     """
    #     Возвращает описание погоды
    #     """
    #     return self.get_text_from_element(TestSearchLocators.ids["LOCATOR_CONDITION"], description="condition")
    #
    # def get_yesterday_temp(self):
    #     """
    #     Возвращает температуру вчера в это время
    #     """
    #     return self.get_text_from_element(TestSearchLocators.ids["LOCATOR_YESTERDAY_TEMP"],
    #                                       description="yesterday_temp")[1:]
    #
    # def get_wind_speed(self):
    #     """
    #     Возвращает скорость ветра
    #     """
    #     return self.get_text_from_element(TestSearchLocators.ids["LOCATOR_WIND_SPEED"], description="wind_speed")
    #
    # def get_wind_dir(self):
    #     """
    #     Возвращает направление ветра
    #     """
    #     return self.get_text_from_element(TestSearchLocators.ids["LOCATOR_WIND_DIR"], description="wind_dir")
    #
    # def get_humidity(self):
    #     """
    #     Возвращает влажность
    #     """
    #     return self.get_text_from_element(TestSearchLocators.ids["LOCATOR_HUMIDITY"], description="humidity")[:-1]
    #
    # def get_pressure(self):
    #     """
    #     Возвращает атмосферное давление
    #     """
    #     return self.get_text_from_element(TestSearchLocators.ids["LOCATOR_PRESSURE"], description="humidity")[:3]
