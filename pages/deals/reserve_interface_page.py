from pages.base_page import BasePage
from locators.reserve_interface_locators import ReserveInterfaceLocators
import allure

class ReserveInterfacePage(BasePage):
    """ Интерфейс резервирования """
    
    def __init__ (self, driver, base_url):
        super().__init__(driver, base_url)
        self.base_url = base_url
        self.ri_url = f"{self.base_url}/pickuppoint/?ID="
        self.locators = ReserveInterfaceLocators
    
    def get_products(self):
        with allure.step("Получает товары из ИР"):
            products = []
            strings = self.find_elements(self.locators.Fields.ALL_STRINGS)
            
            for index, string in enumerate(strings):
                if index <= len(strings)-1:
                    
                    product_property = self.find_elements(self.locators.Fields.COLUMNS)
                    item = {
                        "code": product_property[3].text,
                        "store_available": int(product_property[11].text),
                        "rc_available": int(product_property[13].text),
                        "to_reserve": int(product_property[16].text),
                        "to_reorder": int(product_property[18].text)
                    }
                    products.append(item)
            return products
    
