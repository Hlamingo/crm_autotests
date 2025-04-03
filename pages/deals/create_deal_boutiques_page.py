from pages.deals.create_deal_page import CreateDealPage
from locators.create_deal_boutiques_locators import CreateDealButiquesLocators
import time

class CreateDealBoutiquesPage(CreateDealPage):
    """ Сделки направленя 'Бутики' """
    
    def __init__ (self, driver, base_url):
        super().__init__(driver, base_url)
        self.locators = CreateDealButiquesLocators
        self.base_url = f"{base_url}/crm/deal/"
        self.store_address_locator = self.locators.Fields.STORE_ADDRESS
        
    def enter_store_address(self, store_address_name):
        """ Выбирает адрес самовывоза в сделке и возвращает значение из 
        поля"""
        store_address = self.find_element(self.locators.Fields.STORE_ADDRESS_FIELD)
        self.scroll_into_view(store_address)
        time.sleep(1)
        store_address.click()
        store_address_search_field = self.find_element(self.locators.Fields.STORE_ADDRESS_SEARCH_FIELD)
        store_address_search_field.send_keys(store_address_name)
        select_store_address = self.find_element(self.store_address_locator)
        self.scroll_into_view(select_store_address)
        time.sleep(1)
        select_store_address.click()
        return self.find_element(self.locators.Fields.STORE_ADDRESS_FIELD).text
        

