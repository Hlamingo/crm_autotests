from pages.products import ProductImportFromFiles
import pytest

class ProductsBaseTest:
    """ Базовый тестовый класс товаров """
    
    products_processing_page: ProductImportFromFiles
    
    @pytest.fixture(autouse=True)
    def setup(self, base_url, request):
        """ Инициализация страниц перед каждым тестом """
        request.cls.products_processing_page = ProductImportFromFiles(base_url)
        
