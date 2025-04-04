from selenium.webdriver.common.by import By
from locators.create_deal_locators import CreateDealsLocators

class DealProductLocators(CreateDealsLocators):
    """ Локаторы товарной части """
    
    class Fields(CreateDealsLocators.Fields):
        """ Локаторы полей товарной части """
        PRDUCTS = (By.XPATH, "//*[contains(@id, '_PRODUCT_NAME_c')]")
