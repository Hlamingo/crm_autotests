# ~ import os
# ~ import sys
# ~ sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import allure
from pages.deals import DealBaseTest

@allure.feature("Авторизация в CRM")
class TestAuthorization(DealBaseTest):
    """ Проверка авторизации в CRM """
    
    @allure.title("Проверка авторизации в CRM")
    def test_authorization(self):
        self.auth_page.open_page(self.auth_page.base_url)
        self.auth_page.checking_auth_page_is_open()
        self.auth_page.enter_login()
        self.auth_page.enter_password()
        self.auth_page.click_login_button()
        self.auth_page.authorization_error()
        self.auth_page.checking_login_successful
