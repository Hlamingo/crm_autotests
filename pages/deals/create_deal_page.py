from pages.base_page import BasePage
from locators.create_deal_locators import CreateDealsLocators

class CreateDealPage(BasePage):
    """ Сделки """
    def __init__ (self, driver, base_url):
        super().__init__(driver, base_url)
        self.locators = CreateDealsLocators
        self.base_url = f"{base_url}/crm/deal/"
    
    def checking_deal_page_is_open(self):
        """ Возвращает заголовок раздела 'Сделки' """
        return self.find_element(self.locators.Result.PAGE_TITLE).text

    def click_to_deal_funnel_button(self, category_name):
        """ Кликает на кнопку направления сделок и ищет из выпадающего 
        списка воронку 'Бутики'"""
        self.find_element(self.locators.Buttons.ALL_DEALS).click()
        butiques_funnel = self.find_elements(self.locators.Buttons.funnel_locator(category_name))
        return butiques_funnel[1].text
        
    def select_boutiques_funnel(self, category_name):
        """ Наводит курсор и кликает на воронку и возвращает название 
        вороноки"""
        butiques_funnel = self.find_elements(
            self.locators.Buttons.funnel_locator(category_name)
            )
        self.actions_move_to_element(butiques_funnel[1])
        butiques_funnel[1].click()
        return self.find_element(
            self.locators.Result.current_funnel(category_name)
            ).text
        
    def click_create_deal_button(self):
        """ Кликает на кнопку 'Создать' """
        self.find_element(self.locators.Buttons.CREATE_BUTTON).click()
        
    def enter_deal_title(self, title):
        """ Заполняет название сделки"""
        self.switch_to_frame(2)
        element = self.find_element(self.locators.Fields.DEAL_TITLE)
        element.send_keys(title)
        return element.get_attribute("value")
        
    def enter_value_to_field(self, field_locator, value, entity_block_locator):
        """ Общий метод для выбора компании/контакта в сделке"""
        field = self.find_element(field_locator)
        field.send_keys(value)
        entity = self.find_element(self.locators.Buttons.entity_locator(value))
        entity.click()
        return self.find_element(entity_block_locator, 30).is_displayed()
    
    def enter_company(self, company_id, company_name):
        """ Выбирает компанию в сделке и возвращает True, если появился 
        блок с Телефоном и email """
        return self.enter_value_to_field(
            self.locators.Fields.COMPANY,
            company_name,
            self.locators.Result.entity_block(f"COMPANY_{company_id}")
        )
    
    def enter_contact(self, contact_id, contact_name):
        """ Выбирает контакт в сделке и возвращает True, если появился 
        блок с Телефоном и email """
        return self.enter_value_to_field(
            self.locators.Fields.CONTACT,
            contact_name,
            self.locators.Result.entity_block(f"CONTACT_{contact_id}")
        )
        
    def enter_close_date(self, num):
        """ Устанавливает значение в поле 'Дата завершения' и возвращает
         значение из поля """
        close_date = self.find_element(self.locators.Fields.CLOSEDATE_FIELD)
        self.scroll_into_view(close_date)
        close_date.click()
        self.find_element(self.locators.Buttons.current_date(num)).click()
        return close_date.get_attribute("value")
        
    def open_products_block(self, category):
        """ Открывает товарную часть сделки и возвращает результат 
        открытия товарной части"""
        self.find_element(self.locators.Buttons.products_button(category)).click()
        return self.find_element(self.locators.Result.PRODUCT_BLOCK)
    
    def click_to_select_a_product_button(self):
        """ Кликает на кнопку 'Выбрать товар' и возвращает результат 
        открытия попапа """
        self.find_element(self.locators.Buttons.SELECT_PRODUCT).click()
        return self.find_element(self.locators.Result.PRODUCT_SEARCH_POPUP).is_displayed()
        
    def product_search(self, product_id):
        """ Ищет товар и возвращает название найденного товара """
        self.find_element(self.locators.Fields.PRODUCT_SEARCH).send_keys(product_id)
        return self.visibility_of_element_located(
            self.locators.Result.product_search_title(product_id)
            ).text
        
    def select_product(self, product_id, row_id):
        """ Добавляет товар в товарную часть """
        product = self.find_element(self.locators.Buttons.product_locator(product_id), 20)
        select_item = product.find_element(*self.locators.Buttons.PRODUCT_CHECKBOX)
        select_item.click()
        
        if select_item.is_selected():
            self.find_element(self.locators.Buttons.ADD_PRODUCT_BUTTON).click()
            return self.find_element(
                self.locators.Result.product_title(row_id)
                ).get_attribute("value")
        else:
            return False
            
    def click_to_save_deal_button(self):
        """ Кликает на кнопку 'Сохранить' - сохраняет сделку """
        self.find_element(self.locators.Buttons.SAVE_DEAL_BUTTON).click()
        url = self.driver.current_url
        return self.url_changes(url, 180)
        
    def check_product_in_deal(self, category, row_id):
        """ Возвращает товар из товарной части сделки """
        self.open_products_block(category)
        return self.find_element(
            self.locators.Result.product_title(row_id)
            ).get_attribute("value")
