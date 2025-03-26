from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

class BasePage:
    
    def __init__ (self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        
    def open_page(self):
        """ Открывает страницу по URL """
        return self.driver.get(self.base_url)
        
    def find_element(self, locator, time = 15):
        """ Ищет элемент на странице  """
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(locator)
        )
    def find_elements(self, locator, time=15):
        """ Ищет элементы на странице и возвращает список элементов """
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_all_elements_located(locator)
            )
    def visibility_of_element_located(self, locator, time = 15):
        """ Ищет элемент на странице и возвращает, когда он 
        отображается """
        return WebDriverWait(self.driver, time).until(
            EC.visibility_of_element_located(locator)
            )
    
    def actions_move_to_element(self, element):
        """ Перемещает курсор мыши к элементу """
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

    def url_to_be(self, url, time=15):
        """ Ожидает изменения url страницы """
        return WebDriverWait(self.driver, time).until(EC.url_to_be(url))
    
    def url_changes(self, url, time=15):
        """ Отслеживает url и возвращает измененный url"""
        return WebDriverWait(self.driver, time).until(EC.url_changes(url))
    
    def switch_to_frame(self, frame_name):
        """ Переключается на фрейм """
        self.driver.switch_to.frame(frame_name)
        
    def scroll_into_view(self, element):
        """ Прокручивает страницу до элемента """
        return self.driver.execute_script(
            "arguments[0].scrollIntoView();", element
            )
