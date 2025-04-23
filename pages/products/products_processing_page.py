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
                assert file_name in remote_path
    
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
