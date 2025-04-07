from selenium.webdriver.common.by import By
from locators.create_deal_locators import CreateDealsLocators

class DealProductLocators(CreateDealsLocators):
    """ Локаторы товарной части """
    
    class Fields(CreateDealsLocators.Fields):
        """ Локаторы полей товарной части """
        # Локатор позволяет узанть кол-во товарных позиций (полей)
        PRDUCTS = (By.XPATH, "//*[contains(@id, '_PRODUCT_NAME_c')]")
        # Чекбокс 'Показать остатки'
        SHOW_AVAILABILITY = (By.ID, "crm-top-available-checkbox")
        
        @staticmethod
        def product_quantity(row_id):
            """ Возвращает локатор поля 'Количество' товарной позиции """
            return (By.ID, f'deal_product_editor_product_row_{row_id}_QUANTITY')
            
    class Buttons(CreateDealsLocators.Buttons):
        """ Локаторы кнопок для страницы создания сделки """
        # Кнопка 'Выбрать товар' в товарной части
        SELECT_PRODUCT = (By.ID,"deal_product_editor_select_product_button")
        # Кнопка "Добавить" (выбранный товар в сделку) 
        ADD_PRODUCT_BUTTON = (By.ID, "product_search_add")
        # Чекбокс для добавления товара в товарную часть
        PRODUCT_CHECKBOX = (By.CSS_SELECTOR, ".col_checkbox > input")
    
        @staticmethod
        def products_button(category):
            """ Возвращает локатор кнопки  'Товары' (для перехода в 
            товарную часть)"""
            if category["NAME"] == "Москва":
                return (By.CSS_SELECTOR, "#crm_scope_detail_c_deal__tab_products .main-buttons-item-text-box")
            else:
                return (By.CSS_SELECTOR, f"#crm_scope_detail_c_deal_{category['ID']}__tab_products .main-buttons-item-text-box")
        
        @staticmethod
        def product_locator(product_id):
            """ Возвращает локатор товара из результата поиска """
            return (By.XPATH, f"//div[contains(text(), '{product_id}')]//ancestor::tr")

    class Result(CreateDealsLocators.Result):
        """ Локаторы для проверки """
        # Область товарной части
        PRODUCT_BLOCK = (By.CSS_SELECTOR, ".items_table_wrapper.product-wrapper")
        # Попап поиска товара в товарной части
        PRODUCT_SEARCH_POPUP = (By.ID, "popup-message")
        
        @staticmethod
        def product(option, row_id):
            """ Возвращает локатор поля 'Наименование' товарной позиции """
            if option.lower() == "title":
                return (By.ID, f'deal_product_editor_product_row_{row_id}_PRODUCT_NAME')
            elif option.lower() == "quantity":
                return (By.ID, f'deal_product_editor_product_row_{row_id}_QUANTITY')
            elif option.lower() == "store_available":
                return (By.ID, f'deal_product_editor_product_row_{row_id}_AVAILABLE_ADDITIONAL')
            elif option.lower() == "rc_available":
                return (By.ID, f'deal_product_editor_product_row_{row_id}_PARTNER_AVAILABLE')
            elif option.lower() == "cfd_available":
                return (By.ID, f'deal_product_editor_product_row_{row_id}_AVAILABLE_CFD')
        
        @staticmethod
        def product_search_title(product_id):
            """ Возвращает  """
            return (By.XPATH, f"//div[contains(text(), '{product_id}')]")
