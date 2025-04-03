from pages.deals import DealBaseTest
from api.crm_api_client import APIMethods
from utils.utils import read_file, write_file
import pytest
import allure

params = ["test_case_1.json", "test_case_2.json"]

@pytest.fixture(params=params, scope='session')
def parameters(request):
    return request.param

@allure.feature("Создание сделки 'Заказ с сайта'")
class TestSiteOrder(DealBaseTest):
    
    @allure.title("Отправки пакета POST-запросом")
    def test_check_method_status(self, temp_file, api_client):
        with allure.step("Доступность REST-метода 'site.deal.create'"):
            response = api_client.request(
                "GET", api_client.method.site_deal_create
            )
            assert response.status_code == 200

        data = read_file(f'data/site_order/pickup_today/{temp_file.name}')
        with allure.step("Отправка пакета POST-запросом"):
            response = api_client.request(
                "POST", api_client.method.site_deal_create, data
            )
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
        with allure.step("Проверка наличия ID сделки в ответе"):
            assert response.json()["result"]["ID"]
        
        write_file(temp_file, response.json())
