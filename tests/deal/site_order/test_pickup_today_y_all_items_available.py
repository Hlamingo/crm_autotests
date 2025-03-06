from pages.deal_site_order_page import SiteOrderPage
from utils.utils import get_file_path, read_json
import pytest
import allure

@pytest.fixture
def site_order(browser, base_url):
    """Фикстура для создания сделки 'Заказ с сайта'"""
    return SiteOrderPage(browser, base_url)

@allure.feature("Создание сделки 'Заказ с сайта'")
class TestSiteOrderPage():
    """ Проверка создания сделки 'Заказ с сайта' """
    
    @pytest.fixture(autouse = True)
    def setup(self, site_order):
        self.site_order = site_order
    
    @allure.feature('Проверка API')
    @allure.story('Проверка статуса REST метода')
    @pytest.mark.order(1)
    def test_check_method_status(self):
        """ Проверка статуса REST метода """
        assert self.site_order.check_method_status() == 200
    
    @pytest.mark.order(2)
    def test_make_site_order(self):
        """ Проверка отправки пакета POST-запросом """
        path = get_file_path(
            'test_data/site_order/pickup_today_y_all_items_available.json'
            )
        data = read_json(path)
        status, response = self.site_order.make_site_order(data)
        assert status == 200
        assert response
