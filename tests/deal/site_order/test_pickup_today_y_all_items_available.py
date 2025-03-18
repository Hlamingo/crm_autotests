from pages.deal_site_order_page import SiteDealCreate
from utils.utils import get_file_path, read_json
import pytest
import allure

@allure.feature("Создание сделки 'Заказ с сайта'")
class TestSiteOrder():
    """ Проверка создания сделки 'Заказ с сайта' """
    response = None
    
    @pytest.fixture(autouse = True)
    def setup(self, api_client):
        self.site_order = SiteDealCreate(api_client)
        
    @allure.title(" Проверка доступности REST метода ")
    def test_check_method_status(self):
        with allure.step("Проверка статуса ответа"):
            assert self.site_order.check_method_status() == 200
    
    @allure.title(" Проверка отправки пакета POST-запросом ")
    def test_make_site_order(self):
        path = get_file_path(
            'data/site_order/pickup_today_y_all_items_available.json'
            )
        data = read_json(path)
        status, TestSiteOrder.response = self.site_order.make_site_order(data)
        with allure.step("Проверка статуса ответа"):
            assert status == 200
        with allure.step("Проверка наличия ID сделки в ответе"):
            assert TestSiteOrder.response["result"]["ID"] is not None
    
    @allure.title(" Проверка создания и стадии сделки ")
    def test_get_deal_details(self):
        deal_id = TestSiteOrder.response["result"]["ID"]
        status, deal_details = self.site_order.get_deal_details(deal_id)
        with allure.step("Проверка статуса ответа"):
            assert status == 200
        with allure.step("Проверка стадии сделки"):
            assert deal_details["result"]["STAGE_ID"] == "C4:EXECUTING"
