import pytest
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import sqlite3
from utils.config import get_url
from utils.utils import remove_file, remove_dir
from api.crm_api_client import ApiClient
from pages.products import ProductImportFromFiles

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

@pytest.fixture(scope="session")
def base_url(request):
    """Вспомогательная функция для получения базового URL."""
    env = request.config.getoption("--env")
    specific_url = request.config.getoption("--url")
    return get_url(env, specific_url)

@pytest.fixture(scope="session")
def api_client(base_url):
    """ Фикстура для API Битрик24 """
    return ApiClient(base_url)

@pytest.fixture(scope = 'class')
def response():
    """ Фикстура хранит временные данные для использования в тестовых мтеодах """
    temp_data = {}
    return temp_data

@pytest.fixture(scope="session")
def temp_file(parameters, tmp_path_factory):
    """ Фикстура создают временные файлы """
    file_name = parameters
    a_dir = tmp_path_factory.mktemp('test_data')
    temp_file_path = a_dir / file_name
    
    yield temp_file_path
    
    remove_file(temp_file_path)
    remove_dir(a_dir)

@pytest.fixture(scope='session')
def db_connection():
    """ Фикстура для подключения к БД """
    conn = sqlite3.connect("test_data.db")
    yield conn
    conn.close()

@pytest.fixture(scope="session")
def product_properties(base_url, api_client, db_connection):
    """ Фикстура для работы с тестовыми данными из БД """
    # ~ product_processing = ProductImportFromFiles(base_url)
    # ~ product_processing.create_crm_products_table(db_connection)
    # ~ product_list = product_processing.product_list(api_client)
    # ~ product_processing.insert_product_list(product_list, db_connection)
    # ~ product_price = product_processing.product_price(api_client)
    # ~ product_processing.update_product_price(product_price, db_connection)
    return db_connection
