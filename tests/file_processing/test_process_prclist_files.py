from utils.server_client import ServerClient, PHPScripts
from utils.utils import get_file_path, get_file_from_dir, read_file
from dotenv import load_dotenv
from utils.config import Config
import pytest
import allure
import time

class TestPrlistProcess:
    
    @pytest.fixture(autouse = True)
    def setup(self, api_client):
        self.env_number = list(Config.DEV_URLS.keys())
        self.api_client = api_client
        self.php_script = PHPScripts()
        self.server_client = ServerClient()
        self.server_client.environment = self.env_number[4]
        self.folder_path = "data/prlist_dbf"
    
    # ~ @allure.title("Проверка загрузки файлов на FTP")
    # ~ def test_ftp_file_uploader(self):
        # ~ """ Загружает файлы на сервер """
        # ~ files = get_file_from_dir(self.folder_path)
        # ~ for file_name in files:
            # ~ with allure.step(f"Загрузка фала {file_name}"):
                # ~ local_file_path = get_file_path(f"{self.folder_path}/{file_name}")
                # ~ remote_path = self.server_client.ftp_file_uploader(local_file_path)
                # ~ assert file_name in remote_path
        
    # ~ @allure.title("Подключается к серверу и запускает скрипт")
    # ~ def test_php_script_runner(self):
        # ~ files = get_file_from_dir(self.folder_path)
        # ~ option = ""
        # ~ for file_name in files:
            # ~ file_path = f"/home/dev/www/{self.server_client.environment}/admins_files"
            # ~ option += f" {file_path}/{file_name}"
                
        # ~ self.server_client.php_script_runner(
            # ~ self.php_script.product_import_from_files, option
            # ~ )
            
    @allure.title("Проверка результата обработки файлов")
    def test_check_result_prlist_processing(self):
        
        prlist_rows = read_file(f"{self.folder_path}/PRLIST.DBF")
        sorted_prlist = prlist_rows.sort_values('CODE')
        grouped_products = sorted_prlist.groupby('CODE')
        
        for code, group in grouped_products:
            print(code)
            product_data = read_file(f"{self.folder_path}/ProductsData.csv")
            product_data = product_data[product_data['ProductCode']== int(code)]
            
            time.sleep(2)
            product_id = self.api_client.request(
            "GET", f"{self.api_client.method.crm_product_list}?filter[XML_ID]={int(code)}"
            )
            print (f"\n{product_id.json()}\n")
            properties = self.api_client.request(
            "GET", f"{self.api_client.method.crm_product_get}?id={product_id.json()['result'][0]['ID']}"
            )
            properties = properties.json()
            print (f"\n{properties}\n")
            
            assert f"{product_data.ProductCode.iloc[0]} - {product_data.ProductName.iloc[0]}" == properties['result']['NAME']
            assert float(product_data.UnitWeight.iloc[0].replace(',', '.')) == float(properties['result']['PROPERTY_541']['value'])
            assert product_data.Package_QTY.iloc[0] == float(properties['result']['PROPERTY_339']['value'])
            assert product_data.EANCode.iloc[0] == properties['result']['PROPERTY_244']['value']
            assert product_data.ProdCategoryName.iloc[0].lower == properties['result']['PROPERTY_728']['value'].lower()
            assert product_data.Сapacity.iloc[0] == float(properties['result']['PROPERTY_739'][0]['value'])
            assert product_data.ProductID.iloc[0] in properties['result']['PROPERTY_304']['value']
            assert product_data.Manufacturer.iloc[0] == properties['result']['PROPERTY_737']['value']
            
            for index, row in group.iterrows():
                if row['PAYFORM_ID'] in [200501, 200084]:
                    pass
                elif row['PAYFORM_ID'] == 200114:
                    assert float(properties['result']['PRICE']) == float(row['PRICE'])
                elif row['PAYFORM_ID'] == 200500:
                    assert float(properties['result']['PROPERTY_626']['value'].split("|")[0]) == row['PRICE']
                elif row['PAYFORM_ID'] == 200127:
                    assert float(properties['result']['PROPERTY_731']['value']) == float(row['PRICE'])
                elif row['PAYFORM_ID'] == 200125:
                    assert float(properties['result']['PROPERTY_151']['value']) == float(row['PRICE'])
                elif row['PAYFORM_ID'] == 200502:
                    assert float(properties['result']['PROPERTY_883']['value']) == float(row['PRICE'])
