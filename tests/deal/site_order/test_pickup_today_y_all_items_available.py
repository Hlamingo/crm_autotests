from pages.deal_page import DealPage
from api.crm_api_client import APIMethods
from tests.base.test_authorization import TestAuthorization
from utils.utils import get_file_path, read_json
import pytest
import allure

class DealProperties:
    def __init__(self):
        self.pickup_today = "40"
        self.deal_stage = "C4:EXECUTING"
        self.company_id = "37394"
        self.contact_id = "195342"
        self.category_id = "4"
        self.assigned_by_id = "2848"
        self.store_address = "11"


@allure.feature("Создание сделки 'Заказ с сайта'")
class TestSiteOrder():
    
    response = None
    
    @pytest.fixture(autouse = True)
    def setup(self, api_client, auth_page, deal_page):
        self.api = api_client
        self.auth_page = auth_page
        self.deal_page = deal_page
        self.method = APIMethods()
        self.deal_properties = DealProperties()
    
    @allure.title(" Проверка доступности REST метода 'site.deal.create'")
    def test_check_method_status(self):
        with allure.step("Проверка статуса ответа"):
            response = self.api.request("GET", self.method.site_deal_create)
            assert response.status_code == 200
        
    @allure.title(" Проверка отправки пакета POST-запросом ")
    def test_make_site_order(self):
        path = get_file_path(
            'data/site_order/pickup_today_test_case_1.json'
            )
        data = read_json(path)
        response = self.api.request("POST", self.method.site_deal_create, data)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
        with allure.step("Проверка наличия ID сделки в ответе"):
            assert response.json()["result"]["ID"]
            TestSiteOrder.response = response
    
    @allure.title(" Проверка свойств сделки по REST-методу 'crm.deal.get'")
    def test_deal_create_result(self):
        deal_id = TestSiteOrder.response.json()["result"]["ID"]
        deal = self.api.request("GET", f"{self.method.crm_deal_get}?id={deal_id}")
        with allure.step("Проверка статуса ответа"):
            assert deal.status_code == 200
        TestSiteOrder.response = deal.json()["result"]
        with allure.step("Проверка ID сделки"):
            assert TestSiteOrder.response["ID"] == str(deal_id)
        with allure.step("Проверка типа сделки"):
            assert TestSiteOrder.response["TYPE_ID"] == self.deal_properties.pickup_today
        with allure.step("Проверка стадии сделки"):
            assert TestSiteOrder.response["STAGE_ID"] == self.deal_properties.deal_stage
        with allure.step("Проверка компании в сделке"):
            assert TestSiteOrder.response["COMPANY_ID"] == self.deal_properties.company_id
        with allure.step("Проверка контакта в сделке"):
            assert TestSiteOrder.response["CONTACT_ID"] == self.deal_properties.contact_id
        with allure.step("Проверка направления сделки"):
            assert TestSiteOrder.response["CATEGORY_ID"] == self.deal_properties.category_id
        with allure.step("Проверка ответственного за сделку"):
            assert TestSiteOrder.response["ASSIGNED_BY_ID"] == self.deal_properties.assigned_by_id
        with allure.step("Проверка адреса самовывоза"):
            assert TestSiteOrder.response["UF_CRM_1549889644"] == self.deal_properties.store_address
            
    @allure.title("Авторизация в CRM")
    def test_auth_page(self):
        auth = TestAuthorization()
        auth.auth_page = self.auth_page
        with allure.step("Проверка доступности страницы"):
            auth.test_open_auth_page()
        with allure.step("Проверка ввода логина"):
            auth.test_enter_login()
        with allure.step("Проверка ввода пароля"):
            auth.test_enter_password()
        with allure.step("Проверка нажатия кнопки 'Войти'"):
            auth.test_click_login_button()
        with allure.step("Проверяет результат авторизации"):
            auth.test_checking_login_successful()
    
    @allure.title("Открывает страницу сделки в CRM")
    def test_open_deal_page(self):
        deal_id = TestSiteOrder.response["ID"]
        self.deal_page.open_deal_page(deal_id)
        deal_id_value = deal.deal_id_field()
        assert deal_id_value == deal_id
        deal_stage = self.deal_page.find_element(self.deal_page.locators.Fields.STAGE_ID).get_attribute("value")
        assert deal_stage == "В точку выдачи"
    # ~ @allure.title("Проверка полей в сделке")
    # ~ def test_check_deal_fields(self):
        # ~ deal = TestSiteOrder.response
        # ~ deal_stage = self.deal_page.find_element(self.deal_page.locators.Fields.STAGE_ID).get_attribute("value")
        # ~ assert deal_stage == "В точку выдачи"
    
# ~ https://54448.crm.taskfactory.ru/crm/deal/details/8659616/
