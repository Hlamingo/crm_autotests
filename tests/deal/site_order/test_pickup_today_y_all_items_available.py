from api.crm_api_client import APIMethods
from utils.utils import read_file, write_file
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

params = [
    "test_case_1.json",
    "test_case_2.json"
]

properties_to_check = [
    ("TYPE_ID", "pickup_today"),
    ("STAGE_ID", "deal_stage"),
    ("COMPANY_ID", "company_id"),
    ("CONTACT_ID", "contact_id"),
    ("CATEGORY_ID", "category_id"),
    ("ASSIGNED_BY_ID", "assigned_by_id"),
    ("UF_CRM_1549889644", "store_address"),
]

@pytest.fixture(params=params, scope='session')
def parameters(request):
    return request.param


@allure.feature("Создание сделки 'Заказ с сайта'")
class TestSiteOrder:
    
    @pytest.fixture(autouse=True)
    def setup(self, deal, api_client):
        self.api = api_client
        self.deal = deal["deal_page"]
        self.method = APIMethods()
        self.deal_properties = DealProperties()
    
    @allure.title("Отправки пакета POST-запросом")
    def test_check_method_status(self, temp_file):
        with allure.step("Доступность REST-метода 'site.deal.create'"):
            response = self.api.request("GET", self.method.site_deal_create)
            assert response.status_code == 200

        data = read_file(f'data/site_order/pickup_today/{temp_file.name}')
        with allure.step("Отправка пакета POST-запросом"):
            response = self.api.request(
                "POST", self.method.site_deal_create, data
            )
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
        with allure.step("Проверка наличия ID сделки в ответе"):
            assert response.json()["result"]["ID"]
        
        write_file(temp_file, response.json())
    
    @allure.title("Проверка свойств сделки по REST-методу 'crm.deal.get'")
    def test_deal_create_result(self, temp_file):
        post_result = read_file(temp_file)
        print(f"\n\n{post_result}\n\n")
        get_result = self.api.request(
            "GET", 
            f"{self.method.crm_deal_get}?id={post_result['result']['ID']}"
        )
        with allure.step("Проверка статуса ответа"):
            assert get_result.status_code == 200
            
        write_file(temp_file,get_result.json())
        
        with allure.step("Проверка ID сделки"):
            assert get_result.json()["result"]["ID"] == str(post_result["result"]["ID"])
                
    @allure.title("Проверка свойств сделки")
    @pytest.mark.parametrize("property_name, expected_value", properties_to_check)
    def test_check_deal_property(self, property_name, expected_value, temp_file):
        data = read_file(temp_file)
        print(data)
        with allure.step(f"Проверка свойства {expected_value}"):
            expected = getattr(self.deal_properties, expected_value)
            assert data["result"][property_name] == expected
            
    @allure.title("Открывает страницу сделки в CRM")
    def test_open_deal_page(self, temp_file):
        data = read_file(temp_file)
        print(f"\n\n{data}\n\n")
        deal_id = data["result"]["ID"]
        self.deal.base_url = f"{self.deal.base_url}/crm/deal/details/{deal_id}/"
        self.deal.open_page(self.deal.base_url)
        self.deal.switch_to_frame(0)
        
        deal_id_value = self.deal.deal_id_field()
        with allure.step("Проверка результата загрузки страницы сделки"):
            assert deal_id_value.text == deal_id
        
        deal_stage = self.deal.deal_stage()
        with allure.step("Проверка стадии сделки"):
            assert deal_stage.text == "В точку выдачи"
        
        client = self.deal.client_block()
        company_id = client[0].get_attribute("href").split("/")[-2]
        with allure.step("Проверка компании в сделке"):
            assert company_id == self.deal_properties.company_id
        
        contact_id = client[1].get_attribute("href").split("/")[-2]
        with allure.step("Проверка контакта в сделке"):
            assert contact_id == self.deal_properties.contact_id

    
# ~ https://54448.crm.taskfactory.ru/crm/deal/details/8659485/
