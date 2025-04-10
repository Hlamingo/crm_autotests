from utils.server_client import ServerClient, PHPScripts
from utils.utils import get_file_path, get_file_from_dir
from dotenv import load_dotenv
from utils.config import Config
import pytest
import allure

class TestPrlistProcess:
    
    @pytest.fixture(autouse = True)
    def setup(self):
        self.env_number = list(Config.DEV_URLS.keys())
        self.php_script = PHPScripts()
        self.server_client = ServerClient()
        self.server_client.environment = self.env_number[4]
        self.folder_path = "data/prlist_dbf"
    
    @allure.title("Проверка загрузки файлов на FTP")
    def test_ftp_file_uploader(self):
        """ Загружает файлы на сервер """
        files = get_file_from_dir(self.folder_path)
        for file_name in files:
            with allure.step(f"Загрузка фала {file_name}"):
                local_file_path = get_file_path(f"{self.folder_path}/{file_name}")
                remote_path = self.server_client.ftp_file_uploader(local_file_path)
                assert file_name in remote_path
        
    @allure.title("Подключается к серверу и запускает скрипт")
    def test_php_script_runner(self):
        files = get_file_from_dir(self.folder_path)
        option = ""
        for file_name in files:
            file_path = f"/home/dev/www/{self.server_client.environment}/admins_files"
            option += f" {file_path}/{file_name}"
                
        self.server_client.php_script_runner(
            self.php_script.product_import_from_files, option
            )
