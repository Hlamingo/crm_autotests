from pages.deals import DealBaseTest
from api.crm_api_client import APIMethods
from data.deal_category import DEAL_CATEGORY
from utils.site_order_data import SiteOrderData
from utils.utils import read_file, write_file
import pytest
import allure
import time

deal_properties = {
    'pickup_today': "40",
    'deal_stage': "C4:EXECUTING",
    'company_id': "37394",
    'contact_id': "195342",
    'category_id': "4",
    'assigned_by_id': "2848",
    'store_address': "11"
}

properties_to_check = [
    ("TYPE_ID", "pickup_today"),
    ("STAGE_ID", "deal_stage"),
    ("COMPANY_ID", "company_id"),
    ("CONTACT_ID", "contact_id"),
    ("CATEGORY_ID", "category_id"),
    ("ASSIGNED_BY_ID", "assigned_by_id"),
    ("UF_CRM_1549889644", "store_address"),
]

params = ["test_case_1.json", "test_case_2.json"]

@pytest.fixture(params=params, scope='session')
def parameters(request):
    return request.param

@allure.feature("Создание сделки 'Заказ с сайта'")
class TestSiteOrder(DealBaseTest):
    
    deal_category = DEAL_CATEGORY["Бутики"]
    source_data = None
    
    @pytest.fixture(autouse=True)
    def load_data(self, parameters):
        """ Вспомогательная фикстура: получение данных из тестового пакета 
        """
        self.source_data = SiteOrderData(f'data/site_order/pickup_today/{parameters}')
    
    @allure.title("Отправки пакета POST-запросом")
    def test_check_method_status(self, temp_file, api_client):
        with allure.step("Доступность REST-метода 'site.deal.create'"):
            response = api_client.request(
                "GET", api_client.method.site_deal_create
            )
            assert response.status_code == 200
            
        with allure.step("Отправка пакета POST-запросом"):
            response = api_client.request(
                "POST", api_client.method.site_deal_create, 
                self.source_data.data
            )
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
        with allure.step("Проверка наличия ID сделки в ответе"):
            assert response.json()["result"]["ID"]
        
        write_file(temp_file, response.json())
    
    @allure.title("Проверка свойств сделки по REST-методу 'crm.deal.get'")
    def test_deal_create_result(self, temp_file, api_client):
        post_result = read_file(temp_file)
        get_result = api_client.request(
            "GET", 
            f"{api_client.method.crm_deal_get}?id={post_result['result']['ID']}"
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
        expected = deal_properties[expected_value]
        with allure.step(f"Проверка свойства {expected_value}"):
            assert data["result"][property_name] == expected
    
    @allure.title("Открывает страницу сделки в CRM")
    def test_open_deal_page(self, temp_file):
        data = read_file(temp_file)
        deal_id = data["result"]["ID"]
        url = f"{self.deal_details_page.details_url}/{deal_id}/"
        self.deal_details_page.open_page(url)
        self.deal_details_page.switch_to_frame(0)
        
        deal_id_value = self.deal_details_page.deal_id_field()
        with allure.step("Проверка результата загрузки страницы сделки"):
            assert deal_id_value.text == deal_id
        
        client = self.deal_details_page.client_block()
        company_id = client[0].get_attribute("href").split("/")[-2]
        with allure.step("Проверка компании в сделке"):
            assert company_id == deal_properties["company_id"]
        
        contact_id = client[1].get_attribute("href").split("/")[-2]
        with allure.step("Проверка контакта в сделке"):
            assert contact_id == deal_properties["contact_id"]
    
    @allure.title("Открывает товарную часть")
    def test_deal_product(self, temp_file):
        
        assert self.deal_product_page.open_products_block(self.deal_category)
        
        self.deal_product_page.click_checkbox_show_availability()
        products = self.deal_product_page.get_products()
        
        product_names_ar = [product['title'] for product in products]
        product_qqt_ar = [product['quantity'] for product in products]
        
        with allure.step("Проверяет соответствие товарной части"):
            for product in self.source_data.products:
                assert any(product["CODE"] in product_name_er for product_name_er in product_names_ar)
                assert any(product["QUANTITY"] == product_qtt for product_qtt in product_qqt_ar)
                
        with allure.step("Проверка наличия товаров"):
            
            self.deal_details_page.click_common_button(self.deal_category)
            deal_stage = self.deal_details_page.deal_stage()
            
            product_availability = all(
                any(product[key] > 0 for key in [
                    'store_available', 
                    'rc_available', 
                    'cfd_available'
                ] if key in product)
                for product in products
            )
            if product_availability:
                with allure.step("Проверка стадии сделки"):
                    assert deal_stage.text == "В точку выдачи"
            else:
                with allure.step("Проверка стадии сделки"):
                    assert deal_stage.text == "Новый"
        
    @allure.title("Проверка интерфейса резервирования")
    def test_reserve_interface_page(self, temp_file):
        data = read_file(temp_file)
        deal_id = data["result"]["ID"]
        
        with allure.step("Открывает интерфейс резервирования"):
            assert self.deal_details_page.click_reserve_interface_button()\
             == f"{self.reserve_interface_page.ri_url}{deal_id}"
        
        self.reserve_interface_page.switch_to_default_content()
        products = self.reserve_interface_page.get_products()
        print(products)
    
