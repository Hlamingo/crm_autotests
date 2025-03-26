from pages.base_page import BasePage
from locators.deal_locators import DealsLocators

class DealPage(BasePage):
    """ Сделка 'Заказ с сайта' """
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.driver = driver
        self.base_url = base_url
        self.locators = DealsLocators
        
    def open_deal_page(self, deal_id):
        """ Открывает страницу сделки """
        self.open_page(f"{base_url}crm/deal/details/{deal_id}/")
        
    def deal_id_field(self):
        """ Находит поле 'ID' в сделке,и возвращает значение """
        return self.find_element(self.locators.Fields.DEAL_ID).get_attribute("value")
    
    def deal_stage(self):
        """ Находит поле 'Стадия' и возвращает значение """
        return self.find(self.locatos.Fields.STAGE_ID).get_attribute("value")
