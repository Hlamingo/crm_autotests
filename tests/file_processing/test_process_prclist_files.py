from pages.products import ProductsBaseTest
from utils.utils import read_file
from pytest_check import check
import pytest
import allure
import time

def data():
    """ Получает список товаров из файла PRLIST.DBF, группирует их 
    по коду товара, возвращает результат"""
    folder_path = "data/prlist_dbf"
    # Получает список товаров из файла PRLIST.DBF 
    prlist_rows = read_file(f"{folder_path}/PRLIST.DBF")
    # Сортирует данные по коду товара
    sorted_prlist = prlist_rows.sort_values('CODE')
    i = 0
    for code, prlist_dbf in sorted_prlist.groupby('CODE'):
        if i == 3:
            break
        i += 1
        # Получает свойство товара из ProductsData.csv
        products_data_csv = read_file(f"{folder_path}/ProductsData.csv")
        # Отфильтровывает данные в соответствии с id товара
        products_data_csv = products_data_csv[products_data_csv['ProductCode']== int(code)]
        if products_data_csv.empty:
            products_data_csv = products_data_csv.empty
        yield {'code': code, 'prlist_dbf': prlist_dbf, 'products_data_csv': products_data_csv}

@pytest.fixture(params=data(), scope='class')
def parameters(request):
    return request.param

@allure.feature("Обработка файлов PRLIST.DBF, ProductsData.csv и ProductsMore.csv")
class TestPrlistProcess(ProductsBaseTest):
    
    file_path = "data/prlist_dbf"
    code = None
    prlist_dbf = None
    products_data_csv = None
    
    @pytest.fixture(autouse = True)
    def test_data(self, parameters):
        self.code = parameters['code']
        self.prlist_dbf = parameters['prlist_dbf']
        self.products_data_csv = parameters['products_data_csv']
    
    # ~ @allure.title("Проверка загрузки файлов на FTP")
    # ~ def test_ftp_file_uploader(self):
        # ~ self.products_processing_page.upload_file_to_ftp(self.file_path)
        
    # ~ @allure.title("Подключается к серверу и запускает скрипт")
    # ~ def test_php_script_runner(self):
        # ~ self.products_processing_page.processing_prlist_dbf(self.file_path)
        
    @allure.title("Проверка результата обработки файлов")
    def test_check_result_prlist_processing(self, api_client, response):
        # Делаем паузу, чтобы не заблокировал сервер
        time.sleep(2)
        with allure.step("Отправка get-запроса на crm.product.list"):
            #Делаем запрос по коду sw, чтобы получить ID товара
            product_sw_id = api_client.request(
            "GET", f"{api_client.method.crm_product_list}?filter[XML_ID]={int(self.code)}"
            )
            assert product_sw_id.status_code == 200, \
            f"crm.product.list не доступен {product_sw_id.status_code}"
            #Если ответ с пустым 'result', то тест провален
            result = product_sw_id.json().get('result', [])
            if not result:
                pytest.fail(f"Товар {self.code} не найден в CRM")
            
            sw_code = product_sw_id.json()['result'][0]['XML_ID']
            
            assert sw_code == self.code.strip(), \
            f"Запрашен XML_ID {self.code}, получен {sw_code}"
        
            product_id = product_sw_id.json()['result'][0]['ID']
        
        with allure.step(f"Отправка get-запроса на crm.product.get. ID товара {product_id}"):
            properties = api_client.request(
            "GET", f"{api_client.method.crm_product_get}?id={product_id}"
            )
            
            assert properties.status_code == 200, f"crm.product.list не доступен {properties.status_code}"
            
            assert properties.json()['result']['ID'] == product_id,\
            f"Запрашен ID {product_id}, получен {properties.json()['result']['ID']}"
            response['response'] = properties.json()
     
    @allure.title("Проверка проставления цен")
    def test_check_product_price(self, response):
        self.skip_test_if_products_data_csv_is_true()
        self.products_processing_page.check_product_price(self.prlist_dbf, response['response'])
        
    @allure.title("Проверка свойства 'Наименование'")
    def test_check_property_name(self, response):
        self.skip_test_if_products_data_csv_is_true()
        self.products_processing_page.check_property_name(self.products_data_csv, response['response'])
        
    @allure.title("Проверка свойства 'Вес'")
    def test_check_property_weight(self, response):
        self.skip_test_if_products_data_csv_is_true()
        self.products_processing_page.check_property_weight(self.products_data_csv, response['response'])
        
    @allure.title("Проверка свойства 'Количество в упаковке'")
    def test_check_property_package_qtt(self, response):
        self.skip_test_if_products_data_csv_is_true()
        self.products_processing_page.check_property_package_qtt(self.products_data_csv, response['response'])
        
    @allure.title("Проверка свойства 'Штрих-код'")
    def test_check_property_ean_code(self, response):
        self.skip_test_if_products_data_csv_is_true()
        self.products_processing_page.check_property_ean_code(self.products_data_csv, response['response'])
        
    @allure.title("Проверка свойства 'Страна'")
    def test_check_property_country(self, response):
        self.skip_test_if_products_data_csv_is_true()
        self.products_processing_page.check_property_country(self.products_data_csv, response['response'])
        
    @allure.title("Проверка свойства 'Объём'")
    def test_check_property_capacity(self, response):
        self.skip_test_if_products_data_csv_is_true()
        self.products_processing_page.check_property_capacity(self.products_data_csv, response['response'])
    
    @allure.title("Проверка свойства 'GUID'")
    def test_check_property_guid(self, response):
        self.skip_test_if_products_data_csv_is_true()
        self.products_processing_page.check_property_guid(self.products_data_csv, response['response'])
    
    @allure.title("Проверка свойства 'Производитель АГТ'")
    def test_check_property_manufacturer_agt(self, response):
        self.skip_test_if_products_data_csv_is_true()
        self.products_processing_page.check_property_manufacturer_agt(self.products_data_csv, response['response'])

    def skip_test_if_products_data_csv_is_true(self):
        """ Вспомогательный метод: проверяет наличие товара в файле 
        ProductsData.csv. Если товар отсутствует - тестовый метод 
        пропускается """
        if self.products_data_csv is True:
            pytest.skip(f"Товар {self.code} отсутствует в ProductsData.csv")
