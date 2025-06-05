from pages.products import ProductsBaseTest
from utils.utils import read_file
import pytest
import allure

@allure.feature("Проверка результата обработки файла ProductsData.csv")
class TestProductsDataCsv(ProductsBaseTest):
    
    crm_data = None
    
    @pytest.fixture(autouse=True)
    def get_crm_data_by_product_code(self, code, product_properties_from_crm):
        """ Возвращает данные по товару из БД"""
        conn = product_properties_from_crm
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM crm_products WHERE PRODUCT_ID={code}")
        self.crm_data = cur.fetchone()
        if self.crm_data is None:
            pytest.fail( f"Код товара {product_code} отсутствует в CRM")
    
    @allure.title("Проверка свойства 'Наименование'")
    def test_check_property_name(self, products_data_csv):
        """ Проверяет свойство 'Наименование' """
        expected_name = f"{products_data_csv.ProductCode.iloc[0]} - {products_data_csv.ProductName.iloc[0]}"
        assert expected_name.strip().lower() == self.crm_data[1].strip().lower(),\
            f"Ожидаемое '{expected_name}', Фактический '{self.crm_data[1]}'"
    
    @allure.title("Проверка свойства 'Вес'")
    def test_check_property_weight(self, products_data_csv):
        """ Проверяет свойство 'Вес'"""
        if self.crm_data[8] == None:
            expected_weight = products_data_csv.UnitWeight.iloc[0].replace(',', '.')
            assert expected_weight == self.crm_data[8],\
            f"Ожидаемый {expected_weight}, Фактический {self.crm_data[8]}"
        else:
            expected_weight = products_data_csv.UnitWeight.iloc[0].replace(',', '.')
            assert float(expected_weight) == float(self.crm_data[8]),\
            f"Ожидаемый {expected_weight}, Фактический {self.crm_data[8]}"
    
    @allure.title("Проверка свойства 'Количество в упаковке'")
    def test_check_property_package_qtt(self, products_data_csv):
        """ Проверяет свойство 'Количество в упаковке' """
        expected_qty = products_data_csv.Package_QTY.iloc[0]
        assert expected_qty == self.crm_data[9],\
        f"Ожидаемый {expected_qty}, Фактический {self.crm_data[9]}"
    
    @allure.title("Проверка свойства 'Штрих-код'")
    def test_check_property_ean_code(self, products_data_csv):
        """ Проверяет свойство 'Штрих-код' """
        ean_code = products_data_csv.EANCode.iloc[0]
        if ean_code != ean_code: # Проверяет, если ean_code имеет значение NaN
            ean_code = '0'
        assert ean_code == self.crm_data[10],\
        f"Ожидаемый '{products_data_csv.EANCode.iloc[0]}', Фактический '{self.crm_data[10]}'"
    
    @allure.title("Проверка свойства 'Страна'")
    def test_check_property_country(self, products_data_csv):
        """ Проверяет свойство 'Страна' """
        expected_country = products_data_csv.ProdCategoryName.iloc[0]
        assert self.crm_data[11] is not None, \
        f"Ожидаемый '{expected_country.lower()}', Фактический '{self.crm_data[11]}'"
        assert expected_country.lower() == self.crm_data[11].lower(),\
        f"Ожидаемый '{expected_country.lower()}', Фактический '{self.crm_data[11].lower()}'"
    
    @allure.title("Проверка свойства 'Объём'")
    def test_check_property_capacity(self, products_data_csv):
        """ Проверяет свойство 'Объём' """
        assert self.crm_data[12] is not None, \
        f"Ожидаемый {products_data_csv.Сapacity.iloc[0]}, Фактический {self.crm_data[12]}"
        assert float(products_data_csv.Сapacity.iloc[0]) == float(self.crm_data[12]),\
        f"Ожидаемый {products_data_csv.Сapacity.iloc[0]}, Фактический {self.crm_data[12]}"
    
    @allure.title("Проверка свойства 'GUID'")
    def test_check_property_guid(self, products_data_csv):
        """ Проверяет свойство 'GUID' """
        assert products_data_csv.ProductID.iloc[0] in \
        self.crm_data[13],\
        f"Ожидаемый '{products_data_csv.ProductID.iloc[0]}', Фактический '{self.crm_data[13]}'"
    
    @allure.title("Проверка свойства 'Производитель АГТ'")
    def test_check_property_manufacturer_agt(self, products_data_csv):
        """ Проверяет свойство 'Производитель АГТ' """
        expected_manufacturer = products_data_csv.Manufacturer.iloc[0]
        if expected_manufacturer != expected_manufacturer:
            expected_manufacturer = None
        assert expected_manufacturer == self.crm_data[14],\
        f"Ожидаемый '{expected_manufacturer}', Фактический '{self.crm_data[14]}'"
