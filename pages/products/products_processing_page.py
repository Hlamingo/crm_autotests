from utils.utils import read_file, get_file_from_dir, get_file_path
from utils.server_client import ServerClient, PHPScripts
from utils.config import Config
import allure

class ProductProcessingPage:
    """ Класс обработки товаров из файлов """
    
    def __init__ (self, base_url):
        self.base_url = base_url
        self.environment = self.environment_url()
        self.server_client = ServerClient(self.environment)
        self.php_script = PHPScripts()
        
    def environment_url(self):
        """ Вспомогательный метод для получения окружения """
        return next(
            key for key, value in Config.DEV_URLS.items() if value == self.base_url
            )
    
    def upload_file_to_ftp(self, folder_path):
        """ Загружает файлы на сервер """
        files = get_file_from_dir(folder_path)
        for file_name in files:
            with allure.step(f"Загрузка фала {file_name}"):
                local_file_path = get_file_path(f"{folder_path}/{file_name}")
                remote_path = self.server_client.ftp_file_uploader(local_file_path)
                assert file_name in remote_path, f"Файл отсутствует {file_name} на ftp"
    
    def processing_prlist_dbf(self, folder_path):
        """ Получает список файлов, добавляет его в качестве опции к 
        скрипту, запускает скрипт product_import_from_files """
        files = get_file_from_dir(folder_path)
        option = [f"/home/dev/www/{self.environment}/admins_files/{file_name}" for file_name in files]
        option.sort(key=lambda x: (x.endswith("PRLIST.DBF"), x))
        
        result, message = self.server_client.php_script_runner(
            self.php_script.product_import_from_files, ' '.join(option)
            )
            
        assert result, f"Ошибка при выполнении скрипта: {message}"

    def check_product_price(self, prlist_dbf, properties):
        """ Проверяет проставление тип цен в товаре из ответа на запрос """
        for index, row in prlist_dbf.iterrows():
            if row['PAYFORM_ID'] in [200501, 200084]:
                pass
            elif row['PAYFORM_ID'] == 200114:
                assert int(properties[14]) == int(row['PRICE']),\
                f"Ошибка в Розничной цене: Ожидаемый {row['PRICE']}, Фактический {properties[14]}"
            elif row['PAYFORM_ID'] == 200500:
                assert int(properties[6].split("|")[0]) == int(row['PRICE']),\
                f"Ошибка в цене РРЦ: Ожидаемый {row['PRICE']}, Фактический {properties[6].split('|')[0]}"
            elif row['PAYFORM_ID'] == 200127:
                assert int(properties[4]) == int(row['PRICE']),\
                f"Ошибка в цене МОЦ: Ожидаемый {row['PRICE']}, Фактический {properties[4]}"
            elif row['PAYFORM_ID'] == 200125:
                assert int(properties[5]) == int(row['PRICE']),\
                f"Ошибка в цене МРЦ: Ожидаемый {row['PRICE']}, Фактический {properties[5]}"
            elif row['PAYFORM_ID'] == 200502:
                assert int(properties[3]) == int(row['PRICE']),\
                f"Ошибка в цене САЙТ: Ожидаемый {row['PRICE']}, Фактический {properties[3]}"
    
    def check_property_name(self, product, properties):
        """ Проверяет свойство 'Наименование' из ответа на запрос  """
        assert f"{product.ProductCode.iloc[0]} - {product.ProductName.iloc[0]}" == \
            properties[1],\
            f"Ожидаемое '{expected_name}', Фактический '{properties[1]}'"
    
    def check_property_weight(self, product, properties):
        """ Проверяет свойство 'Вес' из ответа на запрос"""
        assert product.UnitWeight.iloc[0].replace(',', '.') == properties[7],\
        f"Ожидаемый {expected_weight}, Фактический {properties[7]}"
       
    def check_property_package_qtt(self, product, properties):
        """ Проверяет свойство 'Количество в упаковке' из ответа на запрос """
        assert product.Package_QTY.iloc[0] == properties[8],\
        f"Ожидаемый {expected_qty}, Фактический {properties[8]}"
    
    def check_property_ean_code(self, product, properties):
        """ Проверяет свойство 'Штрих-код' из ответа на запрос """
        assert product.EANCode.iloc[0] == \
        properties[9],\
        f"Ожидаемый '{product.EANCode.iloc[0]}', Фактический '{properties[9]}'"
        
    def check_property_country(self, product, properties):
        """ Проверяет свойство 'Страна' из ответа на запрос """
        assert product.ProdCategoryName.iloc[0].lower() == \
        properties[10].lower(),\
        f"Ожидаемый '{product.ProdCategoryName.iloc[0].lower()}', Фактический '{properties[10].lower()}'"
    
    def check_property_capacity(self, product, properties):
        """ Проверяет свойство 'Объём' из ответа на запрос """
        assert product.Сapacity.iloc[0] == properties[11],\
         f"Ожидаемый {product.Сapacity.iloc[0]}, Фактический {properties[11]}"
                
    def check_property_guid(self, product, properties):
        """ Проверяет свойство 'GUID' из ответа на запрос """
        assert product.ProductID.iloc[0] in \
        properties[12],\
        f"Ожидаемый '{product.ProductID.iloc[0]}', Фактический '{properties[12]}'"
        
    def check_property_manufacturer_agt(self, product, properties):
        """ Проверяет свойство 'Производитель АГТ' из ответа на запрос """
        assert product.Manufacturer.iloc[0] == \
        properties[13],\
        f"Ожидаемый '{product.Manufacturer.iloc[0]}', Фактический '{properties[13]}'"
