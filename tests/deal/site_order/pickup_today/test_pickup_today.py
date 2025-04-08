from pages.deals import DealBaseTest
from api.crm_api_client import APIMethods
from data.deal_category import DEAL_CATEGORY
from utils.site_order_data import SiteOrderData
from utils.utils import read_file, write_file, remove_file
import pytest
import allure

params = ["test_case_1.json", "test_case_2.json"]

@pytest.fixture(params=params, scope='session')
def parameters(request):
    return request.param

@allure.feature("Создание сделки 'Заказ с сайта'")
class TestSiteOrder(DealBaseTest):
    
    source_data = None
    deal_category = DEAL_CATEGORY["Бутики"]
    pickup_today = "40"
    deal_stage = "C4:EXECUTING"
    company_id = "37394"
    contact_id = "195342"
    category_id = "4"
    assigned_by_id = "2848"
    store_address = "11"
    
    
    @pytest.fixture(autouse=True)
    def load_data(self, parameters):
        """ Вспомогательная фикстура: получение данных из тестового пакета 
        """
        self.source_data = SiteOrderData(f'data/site_order/pickup_today/{parameters}')
    
    @allure.title("Отправки пакета POST-запросом")
    @pytest.mark.order(1)
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
    
    @allure.title("Проверка создания сделки по REST-методу 'crm.deal.get'")
    @pytest.mark.order(2)
    def test_deal_create_result(self, temp_file, api_client):
        post_result = read_file(temp_file)
        get_result = api_client.request(
            "GET", 
            f"{api_client.method.crm_deal_get}?id={post_result['result']['ID']}"
        )
        with allure.step("Проверка статуса ответа"):
            assert get_result.status_code == 200
            
        write_file(temp_file,get_result.json())
        
        with allure.step("Проверка создания сделки"):
            assert get_result.json()["result"]["ID"] == str(post_result["result"]["ID"])
                
    @allure.title("Проверка полей сделки сделки")
    @pytest.mark.order(3)
    def test_check_deal_type(self, temp_file):
        with allure.step("Проверка типа сделки"):
            if self.source_data.pickup_today == 'Y':
                self.check_deal_property(
                    "TYPE_ID", self.pickup_today, temp_file
                    )
            else:
                raise Exception("pickup_today не равно 'Y'")
    
    @allure.title("Проверка стадии сделки")
    @pytest.mark.order(4)
    def test_check_stage_deal_in_api_response(self, temp_file):
        self.check_deal_property("STAGE_ID", self.deal_stage, temp_file)
    
    @allure.title("Проверка компании в сделке")
    @pytest.mark.order(5)
    def test_check_company_in_deal_in_api_response(self, temp_file):
        self.check_deal_property(
                "COMPANY_ID", self.company_id, temp_file
            )
    
    @allure.title("Проверка компании в сделке")
    @pytest.mark.order(6)
    def test_check_contact_in_deal_in_api_response(self, temp_file):
        self.check_deal_property(
                "CONTACT_ID", self.contact_id, temp_file
            )
    
    @allure.title("Проверка направления сделки")
    @pytest.mark.order(7)
    def test_check_deal_category_in_api_response(self, temp_file):
        self.check_deal_property(
                "CATEGORY_ID", self.category_id, temp_file
            )
    
    @allure.title("Проверка ответственного в сделке")
    @pytest.mark.order(8)
    def test_check_assigned_for_deal_in_api_response(self, temp_file):
        self.check_deal_property(
                "ASSIGNED_BY_ID", self.assigned_by_id, temp_file
            )
            
    @allure.title("Проверка адреса самовывоза")
    @pytest.mark.order(9)
    def test_check_store_address_in_api_response(self, temp_file):
        self.check_deal_property(
                "UF_CRM_1549889644", self.store_address, temp_file
            )
            
    def check_deal_property(self, property_name, expected_value, temp_file):
        """ Вспомогательный метод для проверки свойств сделки """
        data = read_file(temp_file)
        assert data["result"][property_name] == expected_value
    
    @allure.title("Открывает страницу сделки в CRM")
    @pytest.mark.order(10)
    def test_open_deal_page(self, temp_file):
        data = read_file(temp_file)
        deal_id = data["result"]["ID"]
        url = f"{self.deal_details_page.details_url}/{deal_id}/"
        self.deal_details_page.open_page(url)
        self.deal_details_page.switch_to_frame(0)
        
        self.deal_details_page.mark_deal_title_as_test()
        
        deal_id_value = self.deal_details_page.deal_id_field()
        with allure.step("Проверка результата загрузки страницы сделки"):
            assert deal_id_value.text == deal_id
    
    @allure.step("Проверка компании в сделке")
    @pytest.mark.order(11)
    def test_check_company_id_in_crm(self):
        client = self.deal_details_page.client_block()
        company_id = client[0].get_attribute("href").split("/")[-2]
        assert company_id == self.company_id
    
    @allure.step("Проверка контакта в сделке")
    @pytest.mark.order(12)
    def test_check_contact_id_in_deal_crm(self):
        client = self.deal_details_page.client_block()
        contact_id = client[1].get_attribute("href").split("/")[-2]
        assert contact_id == self.contact_id
    
    @allure.title("Открывает товарную часть")
    @pytest.mark.order(13)
    def test_deal_product(self, temp_file):
        
        assert self.deal_product_page.open_products_block(self.deal_category)
        
        self.deal_product_page.click_checkbox_show_availability()
        crm_products = self.deal_product_page.get_products()
        # сохраняет данные по товарам из товарной части
        new_temp_file = temp_file.with_name('crm_products.json')
        write_file(new_temp_file, crm_products)
        
        with allure.step("Проверяет соответствие товарной части"):
            for product in self.source_data.products:
                result = next((crm_product for crm_product in crm_products if product['CODE'] in crm_product['TITLE']), None)
                assert result is not None, f"Отсутствует товар с кодом '{product['CODE']}'"
                assert result['QUANTITY'] == product['QUANTITY']
    
    @allure.title("Проверка стадии сделка на основании наличия товара")
    @pytest.mark.order(14)
    def test_deal_stage_crm(self):
        crm_products = self.deal_product_page.get_products()
        
        self.deal_details_page.click_common_button(self.deal_category)
        deal_stage = self.deal_details_page.deal_stage()
        # Проверяет наличие товара в бутике, филиале и ЦФО. Если товар
        # в наличии хотя бы на одном из складов - возвращает True
        product_availability = all(
            any(crm_product[key] > 0 for key in [
                'STORE_AVAILABLE', 
                'RC_AVAILABLE', 
                'CFD_AVAILABLE'
            ])
            for crm_product in crm_products
        )
        if product_availability:
            with allure.step("Проверка стадии сделки"):
                assert deal_stage.text == "В точку выдачи"
        else:
            with allure.step("Проверка стадии сделки"):
                assert deal_stage.text == "Новый"
        
    @allure.title("Проверка интерфейса резервирования")
    @pytest.mark.order(15)
    def test_reserve_interface_page(self, temp_file):
        data = read_file(temp_file)
        deal_id = data["result"]["ID"]
        
        with allure.step("Открывает интерфейс резервирования"):
            assert self.deal_details_page.click_reserve_interface_button()\
             == f"{self.reserve_interface_page.ri_url}{deal_id}"
    
    @allure.title("Проверка полей 'На резерв' и 'На дозаказ'")
    @pytest.mark.order(16)
    def test_check_reserve_interface_fields(self, temp_file):
        self.reserve_interface_page.switch_to_default_content()
        #считывает файл с товарами из товарной части и удаляет его
        new_temp_file = temp_file.with_name('crm_products.json')
        crm_products = read_file(new_temp_file)
        remove_file(temp_file.parent / new_temp_file)
        
        ir_products = self.reserve_interface_page.get_products()
        for product in crm_products:
            result = next((ir_product for ir_product in ir_products if ir_product['CODE'] in product['TITLE']), None)
            assert result is not None, f"Отсутствует товар '{product['TITLE']}'"
            assert product['STORE_AVAILABLE'] == result['STORE_AVAILABLE'] 
            assert product['RC_AVAILABLE'] == result['RC_AVAILABLE']
            
            if product['STORE_AVAILABLE'] > 0:
                assert product['STORE_AVAILABLE'] == result['TO_RESERVE']
            elif product['RC_AVAILABLE'] > 0:
                assert product['RC_AVAILABLE'] == result['TO_REORDER']
    
    @allure.title("Завершает сделку как тестовую")
    @pytest.mark.order(17)
    def test_close_deal_as_test(self, temp_file):
        data = read_file(temp_file)
        deal_id = data["result"]["ID"]
        url = f"{self.deal_details_page.details_url}/{deal_id}/"
        self.deal_details_page.open_page(url)
        self.deal_details_page.switch_to_frame(0)
        
        self.deal_details_page.change_stage_deal("Завершить сделку")
        self.deal_details_page.click_finish_deal_button("Сделка проиграна")
        failture_status = "Тестовый"
        # ~ self.deal_details_page.click_failture_radio_button(failture_status)
        # ~ deal_stage = self.deal_details_page.deal_stage()
        # ~ assert deal_stage.text = failture_status
