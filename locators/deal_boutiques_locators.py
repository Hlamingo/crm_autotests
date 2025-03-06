from selenium.webdriver.common.by import By
from locators.deal_locators import DealsLocators

class DealButiquesLocators (DealsLocators):
    """ Локаторы для сделки направленя 'Бутики' """
    
    class Fields(DealsLocators.Fields):
        """ Локаторы полей для сделки направления 'Бутики' """
        STORE_ADDRESS = (By.CSS_SELECTOR, 'li.active-result.group-option.test_123')
        STORE_ADDRESS_FIELD = (By.CSS_SELECTOR, '.chosen-single')
        STORE_ADDRESS_SEARCH_FIELD = (By.CSS_SELECTOR,'.chosen-search-input')
        
    class Buttons(DealsLocators.Buttons):
        """ Локаторы кнопок для сделки направления 'Бутики' """
        FUNNEL_LOCATOR = (By.XPATH, '//*[@class = "menu-popup-item-text" and text()="Бутики"]')
        PRODUCTS_BUTTON = (By.CSS_SELECTOR, "#crm_scope_detail_c_deal_4__tab_products .main-buttons-item-text-box")
    
    class Result(DealsLocators.Result):
        """ Локаторы для проверки """
        CURRENT_FUNNEL = (By.XPATH, '//*[@class="ui-btn-text" and text()="Бутики"]')
