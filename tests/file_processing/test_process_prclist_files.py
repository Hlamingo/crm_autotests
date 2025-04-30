from pages.products import ProductsBaseTest
from utils.utils import read_file
from fast_bitrix24 import Bitrix
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

# ~ @pytest.fixture(params=data(), scope='class')
# ~ def parameters(request):
    # ~ return request.param
    
@pytest.fixture(scope = 'session')
def product_properties(api_client):
    """ Фикстура извлекает свойства товаров из CRM и сохраняет в БД """
    bx = Bitrix(api_client.base_url)
    product_list = bx.get_all(
        'catalog.product.list',
        params = {
        "filter": {"iblockId": 27},
        "select": ["id", "iblockId", "price", "name", "property135",
            "property883", "property731", "property731", "property151",
            "property626", "property541", "property339","property244",
            "property728","property739", "property304","property737"
            ]}
        )
    conn = sqlite3.connect(':memory:')
    cur = conn.cursor()
    create_table = """ CREATE TABLE IF NOT EXISTS crm_products (
    ID INTENGER, NAME TEXT, PRODUCT_ID TEXT, STIE_PRICE TEXT, MOC_PRICE TEXT,
    MRC_PRICE TEXT, RRC_PRICE TEXT, UNIT_WEIGHT TEXT, PACKAGE_QTY TEXT,
    EAN_CODE TEXT, PROD_CATEGORY_NAME TEXT, СAPACITY TEXT, GUID TEXT,
    MANUFACTURER TEXT)"""
    
    for i in range(0, len(product_list), 100):
        batch = product_list[i:i + 100]
        data_to_insert = [(
            product.get('id'),
            product.get('name'),
            product.get('property135', {}).get('value') if product.get('property135') else None,
            product.get('property883', {}).get('value') if product.get('property883') else None,
            product.get('property731', {}).get('value') if product.get('property731') else None,
            product.get('property151', {}).get('value') if product.get('property151') else None,
            product.get('property626', {}).get('value') if product.get('property626') else None,
            product.get('property541', {}).get('value') if product.get('property541') else None,
            product.get('property339', {}).get('value') if product.get('property339') else None,
            product.get('property244', {}).get('value') if product.get('property244') else None,
            product.get('property728', {}).get('value') if product.get('property728') else None,
            product.get('property739', [{}])[0].get('value') if product.get('property739') else None,
            product.get('property304', {}).get('value') if product.get('property304') else None,
            product.get('property737', {}).get('value') if product.get('property737') else None
            )for product in batch
        ]
        cur.executemany("INSERT INTO crm_products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data_to_insert)
        
    conn.commit()
    
    bx = Bitrix(webhook)
    product_prices = bx.get_all(
        'crm.product.list',
        params={"select":["ID","PRICE"]})
    cur.execute("PRAGMA table_info(crm_products)")
    columns = [column[1] for column in cur.fetchall()]
    
    if "PRICE" not in columns:
        cur.execute("ALTER TABLE crm_products ADD COLUMN PRICE TEXT")
        
    update_query = """ UPDATE crm_products SET PRICE = CASE ID {cases} END WHERE ID IN ({ids}) """
    
    cases = []
    ids = []
    
    for product in product_prices:
        product_id = product['ID']
        price = product['PRICE']
        
        if product_id is not None:
            if price is None:
                cases.append(f"WHEN {product_id} THEN NULL")
            else:
                cases.append(f"WHEN {product_id} THEN '{price}'")
            ids.append(product_id)
        ids.append(product_id)
    
    update_query = update_query.format(cases=' '.join(cases), ids=','.join(ids))
    
    cur.execute(update_query)
    conn.commit()
    yield conn
    conn.close()
    
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

@allure.feature("Проверка результата обработки файлов PRLIST.DBF, \
                ProductsData.csv, ProductsMore.csv")
@pytest.mark.order(2)
@pytest.mark.usefixtures('product_properties')
@pytest.mark.parametrize("code, products_data_csv", products_data_csv())
class TestProductProperties(ProductsBaseTest):
    
    db_data = None
    
    @pytest.fixture(autouse=True)
    def get_db_databy_product_id(self, code, products_data_csv, product_properties):
        """ Возвращает данные по товару из БД"""
        conn = product_properties
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM crm_products WHERE PRODUCT_ID={code}")
        self.db_data = cur.fetchone()
    
    # ~ @allure.title("Проверка проставления цен")
    # ~ @pytest.mark.parametrize("product_code, prlist_data", prlist_dbf())
    # ~ def test_check_product_price(self, product_code, prlist_data):
        # ~ conn = product_properties
        # ~ cur = conn.cursor()
        # ~ cur.execute(f"SELECT * FROM crm_products WHERE PRODUCT_ID={product_code}")
        # ~ db_data = cur.fetchone()
        # ~ self.products_processing_page.check_product_price(prlist_data, db_data)
        
    @allure.title("Проверка свойства 'Наименование'")
    def test_check_property_name(self, code, products_data_csv):
        self.products_processing_page.check_property_name(products_data_csv)
        
    @allure.title("Проверка свойства 'Вес'")
    def test_check_property_weight(self, code, products_data):
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
