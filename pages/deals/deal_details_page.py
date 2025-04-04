from pages.base_page import BasePage
from locators.deal_locators import DealsLocators
import time

class DealDetailsPage(BasePage):
    """ Сделка """
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.driver = driver
        self.base_url = base_url
        self.category_url = f"{self.base_url}/crm/deal/category"
        self.details_url = f"{self.base_url}/crm/deal/details"
        self.locators = DealsLocators
        
    def deal_id_field(self):
        """ Находит поле 'ID' в сделке,и возвращает значение """
        return self.find_element(self.locators.Fields.DEAL_ID)
    
    def deal_stage(self):
        """ Находит поле 'Стадия' и возвращает значение """
        return self.find_element(self.locators.Fields.STAGE_ID)
    
    def client_block(self):
        """ Находит блок 'Клиент' и возвращает результат, из полей 
        'Компания' и 'Контакт'. Можно извлечь название или ссылку """
        return self.find_elements(self.locators.Fields.CLIENT_BLOCK)
        
    def click_reserve_interface_button(self):
        """ Кликает на кнопку 'Резервирование товаров' """
        current_url = self.driver.current_url
        ri_button = self.find_element(self.locators.Buttons.RESERVE_INTERFACE_BUTTON)
        self.scroll_into_view(ri_button)
        time.sleep(1)
        ri_button.click()
        return self.driver.current_url if self.url_changes(current_url) else current_url
