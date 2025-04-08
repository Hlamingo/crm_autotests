from selenium.webdriver.common.by import By

class CreateDealsLocators:
    """ Локаторы для страницы создания сделки """
    
    class Fields:
        """ Локаторы полей для страницы создания сделки """
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
        
    class Buttons:
        """ Локаторы кнопок для страницы создания сделки """
        # Кнопка 'Создать' (сделку)
        CREATE_BUTTON = (By.CSS_SELECTOR, ".ui-btn-main > .ui-btn-text")
        # Кнопка направления (воронок) сделок
        ALL_DEALS = (By.XPATH, '//*[@class="ui-btn-text" and text()="Все сделки"]')
        
        @staticmethod
        def funnel_locator(catgory_name):
            """ Возвращает локатор направления (воронку) сделки из списка """
            return (By.XPATH, f'//*[@class = "menu-popup-item-text" and text()="{catgory_name}"]')
        
        @staticmethod
        def entity_locator(value):
            """Возвращает локатор контакта/компании из списка при 
            добавлении """
            return (By.XPATH,f'//*[@class="ui-dropdown-item-name" and contains(text(), "{value}") ]')
            
        @staticmethod
        def current_date(num):
            """ Возвращает локатор числа в календаре 'Дата завершения'"""
            return (By.LINK_TEXT, f"{num}")
        
    class Result:
        """ Локаторы для проверки """
        # Заголовок страницы 'Сделки'
        PAGE_TITLE = (By.ID, "pagetitle")
        
        @staticmethod
        def current_funnel(category_name):
            """ Возвращает локатор текущей воронки (направление) сделки """
            return (By.XPATH, f'//*[@class="ui-btn-text" and text()="{category_name}"]')
            
        @staticmethod
        def entity_block(entity):
            """ Возвращает локатор для блока компании/контакта с 
            подставленным ID """
            return (By.CSS_SELECTOR, f'[data-cid="{entity}_client_editor_SECTION"]')
    
