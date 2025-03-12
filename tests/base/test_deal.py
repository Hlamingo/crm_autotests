from pages.deal_page import DealPage
from data.deal_data import DealData
from data.deal_category import DEAL_CATEGORY
import pytest
from datetime import datetime 
import allure

@pytest.fixture(params=[
    DealData(
        "[ITGrade] Тестовая компания с ИНН/КПП и адресом1", 
        16360, 
        "Kейт тест тест Фамилия Фамилия Фамилия Фамилия Фам",
        195342,
        110145
        )
    ])
def deal_data(request):
    return request.param

@pytest.fixture
def deal_page(browser, base_url):
    """Фикстура для инициализации сделок"""
    return DealPage(browser, base_url)

@allure.feature('Создание сделки')
class TestDeal:
    """ Проверка создания сделки """
    
    @pytest.fixture(autouse = True)
    def setup(self, deal_page, deal_data):
        self.deal_page = deal_page
        self.deal_data = deal_data
        self.deal_category = DEAL_CATEGORY["Москва"]
    
    @pytest.mark.order(1)
    @allure.story("Открытие страницы 'Сделки'")
    def test_open_page(self):
        """Проверка открытия страницы 'Сделки'"""
        self.deal_page.open_page()
        deals = self.deal_page.checking_deal_page_is_open()
        assert deals.lower().strip() == "сделки"
    
    @pytest.mark.order(2)
    @allure.story("Клик на кнопку направления сделок")
    def test_click_to_deal_funnel(self):
        """ Проверка нажатия кнопки направления сделок """
        category_name = self.deal_category["NAME"]
        funnel = self.deal_page.click_to_deal_funnel_button(category_name)
        assert funnel.lower().strip() == category_name.lower()
    
    @pytest.mark.order(3)
    @allure.story("Выбор воронки 'Бутики'")
    def test_select_boutiques_funnel(self):
        """ Проверка перехода в воронку 'Бутики' """
        category_name = self.deal_category["NAME"]
        funnel = self.deal_page.select_boutiques_funnel(category_name)
        assert  funnel.lower().strip() == category_name.lower()
    
    @pytest.mark.order(4)
    @allure.story("Клик на кнопку 'Создать'")
    def test_click_create_button(self):
        """ Проверка при клике на кнопку 'Создать' """
        self.deal_page.click_create_deal_button()
        assert self.deal_page.url_to_be(
            f"{self.deal_page.base_url}details/0/?category_id={self.deal_category['ID']}",
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
        assert self.deal_page.enter_company(
            self.deal_data.company["ID"], self.deal_data.company["NAME"]
        )
    
    @pytest.mark.order(7)
    @allure.story("Добавление контакта в сделке")
    def test_enter_contact(self):
        """ Проверяет добавление контакта в сделке"""
        assert self.deal_page.enter_contact(
            self.deal_data.contact["ID"], self.deal_data.contact["NAME"]
        )
    
    @pytest.mark.order(8)
    @allure.story("Ввод значения в поле 'Дата завершения'")
    def test_close_date(self):
        """ Проверяет ввод значения в поле 'Дата завершения' """
        current_date = datetime.now()
        close_date = self.deal_page.enter_close_date(current_date.day)
        assert close_date == current_date.strftime("%d.%m.%Y")
    
    @pytest.mark.order(9)
    @allure.story("Переход в товарную часть")
    def test_open_products_block(self):
        """ Проверка перехода в товарную часть """
        assert self.deal_page.open_products_block()
    
    @pytest.mark.order(10)
    @allure.story("Нажатие на кнопку 'Выбрать товар'")
    def test_click_to_select_a_product_button(self):
        """ Проверяет нажатие на кнопку 'Выбрать товар' """
        assert self.deal_page.click_to_select_a_product_button()
    
    @pytest.mark.order(11)
    @allure.story("Клика на кнопку 'Добавить товар'")
    def test_product_search(self):
        """ Проверяет поиск товара """
        product = self.deal_page.product_search(self.deal_data.product_id)
        assert str(self.deal_data.product_id) in product
    
    @pytest.mark.order(12)
    @allure.story("Выбор товара")
    def test_select_product(self):
        """ Проверка выбора товара перед сохранением сделки """
        product = self.deal_page.select_product(self.deal_data.product_id, 0)
        assert str(self.deal_data.product_id) in product
    
    @pytest.mark.order(13)
    @allure.story("Сохранение сделки")
    def test_click_to_save_deal_button(self):
        """ Проверка сохранения сделки """
        assert self.deal_page.click_to_save_deal_button()
    
    @pytest.mark.order(14)
    @allure.story("Проверка наличия товара в сделке")
    def test_check_product_in_deal(self):
        """ Проверяет содержание товара в товарной части сделки после 
        сохранения """
        product = self.deal_page.check_product_in_deal(0)
        assert str(self.deal_data.product_id) in product
