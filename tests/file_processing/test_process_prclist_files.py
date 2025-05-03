from pages.products import ProductsBaseTest, ProductProcessingPage
from utils.utils import read_file
import sqlite3
import pytest
import allure
import time

def prlist_dbf():
    """ Получает список товаров из файла PRLIST.DBF, группирует их 
    по коду товара, возвращает результат"""
    folder_path = "data/prlist_dbf"
    prlist_rows = read_file(f"{folder_path}/PRLIST.DBF")
    sorted_prlist = prlist_rows.sort_values('CODE')
    data = [(code, prlist_data) for code, prlist_data in sorted_prlist.groupby('CODE')]
    
    return data

def products_data_csv():
    """ Получает список товаров из файла ProductsData.csv, группирует их 
    по коду товара, возвращает результат"""
    folder_path = "data/prlist_dbf"
    products_data_rows = read_file(f"{folder_path}/ProductsData.csv")
    sorted_products_data = products_data_rows.sort_values('ProductCode')
    data = [(code, products_data) for code, products_data in sorted_products_data.groupby('ProductCode')]
    
    return data

def products_more_csv():
    """ Получает список товаров из файла ProductsMore.csv, группирует их 
    по коду товара, возвращает результат"""
    folder_path = "data/prlist_dbf"
    products_data_rows = read_file(f"{folder_path}/ProductsMore.csv")
    sorted_products_data = products_data_rows.sort_values('ProductCode')
    data = [(code, products_data) for code, products_data in sorted_products_data.groupby('ProductCode')]
    
@pytest.fixture(scope='session')
def db_connection():
    """ Фикстура для подключения к БД """
    conn = sqlite3.connect("test_data.db")
    yield conn
    conn.close()

@pytest.fixture(scope="session")
def product_properties(base_url, api_client, db_connection):
    """ Фикстура для работы с тестовыми данными из БД """
    # ~ product_processing = ProductProcessingPage(base_url)
    # ~ product_processing.create_crm_products_table(db_connection)
    # ~ product_list = product_processing.product_list(api_client)
    # ~ product_processing.insert_product_list(product_list, db_connection)
    # ~ product_price = product_processing.product_price(api_client)
    # ~ product_processing.update_product_price(product_price, db_connection)
    return db_connection

# ~ @allure.feature("Обработка файлов PRLIST.DBF, ProductsData.csv и ProductsMore.csv")
# ~ @pytest.mark.order(1)
# ~ class TestFileUploadAndProcessing(ProductsBaseTest):
    
    # ~ file_path = "data/prlist_dbf"
    
    # ~ @allure.title("Проверка загрузки файлов на FTP")
    # ~ def test_ftp_file_uploader(self):
        # ~ if self.products_processing_page.environment == "https://crm.l-wine.ru":
            # ~ pytest.skip("Функционал тестируется на production")
        # ~ self.products_processing_page.upload_file_to_ftp(self.file_path)
        
    # ~ @allure.title("Подключается к серверу и запускает скрипт")
    # ~ def test_php_script_runner(self):
        # ~ if self.products_processing_page.environment == "https://crm.l-wine.ru":
            # ~ pytest.skip("Функционал тестируется на production")
        # ~ self.products_processing_page.processing_prlist_dbf(self.file_path)

# ~ @allure.feature("Проверка результата обработки файла PRLIST.DBF")
# ~ @pytest.mark.order(2)
# ~ @pytest.mark.usefixtures('product_properties')
# ~ @pytest.mark.parametrize("product_code, prlist_data", prlist_dbf())
# ~ class TestPrlistDBF(ProductsBaseTest):
    
    # ~ @allure.title("Проверка проставления цен")
    # ~ def test_check_product_price(self, product_code, prlist_data, product_properties):
        # ~ conn = product_properties
        # ~ cur = conn.cursor()
        # ~ cur.execute(f"SELECT * FROM crm_products WHERE PRODUCT_ID={product_code}")
        # ~ db_data = cur.fetchone()
        # ~ assert db_data is not None, f"Код товара {product_code} отсутствует в CRM"
        # ~ self.products_processing_page.check_product_price(prlist_data, db_data)
        

@allure.feature("Проверка результата обработки файла ProductsData.csv")
@pytest.mark.order(3)
@pytest.mark.usefixtures('product_properties')
@pytest.mark.parametrize("code, products_data_csv", products_data_csv())
class TestProductsDataCsv(ProductsBaseTest):
    
    db_data = None
    
    @pytest.fixture(autouse=True)
    def get_db_data_by_product_id(self, code, product_properties):
        """ Возвращает данные по товару из БД"""
        conn = product_properties
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM crm_products WHERE PRODUCT_ID={code}")
        self.db_data = cur.fetchone()
        assert self.db_data is not None, f"Код товара {product_code} отсутствует в CRM"
    
    @allure.title("Проверка свойства 'Наименование'")
    def test_check_property_name(self, code, products_data_csv):
        self.products_processing_page.check_property_name(products_data_csv, self.db_data)
        
    @allure.title("Проверка свойства 'Вес'")
    def test_check_property_weight(self, code, products_data_csv):
        self.products_processing_page.check_property_weight(products_data_csv, self.db_data)
        
    @allure.title("Проверка свойства 'Количество в упаковке'")
    def test_check_property_package_qtt(self, code, products_data_csv):
        self.products_processing_page.check_property_package_qtt(products_data_csv, self.db_data)
        
    @allure.title("Проверка свойства 'Штрих-код'")
    def test_check_property_ean_code(self, code, products_data_csv):
        self.products_processing_page.check_property_ean_code(products_data_csv, self.db_data)
        
    @allure.title("Проверка свойства 'Страна'")
    def test_check_property_country(self, code, products_data_csv):
        self.products_processing_page.check_property_country(products_data_csv, self.db_data)
        
    @allure.title("Проверка свойства 'Объём'")
    def test_check_property_capacity(self, code, products_data_csv):
        self.products_processing_page.check_property_capacity(products_data_csv, self.db_data)
    
    @allure.title("Проверка свойства 'GUID'")
    def test_check_property_guid(self, code, products_data_csv):
        self.products_processing_page.check_property_guid(products_data_csv, self.db_data)
    
    @allure.title("Проверка свойства 'Производитель АГТ'")
    def test_check_property_manufacturer_agt(self, code, products_data_csv):
        self.products_processing_page.check_property_manufacturer_agt(products_data_csv, self.db_data)

# ~ @allure.feature("Проверка результата обработки файла ProductsMore.csv")
# ~ @pytest.mark.order(4)
# ~ @pytest.usefixtures("product_properties")
# ~ @pytest.mark.parametrize("code, products_more_csv", products_more_csv())
# ~ class TestProductsMoreCsv(ProductsBaseTest):
    

