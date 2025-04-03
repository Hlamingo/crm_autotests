import os
import sys
# ~ sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import allure

class TestAuthorization:
    """ Проверка авторизации в CRM """
    
    @pytest.fixture(autouse = True)
    def setup(self, auth_page):
        self.auth_page = auth_page
        
    def test_open_auth_page(self):
        """ Проверка доступности страницы """
        self.auth_page.open_page(self.auth_page.base_url)
        auth = self.auth_page.checking_auth_page_is_open()
        assert auth.lower().strip() == "авторизация"
    
    def test_enter_login(self):
        """Проверка ввода логина"""
        self.auth_page.enter_login()
        
    def test_enter_password(self):
        """ Проверка ввода пароля """
        self.auth_page.enter_password()
    
    def test_click_login_button(self):
        """ Проверка нажатия кнопки 'Войти' """
        self.auth_page.click_login_button()
        assert not self.auth_page.authorization_error()
    
    def test_checking_login_successful(self):
        """ Проверяет результат авторизации """
        news = self.auth_page.checking_login_successful()
        assert news.lower().strip() == "новости"
    
