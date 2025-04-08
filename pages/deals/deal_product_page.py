from pages.base_page import BasePage
from locators.deal_product_locators import DealProductLocators
import allure
import time

class DealProductPage(BasePage):
    """ Товарная часть сделки """
    
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.base_url = base_url
        self.locators = DealProductLocators
    
    def open_products_block(self, category_id):
        with allure.step("Кликает на вкладку 'Товары'"):
            self.find_element(self.locators.Buttons.products_button(category_id)).click()
            element = self.find_element(self.locators.Result.PRODUCT_BLOCK)
            return element.is_displayed()
    
    def get_products(self):
        with allure.step("Получает товары из товарной части"):
            elements = self.find_elements(self.locators.Fields.PRDUCTS)
            products = []
    
            for index in range(len(elements)):
                title = self.find_element(self.locators.Result.product("title", index))
                quantity = self.find_element(self.locators.Result.product("quantity", index))
                store_available = self.find_element(self.locators.Result.product("store_available", index))
                rc_available = self.find_element(self.locators.Result.product("rc_available", index))
                cfd_available = self.visibility_of_element_located(self.locators.Result.product("cfd_available", index))
                item = {
                    "TITLE": title.get_attribute("value"),
                    "QUANTITY": int(quantity.get_attribute("value")),
                    "STORE_AVAILABLE": int(store_available.get_attribute("value")),
                    "RC_AVAILABLE": int(rc_available.get_attribute("value")),
                    "CFD_AVAILABLE": int(cfd_available.text)
                }
                products.append(item)
            
            return sorted(products, key=lambda x: x["TITLE"])
            
    def click_checkbox_show_availability(self):
        with allure.step("Устанавливает чекбокс 'Показать сотатки'"):
            self.find_element(self.locators.Fields.SHOW_AVAILABILITY).click()
        
        
