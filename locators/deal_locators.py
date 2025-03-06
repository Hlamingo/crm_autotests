from selenium.webdriver.common.by import By

class DealsLocators:
    """ Локаторы для страницы сделки """
    
    class Fields:
        """ Локаторы полей для страницы сделки """
        # Поле 'Название' в сделке
        DEAL_TITLE = (By.ID, "title_text")
        # Поле 'Компания'
        COMPANY = (By.CSS_SELECTOR, '[placeholder="Название компании, телефон или e-mail"]')
        # Поле 'Контакт'
        CONTACT = (By.CSS_SELECTOR,'[placeholder="Имя контакта, телефон или e-mail"]')
        # Поле 'Дата завершения'
        CLOSEDATE_FIELD = (By.NAME, "CLOSEDATE")
        # Поле поиска товара
        PRODUCT_SEARCH = (By.ID, "product_search_text")
        # Поле 'ID' в сделке
        DEAL_ID = (By.CSS_SELECTOR, '[data-cid="ID"]')
        
    class Buttons:
        """ Локаторы кнопок для страницы сделки """
        # Кнопка 'Создать' (сделку)
        CREATE_BUTTON = (By.CSS_SELECTOR, ".ui-btn-main > .ui-btn-text")
        # Кнопка направления (воронок) сделок
        ALL_DEALS = (By.XPATH, '//*[@class="ui-btn-text" and text()="Все сделки"]')
        # Направление (воронка) сделки из списка
        FUNNEL_LOCATOR = (By.XPATH, '//*[@class = "menu-popup-item-text" and text()="Москва"]')
        # Вкладка 'Товары' (для перехода в товарную часть)
        PRODUCTS_BUTTON = (By.CSS_SELECTOR, "#crm_scope_detail_c_deal__tab_products .main-buttons-item-text-box")
        # Кнопка 'Выбрать товар' в товарной части
        SELECT_PRODUCT = (By.ID,"deal_product_editor_select_product_button")
        # Кнопка "Добавить" (выбранный товар в сделку) 
        ADD_PRODUCT_BUTTON = (By.ID, "product_search_add")
        # Кнопка 'Сохранить' (сделку)
        SAVE_DEAL_BUTTON = (By.CSS_SELECTOR,".ui-entity-section > .ui-btn-success")
        # Чекбокс для добавления товара в товарную часть
        PRODUCT_CHECKBOX = (By.CSS_SELECTOR, ".col_checkbox > input")
        
        @staticmethod
        def entity_locator(value):
            """Возвращает локатор контакта/компании из списка при 
            добавлении """
            return (By.XPATH,f'//*[@class="ui-dropdown-item-name" and contains(text(), "{value}") ]')
            
        @staticmethod
        def product_locator(product_id):
            """ Возвращает локатор товара из результата поиска """
            return (By.XPATH, f"//div[contains(text(), '{product_id}')]//ancestor::tr")
        
        @staticmethod
        def current_date(num):
            """ Возвращает локатор числа в календаре 'Дата завершения'"""
            return (By.LINK_TEXT, f"{num}")
        
    class Result:
        """ Локаторы для проверки """
        # Заголовок страницы 'Сделки'
        PAGE_TITLE = (By.ID, "pagetitle")
        # Текущая воронка (направление) сделки
        CURRENT_FUNNEL = (By.XPATH, '//*[@class="ui-btn-text" and text()="Москва"]')
        # Область товарной части
        PRODUCT_BLOCK = (By.CSS_SELECTOR, ".items_table_wrapper.product-wrapper")
        # Попап поиска товара в товарной части
        PRODUCT_SEARCH_POPUP = (By.ID, "popup-message")
        # ~ (By.XPATH, '//input[@class = "crm-item-name-inp"]')
        
        @staticmethod
        def entity_block(entity):
            """ Возвращает локатор для блока компании/контакта с 
            подставленным ID """
            return (By.CSS_SELECTOR, f'[data-cid="{entity}_client_editor_SECTION"]')
            
        @staticmethod
        def product_title(row_id):
            """ Возвращает локатор поля 'Наименование' товарной позиции """
            return (By.ID, f'deal_product_editor_product_row_{row_id}_PRODUCT_NAME')
        
        @staticmethod
        def product_search_title(product_id):
            """ Возвращает  """
            return (By.XPATH, f"//div[contains(text(), '{product_id}')]")
    
