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
    
    def get_products_from_ir(self):
        """ Получает товары из ИР """
        products = []
        strings = self.find_elements(((By.CSS_SELECTOR, '.itg-pickuppoint-table-row')))
        
        for index, string in enumerate(strings):
            if index < len(strings)-1:
                if index == 0:
                    
                    product_property = strings[index].find_elements(By.CSS_SELECTOR, '.itg-pickuppoint-table-cell-center')
                    item = {
                        "CODE": product_property[3].text,
                        "QUANTITY": int(product_property[7].text),
                        "STORE_AVAILABLE": int(product_property[11].text),
                        "RC_AVAILABLE": int(product_property[13].text),
                        "TO_RESERVE": int(product_property[16].text),
                        "TO_REORDER": int(product_property[18].text)
                    }
                    products.append(item)
                    
                else:
                    product_property = strings[index].find_elements(By.CSS_SELECTOR, '.itg-pickuppoint-table-cell-center')
                    item = {
                        "CODE": product_property[0].text,
                        "QUANTITY": int(product_property[4].text),
                        "STORE_AVAILABLE": int(product_property[8].text),
                        "RC_AVAILABLE": int(product_property[10].text),
                        "TO_RESERVE": int(product_property[13].text),
                        "TO_REORDER": int(product_property[15].text)
                    }
                    products.append(item)
        return products
    
