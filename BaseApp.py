import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """
    Базовые методы для работы с WebDriver
    """

    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://price.ru/"


    def find_element(self, locator, time=10):
        """
        Ищет один элемент и возвращает его
        :param locator: локатор для поиска элемента
        :param time: время ожидания элемента
        :return: объект найденного элемента, в случае ошибки None
        """
        try:
            element = WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator),
                                                             message=f"Element not found {locator}")
        except:
            logging.exception("Find element exception")
            element = None
        return element

    def find_elements(self, locator, time=10):
        """
        Ищет все элементы и возвращает список
        :param locator: локатор для поиска элемента
        :param time: время ожидания элемента
        :return: список объектов найденного элемента, в случае ошибки None
        """
        try:
            element = WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator),
                                                             message=f"Element not found {locator}")
        except:
            logging.exception("Find element exception")
            element = None
        return element

    def get_element_property(self, locator, property):
        """
        Получает css свойство элемента страницы
        :param locator:  локатор для поиска элемента
        :param property: наименование css свойства элемента
        :return: значение css свойства элемента
        """
        element = self.find_element(locator)
        if element:
            return element.value_of_css_property(property)
        else:
            logging.error(f"Property {property} not found no element with locator {locator}")
            return None

    def go_to_site(self):
        """
        Переход на страницу указанную в base_url
        """
        try:
            start_browsing = self.driver.get(self.base_url)
        except:
            logging.exception("Exception while open site")
            start_browsing = None
        return start_browsing

    def get_alert(self, time=10):
        """
        Получает объект всплывающего модального окна в браузере
        :param time: время ожидания элемента
        :return: объект всплывающего модального окна
        """
        try:
            alert = WebDriverWait(self.driver, time).until(EC.alert_is_present(),
                                                           message=f"alert ot found")
            return alert
        except:
            logging.exception("Exception with alert")
            return None
