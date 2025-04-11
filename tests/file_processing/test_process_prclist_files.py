from pages.products import ProductsBaseTest, ProductProcessingPage
from utils.utils import write_file, read_file
import pytest
import allure
import time

@pytest.fixture
def prlist_data(base_url):
    """ Фикстура возвращает тестовые данные """
    file_path = "data/prlist_dbf"
    products_processing_page = ProductProcessingPage(base_url)
    prlist = products_processing_page.get_prlist_dbf_data(file_path)
    
    for code, parlist_data in prlist:
        product_data = products_processing_page.get_products_data_csv_data(file_path, code)
        return {'code': code, 'parlist_data': parlist_data, "product_data": product_data}

@pytest.fixture(scope = 'class')
def response():
    data = {'response': None}
    yield data

class TestPrlistProcess(ProductsBaseTest):
    
    file_path = "data/prlist_dbf"
    
    # ~ @allure.title("Проверка загрузки файлов на FTP")
    # ~ def test_ftp_file_uploader(self):
        # ~ self.products_processing_page.upload_file_to_ftp(self.file_path)
        
    # ~ @allure.title("Подключается к серверу и запускает скрипт")
    # ~ def test_php_script_runner(self):
        # ~ self.products_processing_page.processing_prlist_dbf(self.file_path)
        
    @allure.title("Проверка результата обработки файлов")
    def test_check_result_prlist_processing(self, api_client, response, prlist_data):
        
        with allure.step("Отправка get-запроса на crm.product.list"):
            product_id = api_client.request(
            "GET", f"{api_client.method.crm_product_list}?filter[XML_ID]={int(prlist_data['code'])}"
            )
            assert product_id.status_code == 200, f"crm.product.list не доступен {product_id.status_code}"
            assert product_id.json()['result'][0]['XML_ID'] == prlist_data['code'].strip(), \
            f"Ответ не соответствует запросу. Запрашиваемый XML_ID {prlist_data['code']}, \
            получен {product_id.json()['result'][0]['XML_ID']}"
        
        with allure.step(f"Отправка get-запроса на crm.product.get. ID - товара {product_id.json()['result'][0]['ID']}"):
            properties = api_client.request(
            "GET", f"{api_client.method.crm_product_get}?id={product_id.json()['result'][0]['ID']}"
            )
            assert properties.status_code == 200, f"crm.product.list не доступен {properties.status_code}"
            assert properties.json()['result']['ID'] == product_id.json()['result'][0]['ID']
            response['response'] = properties.json()
    
    def test_check_product_price(self, response, prlist_data):
        properties = response['response']
        self.products_processing_page.check_product_price(prlist_data['parlist_data'], response['response'])
        
    def test_check_property_name(self, response, prlist_data):
        properties = response['response']
        self.products_processing_page.check_property_name(prlist_data['product_data'], properties)
        
    def test_check_property_weight(self, response, prlist_data):
        properties = response['response']
        self.products_processing_page.check_property_weight(prlist_data['product_data'], properties)
        
    def test_check_property_package_qtt(self, response, prlist_data):
        properties = response['response']
        self.products_processing_page.check_property_package_qtt(prlist_data['product_data'], properties)
    
    def test_check_property_ean_code(self, response, prlist_data):
        properties = response['response']
        self.products_processing_page.check_property_ean_code(prlist_data['product_data'], properties)
        
    def test_check_property_country(self, response, prlist_data):
        properties = response['response']
        self.products_processing_page.check_property_country(prlist_data['product_data'], properties)
        
    def test_check_property_capacity(self, response, prlist_data):
        properties = response['response']
        self.products_processing_page.check_property_capacity(prlist_data['product_data'], properties)
        
    def test_check_property_guid(self, response, prlist_data):
        properties = response['response']
        self.products_processing_page.check_property_guid(prlist_data['product_data'], properties)
        
    def test_check_property_manufacturer_agt(self, response, prlist_data):
        properties = response['response']
        self.products_processing_page.check_property_manufacturer_agt(prlist_data['product_data'], properties)
        
