from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import os
from pages.base_page import BasePage

class AuthLocators:
    #Авторизационные данные
    USER_LOGIN = (By.NAME, "USER_LOGIN")
    USER_PASSWORD = (By.NAME, "USER_PASSWORD")
    LOGIN_BUTTON = (By.CSS_SELECTOR, ".login-btn")
    # Локаторы для проверок
    CRM_AUTH = (By.CSS_SELECTOR, ".log-popup-header")
    CRM_NEWS = (By.ID, "pagetitle")
    CRM_AUTH_ERROR = (By.CSS_SELECTOR, ".errortext")
    
class AuthData:
    """ Данные для авторизации """
    load_dotenv()
    LOGIN = os.getenv("LOGIN")
    PASSWORD = os.getenv("PASSWORD")
    
class AuthPage(BasePage):
    """ Авторизация """
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        
    def checking_auth_page_is_open(self):
        """ Возвращает заголовок страницы авторизации"""
        return self.find_element(AuthLocators.CRM_AUTH).text
        
    def enter_login(self):
        """ Вводит логин и возвращает введенное значение"""
        login_field = self.find_element(AuthLocators.USER_LOGIN)
        login_field.send_keys(AuthData.LOGIN)
        assert login_field.get_attribute("value") == AuthData.LOGIN
    
    def enter_password(self):
        """ Вводит пароль и возвращает введенное значение"""
        pass_field = self.find_element(AuthLocators.USER_PASSWORD)
        pass_field.send_keys(AuthData.PASSWORD)
        assert pass_field.get_attribute("value") == AuthData.PASSWORD
    
    def click_login_button(self):
        """ Кликает на кнопку 'Войти'"""
        self.find_element(AuthLocators.LOGIN_BUTTON).click()
    
    def authorization_error(self):
        """ Возвращает текст ошибки авторизации """
        try:
            return self.find_element(AuthLocators.CRM_AUTH_ERROR, 3).text
        except TimeoutException:
            return False
        
    def checking_login_successful(self):
        """ Возвращает заголовок ленты новостей CRM """
        return self.find_element(AuthLocators.CRM_NEWS).text
