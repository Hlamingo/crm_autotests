from pages.deal_site_order_page import SiteDealCreate
from utils.utils import get_file_path, read_json
import pytest
import allure

@allure.feature("Создание сделки 'Заказ с сайта'")
class TestSiteOrder():
    """ Проверка создания сделки 'Заказ с сайта' """
    
    @pytest.fixture(autouse = True)
    def setup(self, api_client):
        self.site_order = SiteDealCreate(api_client)
    
    @allure.feature('Проверка API')
    @allure.story('Проверка доступности REST метода')
    @pytest.mark.order(1)
    def test_check_method_status(self):
        """ Проверка статуса REST метода """
        with allure.step("Статуса ответа"):
            assert self.site_order.check_method_status() == 200
    
    @pytest.mark.order(2)
    def test_make_site_order(self):
        """ Проверка отправки пакета POST-запросом """
        path = get_file_path(
            'data/site_order/pickup_today_y_all_items_available.json'
            )
        data = read_json(path)
        status, response = self.site_order.make_site_order(data)
        with allure.step("Статуса ответа"):
            assert status == 200
        with allure.step("Наличие ID сделки в ответе"):
            assert "error" not in response
            assert response["result"]["ID"] is not None
