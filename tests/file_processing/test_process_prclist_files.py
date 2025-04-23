from pages.products import ProductsBaseTest
from utils.utils import read_file
from pytest_check import check
import pytest
import allure
import time

class TestPrlistProcess(ProductsBaseTest):
    
    file_path = "data/prlist_dbf"
    
    # ~ @allure.title("Проверка загрузки файлов на FTP")
    # ~ def test_ftp_file_uploader(self):
        # ~ self.products_processing_page.upload_file_to_ftp(self.file_path)
        
    # ~ @allure.title("Подключается к серверу и запускает скрипт")
    # ~ def test_php_script_runner(self):
        # ~ self.products_processing_page.processing_prlist_dbf(self.file_path)
        
    @allure.title("Проверка результата обработки файлов")
    def test_check_result_prlist_processing(self, api_client):
        
        # Получает список товаров из файла PRLIST.DBF 
        prlist_rows = read_file(f"{self.file_path}/PRLIST.DBF")
        # Сортирует данные по коду товара
        sorted_prlist = prlist_rows.sort_values('CODE')
        for code, prlist_dbf in sorted_prlist.groupby('CODE'):
            print(code)
            # Получает свойство товара из ProductsData.csv
            product_data_csv = read_file(f"{self.file_path}/ProductsData.csv")
            # Отфильтровывает данные в соответствии с id товара
            product_data_csv[product_data_csv['ProductCode']== int(code)]
            
            with allure.step("Отправка get-запроса на crm.product.list"):
                time.sleep(2)
                product_id = api_client.request(
                "GET", f"{api_client.method.crm_product_list}?filter[XML_ID]={int(code)}"
                )
                assert product_id.status_code == 200, \
                f"crm.product.list не доступен {product_id.status_code}"
                
                try:
                    product_xml_id = product_id.json()['result'][0]['XML_ID']
                except IndexError:
                    check.is_true(IndexError, f"Товар {code} не найден в CRM")
                    
                check.equal(
                    product_xml_id,
                    code.strip(),
                f"Запрошен XML_ID {code}, получен {product_xml_id}")
            
            # Получает id товара из запроса crm.product.list
            product_id = product_id.json()['result'][0]['ID']
            
            with allure.step(f"Отправка get-запроса на crm.product.get. ID - товара {product_id}"):
                properties = api_client.request(
                "GET", f"{api_client.method.crm_product_get}?id={product_id}"
                )
                assert properties.status_code == 200,\
                f"crm.product.list не доступен {properties.status_code}"
            
                properties = properties.json()
                check.equal(
                    properties['result']['ID'],
                    product_id,
                    f"Запрошен ID {product_id}, получен {properties['result']['ID']}"
                    )
            with allure.step(self.check_product_price.__doc__):
                self.check_product_price(prlist_dbf, properties)
                
            with allure.step(self.check_property_name.__doc__):
                self.check_property_name(product_data_csv, properties)
                
            with allure.step(self.check_property_weight.__doc__):
                self.check_property_weight(product_data_csv, properties)
                
            with allure.step(self.check_property_package_qtt.__doc__):
                self.check_property_package_qtt(product_data_csv, properties)
                
            with allure.step(self.check_property_ean_code.__doc__):
                self.check_property_ean_code(product_data_csv, properties)
                
            with allure.step(self.check_property_country.__doc__):
                self.check_property_country(product_data_csv, properties)
                
            with allure.step(self.check_property_capacity.__doc__):
                self.check_property_capacity(product_data_csv, properties)
                
            with allure.step(self.check_property_guid.__doc__):
                self.check_property_guid(product_data_csv, properties)
                
            with allure.step(self.check_property_manufacturer_agt.__doc__):
                self.check_property_manufacturer_agt(product_data_csv, properties)
    
    def check_product_price(self, prlist_dbf, properties):
        """ Проверяет проставление тип цен в товаре из ответа на запрос """
        for index, row in prlist_dbf.iterrows():
            if row['PAYFORM_ID'] in [200501, 200084]:
                pass
            elif row['PAYFORM_ID'] == 200114:
                check.equal(
                    float(properties['result']['PRICE']), 
                    float(row['PRICE'])
                    )
            elif row['PAYFORM_ID'] == 200500:
                check.equal(
                    float(properties['result']['PROPERTY_626']['value'].split("|")[0]),
                    row['PRICE']
                    )
            elif row['PAYFORM_ID'] == 200127:
                check.equal(
                    float(properties['result']['PROPERTY_731']['value']),
                    float(row['PRICE'])
                    )
            elif row['PAYFORM_ID'] == 200125:
                check.equal(
                    float(properties['result']['PROPERTY_151']['value']),
                    float(row['PRICE'])
                    )
            elif row['PAYFORM_ID'] == 200502:
                check.equal(
                    float(properties['result']['PROPERTY_883']['value']),
                    float(row['PRICE'])
                    )
    
    def check_property_name(self, product, properties):
        """ Проверяет свойство 'Наименование' из ответа на запрос  """
        check.equal(
            f"{product.ProductCode.iloc[0]} - {product.ProductName.iloc[0]}",
            properties['result']['NAME']
            )
    
    def check_property_weight(self, product, properties):
        """ Проверяет свойство 'Вес' из ответа на запрос"""
        check.equal(
            float(product.UnitWeight.iloc[0].replace(',', '.')),
            float(properties['result']['PROPERTY_541']['value'])
        )
    
    def check_property_package_qtt(self, product, properties):
        """ Проверяет поле 'Количество в упаковке' из ответа на запрос """
        check.equal(
            product.Package_QTY.iloc[0],
            float(properties['result']['PROPERTY_339']['value'])
            )
    
    def check_property_ean_code(self, product, properties):
        """ Проверяет свойство 'Штрих-код' из ответа на запрос """
        check.equal(
            product.EANCode.iloc[0],
            properties['result']['PROPERTY_244']['value']
            )
        
    def check_property_country(self, product, properties):
        """ Проверяет свойство 'Страна' из ответа на запрос """
        check.equal(
            product.ProdCategoryName.iloc[0].lower(),
            properties['result']['PROPERTY_728']['value'].lower()
        )
    
    def check_property_capacity(self, product, properties):
        """ Проверяет свойство 'Объём' из ответа на запрос """
        check.equal(
            product.Сapacity.iloc[0],
            float(properties['result']['PROPERTY_739'][0]['value'])
            )
    
    def check_property_guid(self, product, properties):
        """ Проверяет свойство 'GUID' из ответа на запрос """
        check.is_in(
            product.ProductID.iloc[0],
            properties['result']['PROPERTY_304']['value']
            )
    
    def check_property_manufacturer_agt(self, product, properties):
        """ Проверяет свойство 'Производитель АГТ' из ответа на запрос """
        check.equal(
            product.Manufacturer.iloc[0],
            properties['result']['PROPERTY_737']['value']
        )
