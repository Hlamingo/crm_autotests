from pages.deal_boutiques_page import DealButiquesPage
import pytest
import time
from datetime import datetime 
import allure

@pytest.fixture
def deal_boutiques_page(browser, base_url):
    """Фикстура для инициализации сделок 'Бутики'"""
    return DealButiquesPage(browser, base_url)

@allure.feature('Создание сделки направления "Бутики"')
class TestDealBoutiques:
    """ Проверка создания сделки """
    
    @pytest.fixture(autouse = True)
    def setup(self, deal_boutiques_page):
        self.deal_page = deal_boutiques_page
        self.deal_page.contact_name = "Тест3 Комшуков"
        self.deal_page.contact_id = 793411
        self.deal_page.category_id = 4
        self.deal_page.product_id = 40440
    
    @pytest.mark.order(1)
    @allure.story("Открытие страницы 'Сделки'")
    def test_open_page(self):
        """Проверка открытия страницы 'Сделки'"""
        self.deal_page.open_page()
        deals = self.deal_page.checking_deal_page_is_open()
        assert deals.lower().strip() == "сделки"
    
    @pytest.mark.order(2)
    @allure.story("Клик на кнопку направления сделок")
    def test_click_to_deal_funnel_button(self):
        """ Проверка нажатия кнопки направления сделок """
        funnel = self.deal_page.click_to_deal_funnel_button()
        assert funnel.lower().strip() == "бутики"
    
    @pytest.mark.order(3)
    @allure.story("Выбор воронки 'Бутики'")
    def test_select_boutiques_funnel(self):
        """ Проверка перехода в воронку 'Бутики' """
        funnel = self.deal_page.select_boutiques_funnel()
        assert  funnel.lower().strip() == "бутики"
    
    @pytest.mark.order(4)
    @allure.story("Клик на кнопку 'Создать'")
    def test_click_create_button(self):
        """ Проверка при клике на кнопку 'Создать' """
        self.deal_page.click_create_deal_button()
        assert self.deal_page.url_to_be(
            f"{self.deal_page.base_url}details/0/?category_id={self.deal_page.category_id}",
            20
        )
    
    @pytest.mark.order(5)
    @allure.story("Ввод названия сделки")
    def test_enter_deal_title(self):
        """ Проверяет ввод названия сделки """
        assert self.deal_page.enter_deal_title("Тест") == "Тест"
    
    @pytest.mark.order(6)
    @allure.story("Добавление компании в сделке")
    def test_enter_company(self):
        """ Проверяет добавление компании в сделке """
        assert self.deal_page.enter_company()
    
    @pytest.mark.order(7)
    @allure.story("Добавление контакта в сделке")
    def test_enter_contact(self):
        """ Проверяет добавление контакта в сделке"""
        assert self.deal_page.enter_contact()
    
    @pytest.mark.order(8)
    @allure.story("Добавление адреса самовывоза в сделке")
    def test_enter_store_address(self):
        """ Проверяет добавление адреса самовывоза в сделке"""
        assert self.deal_page.enter_store_address() == self.deal_page.store_address_name
    
    @pytest.mark.order(9)
    @allure.story("Ввод значения в поле 'Дата завершения'")
    def test_close_date(self):
        """ Проверяет ввод значения в поле 'Дата завершения' """
        current_date = datetime.now()
        close_date = self.deal_page.enter_close_date(current_date.day)
        assert close_date == current_date.strftime("%d.%m.%Y")
    
    @pytest.mark.order(10)
    @allure.story("Переход в товарную часть")
    def test_open_products_block(self):
        """ Проверка перехода в товарную часть """
        assert self.deal_page.open_products_block()
    
    @pytest.mark.order(11)
    @allure.story("Нажатие на кнопку 'Выбрать товар'")
    def test_click_to_select_a_product_button(self):
        """ Проверяет нажатие на кнопку 'Выбрать товар' """
        assert self.deal_page.click_to_select_a_product_button()
    
    @pytest.mark.order(12)
    @allure.story("Клика на кнопку 'Добавить товар'")
    def test_product_search(self):
        """ Проверяет поиск товара """
        product = self.deal_page.product_search(self.deal_page.product_id)
        assert str(self.deal_page.product_id) in product
    
    @pytest.mark.order(13)
    @allure.story("Выбор товара")
    def test_select_product(self):
        """ Проверка выбора товара перед сохранением сделки """
        product = self.deal_page.select_product(self.deal_page.product_id, 0)
        assert str(self.deal_page.product_id) in product
    
    @pytest.mark.order(14)
    @allure.story("Сохранение сделки")
    def test_click_to_save_deal_button(self):
        """ Проверка сохранения сделки """
        assert self.deal_page.click_to_save_deal_button()
    
    @pytest.mark.order(15)
    @allure.story("Проверка наличия товара в сделке")
    def test_check_product_in_deal(self):
        """ Проверяет содержание товара в товарной части сделки после 
        сохранения """
        product = self.deal_page.check_product_in_deal(0)
        assert str(self.deal_page.product_id) in product
        time.sleep(3)
