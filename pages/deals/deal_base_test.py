from pages.auth_page import AuthPage
from pages.deals import DealDetailsPage, DealProductPage
from pages.deals import CreateDealPage, CreateDealBoutiquesPage
from pages.deals import ReserveInterfacePage
import pytest

class DealBaseTest:
    """ Базовый тестовый класс сделки """
    auth_page: AuthPage
    deal_details_page: DealDetailsPage
    deal_product_page: DealProductPage
    create_deal_page: CreateDealPage
    create_deal_boutiques_page: CreateDealBoutiquesPage
    reserve_interface_page: ReserveInterfacePage
    
    @pytest.fixture(autouse=True)
    def setup(self, browser, base_url, request):
        """ Инициализация страниц перед каждым тестом """
        request.cls.auth_page = AuthPage(browser, base_url)
        request.cls.deal_details_page = DealDetailsPage(browser, base_url)
        request.cls.deal_product_page = DealProductPage(browser, base_url)
        request.cls.create_deal_page = CreateDealPage(browser, base_url)
        request.cls.create_deal_boutiques_page = CreateDealBoutiquesPage(browser, base_url)
        request.cls.reserve_interface_page = ReserveInterfacePage(browser, base_url)
