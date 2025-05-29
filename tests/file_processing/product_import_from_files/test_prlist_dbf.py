from pages.products import ProductsBaseTest
import pytest
import allure

@allure.feature("Проверка результата обработки файла PRLIST.DBF")
class TestPrlistDBF(ProductsBaseTest):
    
    crm_data = None
    prlist_dbf = None
    product_code = None

    @pytest.fixture(autouse=True)
    def test_data(self, product_code, prlist_dbf_data, product_properties):
        conn = product_properties
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM crm_products WHERE PRODUCT_ID={product_code}")
        self.crm_data = cur.fetchone()
        if self.crm_data is None:
            pytest.fail( f"Код товара {product_code} отсутствует в CRM")
        self.product_code = product_code
        self.prlist_dbf = {row['PAYFORM_ID']:row['PRICE'] for index, row in prlist_dbf_data.iterrows() \
                           if row['PAYFORM_ID'] not in [200501, 200084]}

    @allure.title("Проверка типа цены 'САЙТ'")
    def test_check_site_price(self):
        if 200502 not in self.prlist_dbf:
            pytest.skip(f"Для товара {self.product_code} отсутствует запись с PAYFORM_ID = 200502 в файле")
        assert float(self.prlist_dbf[200502]) == float(self.crm_data[4]),\
        f"Ошибка в цене САЙТ: Ожидаемый {self.prlist_dbf[200502]}, Фактический {self.crm_data[4]}"
    
    @allure.title("Проверка типа цены 'МОЦ'")
    def test_check_moc_price(self):
        if 200127 not in self.prlist_dbf:
            pytest.skip(f"Для товара {self.product_code} отсутствует запись с PAYFORM_ID = 200127 в файле")
        assert float(self.prlist_dbf[200127]) == float(self.crm_data[5]),\
        f"Ошибка в цене МОЦ: Ожидаемый {self.prlist_dbf[200127]}, Фактический {self.crm_data[5]}"
    
    @allure.title("Проверка типа цены 'МРЦ'")
    def test_cgeck_mrc_price(self):
        if 200125 not in self.prlist_dbf:
            pytest.skip(f"Для товара {self.product_code} отсутствует запись с PAYFORM_ID = 200125 в файле")
        assert float(self.prlist_dbf[200125]) == float(self.crm_data[6]),\
        f"Ошибка в цене МРЦ: Ожидаемый {self.prlist_dbf[200125]}, Фактический {self.crm_data[6]}"
    
    @allure.title("Проверка типа цены 'РРЦ'")
    def test_check_rrc_price(self):
        if 200500 not in self.prlist_dbf:
            pytest.skip(f"Для товара {self.product_code} отсутствует запись с PAYFORM_ID = 200500 в файле")
        assert float(self.prlist_dbf[200500]) == float(self.crm_data[7].split("|")[0]),\
        f"Ошибка в цене РРЦ: Ожидаемый {self.prlist_dbf[200500]}, Фактический {self.crm_data[7].split('|')[0]}"

    @allure.title("Проверка базовой цены (Розничная цена)")
    def test_check_base_price(self):
        if 200114 not in self.prlist_dbf:
            pytest.skip(f"Для товара {self.product_code} отсутствует запись с PAYFORM_ID = 200114 в файле")
        assert float(self.prlist_dbf[200114]) == float(self.crm_data[16]),\
        f"Ошибка в Розничной (Базовой) цене: Ожидаемый {self.prlist_dbf[200114]}, Фактический {self.crm_data[16]}"
