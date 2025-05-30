from pages.products import ProductsBaseTest
from utils.utils import read_file
from data.product_ad import PRODUCT_AD
import pytest
import allure

@allure.feature("Проверка результата обработки файла ProductsMore.csv")
class TestProductsMoreCsv(ProductsBaseTest):
    
    crm_data = None
    
    @pytest.fixture(autouse=True)
    def get_crm_data_by_product_code(self, code, product_properties_from_crm):
        """ Возвращает данные по товару из БД"""
        if code != code:
            pytest.skip(f"Строка в файле ProductsMore.csv пустая: {code}")
        
        conn = product_properties_from_crm
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM crm_products WHERE PRODUCT_ID={code}")
        self.crm_data = cur.fetchone()
        assert self.crm_data is not None, f"Код товара {product_code} отсутствует в CRM"
    
    @allure.title("Проверка свойства 'Код аналога'")
    def test_analog_code(self, products_more_csv):
        analog_code = products_more_csv.AnalogCode.iloc[0]
        if analog_code.strip().lower() == 'пусто':
            analog_code = '0'
        assert analog_code == self.crm_data[3],\
        f"Ожидаемый {analog_code}, Фактический {self.crm_data[3]}"
        
    @allure.title("Проверка свойства 'Ассортиментная дистрибуция'")
    def test_assortment_distribution(self, products_more_csv):
        
        ass_distrib_csv = products_more_csv.AssDistrib.iloc[0]
        if ass_distrib_csv != ass_distrib_csv: # Проверяем, что ass_distrib_csv = NaN
            ass_distrib_id = None
        else:
            ass_distrib_id = next(key for key, value in PRODUCT_AD.items() if value == ass_distrib_csv)
            
        assert ass_distrib_id == self.crm_data[15],\
        f"Ожидаемый {ass_distrib_id}, Фактический {self.crm_data[15]}"
