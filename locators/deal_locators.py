from selenium.webdriver.common.by import By
from locators.create_deal_locators import CreateDealsLocators

class DealsLocators(CreateDealsLocators):
    """ Локаторы для страницы сделки """
    class Fields:
        """ Локаторы полей для страницы сделки """
        # Значение из поле 'ID'
        DEAL_ID = (By.CSS_SELECTOR, '[data-cid="ID"] .ui-entity-editor-content-block-text')
        # Значение из пооля 'Стадия'
        STAGE_ID = (By.CSS_SELECTOR, '[data-cid="STAGE_ID"] .ui-entity-editor-content-block-text')
        # Значения из полей 'Компания' и 'Контакт' из блока 'Клиент'
        CLIENT_BLOCK = (By.CSS_SELECTOR, 'a.crm-entity-widget-client-box-name')
        # Изменить название сделки
        DEAL_TITLE_EDIT = (By.ID, "pagetitle_edit")
        
    class Buttons:
        """ Локаторы кнопок для страницы создания сделки """
        RESERVE_INTERFACE_BUTTON = (By.ID, "reserve_interface_button")
        # Кнопка 'Сохранить' (сделку)
        SAVE_DEAL_BUTTON = (By.CSS_SELECTOR,".ui-entity-section > .ui-btn-success")
        
        @staticmethod
        def common_button(category):
            """ Возвращает локатор кнопки  'Общее' """
            if category["NAME"] == "Москва":
                return (By.CSS_SELECTOR, "##crm_scope_detail_c_deal___main .main-buttons-item-text-box")
            else:
                return (By.CSS_SELECTOR, f"#crm_scope_detail_c_deal_{category['ID']}__main .main-buttons-item-text-box")
