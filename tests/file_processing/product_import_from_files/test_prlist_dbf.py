from pages.products import ProductsBaseTest
from utils.server_client import ServerClient
from utils.utils import read_file
import pytest
import allure

def pytest_generate_tests(metafunc):
    """ Получает список товаров из файла PRLIST.DBF, группирует их 
    по коду товара, возвращает результат"""
    if metafunc.config.getoption("env") == "dev":
        server_client = ServerClient("https://54448.crm.taskfactory.ru")
        content = server_client.ftp_file_reader("PRLIST.DBF")
        prlist_rows = read_file(file_content=content)
        print(prlist_rows)
        sorted_prlist = prlist_rows.sort_values('CODE')
        data = [(code, prlist_data) for code, prlist_data in sorted_prlist.groupby('CODE')]
    else:
        folder_path = "data/prlist_dbf"
        prlist_rows = read_file(f"{folder_path}/PRLIST.DBF")
        sorted_prlist = prlist_rows.sort_values('CODE')
        data = [(code, prlist_data) for code, prlist_data in sorted_prlist.groupby('CODE')]
        
    metafunc.parametrize("product_code, prlist_data", data)

@allure.feature("Проверка результата обработки файла PRLIST.DBF")
class TestPrlistDBF(ProductsBaseTest):
    
    db_data = None
    prlist_data = None
    
    @pytest.fixture(autouse=True)
    def test_prlist_dbf_data(self, product_code, prlist_data, product_properties):
        print(product_code)
        conn = product_properties
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM crm_products WHERE PRODUCT_ID={product_code}")
        self.db_data = cur.fetchone()
        if self.db_data is None:
            pytest.fail( f"Код товара {product_code} отсутствует в CRM")
        self.prlist_data = {row['PAYFORM_ID']:row['PRICE'] for index, row in prlist_data.iterrows() if row['PAYFORM_ID'] not in [200501, 200084]}
    
    @allure.title("Проверка типа цены 'САЙТ'")
    def test_check_site_price(self, product_code):
        if 200502 not in self.prlist_data:
            pytest.skip(f"Для товара {product_code} отсутствует запись с PAYFORM_ID = 200502 в файле")
        assert float(self.prlist_data[200502]) == float(self.db_data[4]),\
        f"Ошибка в цене САЙТ: Ожидаемый {self.prlist_data[200502]}, Фактический {self.db_data[4]}"
    
    @allure.title("Проверка типа цены 'МОЦ'")
    def test_check_moc_price(self, product_code):
        if 200127 not in self.prlist_data:
            pytest.skip(f"Для товара {product_code} отсутствует запись с PAYFORM_ID = 200127 в файле")
        assert float(self.prlist_data[200127]) == float(self.db_data[5]),\
        f"Ошибка в цене МОЦ: Ожидаемый {self.prlist_data[200127]}, Фактический {self.db_data[5]}"
    
    @allure.title("Проверка типа цены 'МРЦ'")
    def test_cgeck_mrc_price(self, product_code):
        if 200125 not in self.prlist_data:
            pytest.skip(f"Для товара {product_code} отсутствует запись с PAYFORM_ID = 200125 в файле")
        assert float(self.prlist_data[200125]) == float(self.db_data[6]),\
        f"Ошибка в цене МРЦ: Ожидаемый {self.prlist_data[200125]}, Фактический {self.db_data[6]}"
    
    @allure.title("Проверка типа цены 'РРЦ'")
    def test_check_rrc_price(self, product_code):
        if 200500 not in self.prlist_data:
            pytest.skip(f"Для товара {product_code} отсутствует запись с PAYFORM_ID = 200500 в файле")
        assert float(self.prlist_data[200500]) == float(self.db_data[7].split("|")[0]),\
        f"Ошибка в цене РРЦ: Ожидаемый {self.prlist_data[200500]}, Фактический {self.db_data[7].split('|')[0]}"

    @allure.title("Проверка базовой цены (Розничная цена)")
    def test_check_base_price(self, product_code):
        if 200114 not in self.prlist_data:
            pytest.skip(f"Для товара {product_code} отсутствует запись с PAYFORM_ID = 200114 в файле")
        assert float(self.prlist_data[200114]) == float(self.db_data[16]),\
        f"Ошибка в Розничной (Базовой) цене: Ожидаемый {self.prlist_data[200114]}, Фактический {self.db_data[16]}" 
