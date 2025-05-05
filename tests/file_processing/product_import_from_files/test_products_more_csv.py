from pages.products import ProductsBaseTest
from utils.utils import read_file
from data.product_ad import PRODUCT_AD
import pytest
import allure

def products_more_csv():
    """ Получает список товаров из файла ProductsMore.csv, группирует их 
    по коду товара, возвращает результат"""
    folder_path = "data/prlist_dbf"
    products_data_rows = read_file(f"{folder_path}/ProductsMore.csv")
    sorted_products_data = products_data_rows.sort_values('ProductCode')
    data = [(code, products_data) for code, products_data in sorted_products_data.groupby('ProductCode')]
    
    return data
    
@allure.feature("Проверка результата обработки файла ProductsMore.csv")
@pytest.mark.parametrize("code, products_more_csv", products_more_csv())
class TestProductsMoreCsv(ProductsBaseTest):
    
    db_data = None
    
    @pytest.fixture(autouse=True)
    def get_db_data_by_product_id(self, code, product_properties):
        """ Возвращает данные по товару из БД"""
        if code != code:
            pytest.skip(f"Строка в файле ProductsMore.csv пустая: {code}")
        
        conn = product_properties
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM crm_products WHERE PRODUCT_ID={code}")
        self.db_data = cur.fetchone()
        assert self.db_data is not None, f"Код товара {product_code} отсутствует в CRM"
    
    @allure.title("Проверка свойства 'Код аналога'")
    def test_analog_code(self, products_more_csv):
        analog_code = products_more_csv.AnalogCode.iloc[0]
        if analog_code.strip().lower() == 'пусто':
            analog_code = '0'
        assert analog_code == self.db_data[3],\
        f"Ожидаемый {analog_code}, Фактический {self.db_data[3]}"
        
    @allure.title("Проверка свойства 'Ассортиментная дистрибуция'")
    def test_assortment_distribution(self, products_more_csv):
        
        ass_distrib_csv = products_more_csv.AssDistrib.iloc[0]
        if ass_distrib_csv != ass_distrib_csv: # Проверяем, что ass_distrib_csv = NaN
            ass_distrib_id = None
        else:
            ass_distrib_id = next(key for key, value in PRODUCT_AD.items() if value == ass_distrib_csv)
            
        assert ass_distrib_id == self.db_data[15],\
        f"Ожидаемый {ass_distrib_id}, Фактический {self.db_data[15]}"
