from locators.create_deal_locators import CreateDealsLocators
from selenium.webdriver.common.by import By

class ReserveInterfaceLocators(CreateDealsLocators):
    """ Локаторы Интерфейса резервирования """
    
    class Fields(CreateDealsLocators.Fields):
        """ Локаторы полей Интерфейса резервирования """
        #Все строки таблицы ИР
        ALL_STRINGS = (By.CSS_SELECTOR, '.itg-pickuppoint-table-row')
        COLUMNS = (By.CSS_SELECTOR, '.itg-pickuppoint-table-cell-center')
        
