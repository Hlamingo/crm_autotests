import pytest
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from utils.config import get_url
from utils.utils import remove
from pages.auth_page.authorization_page import AuthPage
from pages.deals import DealPage, CreateDealPage, CreateDealBoutiquesPage
from api.crm_api_client import ApiClient

@pytest.fixture(scope = 'session')
def browser():
    """Фикстура для инициализации и управления экземпляром браузера Firefox."""
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) \
    Gecko/20100101 Firefox/128.0'
    options = Options()
    # ~ options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.set_preference("general.useragent.override", user_agent)
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service = service, options = options)
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev", help="Environment to run tests against")
    parser.addoption("--url", action="store", help="Specific URL number to run tests against in dev environment")

def get_base_url(request):
    """Вспомогательная функция для получения базового URL."""
    env = request.config.getoption("--env")
    specific_url = request.config.getoption("--url")
    return get_url(env, specific_url)

@pytest.fixture
def auth_page(browser, request):
    """ Фикстура для страницы авторизации """
    base_url = get_base_url(request)
    return AuthPage(browser, base_url)

@pytest.fixture
def api_client(request):
    """ Фикстура для API Битрик24 """
    base_url = get_base_url(request)
    return ApiClient(base_url)

@pytest.fixture
def deal(browser, request):
    """ Фикстура для API Битрик24 """
    base_url = get_base_url(request)
    
    deal_page = DealPage(browser, base_url)
    create_deal = CreateDealPage(browser, base_url)
    create_deal_boutiques = CreateDealBoutiquesPage(browser, base_url)
    
    return {
        "deal_page":deal_page, 
        "create_deal":create_deal, 
        "create_deal_boutiques":create_deal_boutiques
        }
        
@pytest.fixture(scope="session")
def temp_file(parameters, tmp_path_factory):
    file_name = parameters
    a_dir = tmp_path_factory.mktemp('test_data')
    temp_file_path = a_dir / file_name
    
    yield temp_file_path
    
    remove(temp_file_path)
    remove(a_dir)
