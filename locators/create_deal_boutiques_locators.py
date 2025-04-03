from selenium.webdriver.common.by import By
from locators.deal_locators import CreateDealsLocators

class CreateDealButiquesLocators (CreateDealsLocators):
    """ Локаторы для сделки направленя 'Бутики' """
    
    class Fields(CreateDealsLocators.Fields):
        """ Локаторы полей для сделки направления 'Бутики' """
        STORE_ADDRESS = (By.CSS_SELECTOR, 'li.active-result.group-option.test_123')
        STORE_ADDRESS_FIELD = (By.CSS_SELECTOR, '.chosen-single')
        STORE_ADDRESS_SEARCH_FIELD = (By.CSS_SELECTOR,'.chosen-search-input')
