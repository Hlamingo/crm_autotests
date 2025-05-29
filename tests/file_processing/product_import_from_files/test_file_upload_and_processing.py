from pages.products import ProductsBaseTest
import pytest
import allure

@allure.feature("Обработка файлов PRLIST.DBF, ProductsData.csv и ProductsMore.csv")
@pytest.mark.order(1)
class TestFileUploadAndProcessing(ProductsBaseTest):
    
    file_path = "data/prlist_dbf"
    
    @allure.title("Проверка загрузки файлов на FTP")
    def test_ftp_file_uploader(self):
        self.products_processing_page.upload_file_to_ftp(self.file_path)
        
    @allure.title("Подключается к серверу и запускает скрипт")
    def test_php_script_runner(self):
        self.products_processing_page.processing_prlist_dbf(self.file_path)
