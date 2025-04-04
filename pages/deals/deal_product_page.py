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
    
    def open_products_block(self, category):
        with allure.step("Кликает на вкладку 'Товары'"):
            self.find_element(self.locators.Buttons.products_button(category)).click()
            element = self.find_element(self.locators.Result.PRODUCT_BLOCK)
            return element.is_displayed()
    
    def get_products(self):
        with allure.step("Получает товары из товарной части"):
            elements = self.find_elements(self.locators.Fields.PRDUCTS)
            products = 
            for index, _ in enumerate(elements):
                self.product_properties
                product = self.find_element(self.locators.Result.product_title(index))
                products.append(product)
            
            return products
            
    def product_properties(self, elements, option, row_id):
        """ Возвращает данные из полей товарной позиции """
        values = []
        for index, _ in enumerate(elements):
            value = self.find_element(self.locators.Result.product_title(option, index))
            value = {
                f"{option}": value.get_attribute("value")
            }
            values.append(value)
        
        return values
