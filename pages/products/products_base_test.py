from pages.products import ProductProcessingPage
import pytest

class ProductsBaseTest:
    """ Базовый тестовый класс товаров """
    
    products_processing_page: ProductProcessingPage
    
    @pytest.fixture(autouse=True)
    def setup(self, base_url, request):
        """ Инициализация страниц перед каждым тестом """
        request.cls.products_processing_page = ProductProcessingPage(base_url)
        
