import pytest
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from utils.config import get_url
from pages.authorization_page import AuthPage
from api.crm_api_client import ApiClient

@pytest.fixture(scope = 'session')
def browser():
    """Фикстура для инициализации и управления экземпляром браузера Firefox."""
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) \
    Gecko/20100101 Firefox/128.0'
    options = Options()
    options.set_preference("general.useragent.override", user_agent)
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service = service, options = options)
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev", help="Environment to run tests against")
    parser.addoption("--url", action="store", help="Specific URL number to run tests against in dev environment")

@pytest.fixture
def auth_page(browser, request):
    """ Фикстура для страницы авторизации """
    env = request.config.getoption("--env")
    specific_url = request.config.getoption("--url")
    base_url = get_url(env, specific_url)
    return AuthPage(browser, base_url)

@pytest.fixture
def base_url(auth_page):
    """Фикстура для получения базового URL из auth_page."""
    return auth_page.base_url

@pytest.fixture
def api_client(request):
    """ Фикстура для API Битрик24 """
    env = request.config.getoption("--env")
    specific_url = request.config.getoption("--url")
    base_url = get_url(env, specific_url)
    return ApiClient(base_url)
