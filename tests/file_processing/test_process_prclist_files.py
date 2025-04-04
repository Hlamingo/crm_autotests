from utils.server_client import ServerClient
from utils.utils import get_file_from_dir, get_file_path
from dotenv import load_dotenv
from utils.config import Config
from data.php_scripts import PHPScripts
import pytest

class TestPrlistProcess:
    
    @pytest.fixture(autouse = True)
    def setup(self):
        self.env_number = list(Config.DEV_URLS.keys())
        self.php_script = PHPScripts()
        self.server_client = ServerClient()
        self.server_client.environment = self.env_number[4]
    
    # ~ def test_php_script_runner(self):
        # ~ """ Подключается запускает скрипт на сервере """
        # ~ self.server_client.php_script_runner(
            # ~ self.php_script.product_import_from_files
            # ~ )
    
    def test_ftp_file_uploader(self):
        """ Загружает файлы на сервер """
        files = get_file_from_dir("data\\prlist_dbf")
        for file in files:
            file_path = get_file_path(file)
            assert self.server_client.ftp_file_uploader(file_path)
