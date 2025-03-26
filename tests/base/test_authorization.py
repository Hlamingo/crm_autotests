import os
import sys
# ~ sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.auth_page.authorization_page import AuthData
import pytest
import allure

class TestAuthorization:
    """ Проверка авторизации в CRM """
    
    @pytest.fixture(autouse = True)
    def setup(self, auth_page):
        self.auth_page = auth_page
        
    def test_open_auth_page(self):
        """ Проверка доступности страницы """
        self.auth_page.open_page()
        auth = self.auth_page.checking_auth_page_is_open()
        assert auth.lower().strip() == "авторизация"
    
    def test_enter_login(self):
        """Проверка ввода логина"""
        assert self.auth_page.enter_login() == AuthData.LOGIN
        
    def test_enter_password(self):
        """ Проверка ввода пароля """
        assert self.auth_page.enter_password() == AuthData.PASSWORD
    
    def test_click_login_button(self):
        """ Проверка нажатия кнопки 'Войти' """
        self.auth_page.click_login_button()
        assert not self.auth_page.authorization_error()
    
    def test_checking_login_successful(self):
        """ Проверяет результат авторизации """
        news = self.auth_page.checking_login_successful()
        assert news.lower().strip() == "новости"
    
