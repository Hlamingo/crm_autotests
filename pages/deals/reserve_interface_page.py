from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure

class ReserveInterfacePage(BasePage):
    """ Интерфейс резервирования """
    
    ALL_STRINGS = (By.CSS_SELECTOR, '.itg-pickuppoint-table-row')
    COLUMNS = (By.CSS_SELECTOR, '.itg-pickuppoint-table-cell-center')
    
    def __init__ (self, driver, base_url):
        super().__init__(driver, base_url)
        self.base_url = base_url
        self.ri_url = f"{self.base_url}/pickuppoint/?ID="
    
    def get_products(self):
        """ Получает товары из ИР """
        products = []
        strings = self.find_elements(self.ALL_STRINGS)
        
        for index, string in enumerate(strings):
            if index < len(strings)-1:
                
                product_property = self.find_elements(self.COLUMNS)
                item = {
                    "CODE": product_property[3].text,
                    "STORE_AVAILABLE": int(product_property[11].text),
                    "RC_AVAILABLE": int(product_property[13].text),
                    "TO_RESERVE": int(product_property[16].text),
                    "TO_REORDER": int(product_property[18].text)
                }
                products.append(item)
        return products
    
