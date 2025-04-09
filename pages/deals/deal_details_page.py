from pages.base_page import BasePage
from locators.deal_locators import DealsLocators
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class DealDetailsPage(BasePage):
    """ Сделка """
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.driver = driver
        self.base_url = base_url
        self.category_url = f"{self.base_url}/crm/deal/category"
        self.details_url = f"{self.base_url}/crm/deal/details"
        self.locators = DealsLocators
    
    def mark_deal_title_as_test(self):
        """ Кликает на карандаш в названии сделки, редактирует название
        """
        self.find_element((By.ID, "pagetitle_edit")).click()
        title_field = self.find_element(
            (By.CSS_SELECTOR, ".pagetitle-item.crm-pagetitle-item")
            )
        title_field.click()
        title = title_field.get_attribute("value")
        title_field.clear()
        test_text = f"ТЕСТ!!! {title}"
        title_field.send_keys(test_text)
        title_field.send_keys(Keys.ENTER)
        title = self.find_element(
            (By.CSS_SELECTOR, "#pagetitle.pagetitle-item")
            )
        assert title.text in test_text
    
    def change_stage_deal(self, stage):
        """ Изменяет стадию сделки в зависимости от аргумент stage"""
        self.element_to_be_clickable((
            By.XPATH, 
            f'//div[@class="crm-entity-section-status-step-item-text" and contains(text(), "{stage}")]'
            )).click()
    
    def click_finish_deal_button(self, status):
        """ Кликает статус завершения сделки в попапе """
        self.visibility_of_element_located(
            (By.ID, "entity_progress_TERMINATION")
            )
        if status.lower() == "сделка успешна":
            self.element_to_be_clickable(
                (By.CSS_SELECTOR, 'a.webform-small-button-accept')
            ).click()
        elif status.lower() == "сделка проиграна":
            self.element_to_be_clickable(
                (By.CSS_SELECTOR, 'a.webform-small-button-decline')
                ).click()
        else:
            raise ValueError(f"Неизвестный статус '{status}'")
                
    def click_failture_radio_button(self, failture_status):
        """ Выбирает (радио-кнопку) проигрышный статус сделки """
        self.visibility_of_element_located((
            By.ID, "entity_progress_FAILURE"
        ))
        self.element_to_be_clickable((
            By.XPATH, f'//input[@name="entity_progress_FAILURE" and \
            following-sibling::label[text()="{failture_status}"]]'
        )).click()
        self.element_to_be_clickable(
            (By.CSS_SELECTOR, '.popup-window-button-accept')
        ).click()
        time.sleep(2)
            
    def click_common_button(self, category_id):
        """ Кликает на раздел 'Общее' """
        self.element_to_be_clickable(self.locators.Buttons.common_button(category_id)).click()
        
    def deal_id_field(self):
        """ Находит поле 'ID' в сделке,и возвращает значение """
        return self.find_element(self.locators.Fields.DEAL_ID)
    
    def deal_stage(self):
        """ Находит поле 'Стадия' и возвращает значение """
        return self.visibility_of_element_located(self.locators.Fields.STAGE_ID)
    
    def client_block(self):
        """ Находит блок 'Клиент' и возвращает результат из полей 
        'Компания' и 'Контакт'. Можно извлечь название или ссылку """
        return self.find_elements(self.locators.Fields.CLIENT_BLOCK)
        
    def assigned_block(self):
        """ Находит блок 'Ответственный' и возвращает результат из полей
        'Ответственный' и 'Наблюдатели'. Можно извлечь текст или ссылку.
        """
        assigned = self.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, "a.crm-widget-employee-name")
            )
        return assigned
        
    def click_reserve_interface_button(self):
        """ Кликает на кнопку 'Резервирование товаров' """
        current_url = self.driver.current_url
        ri_button = self.element_to_be_clickable(self.locators.Buttons.RESERVE_INTERFACE_BUTTON)
        self.scroll_into_view(ri_button)
        ri_button.click()
        return self.driver.current_url if self.url_changes(current_url, 30) else current_url
