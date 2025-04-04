from pages.base_page import BasePage

class ReserveInterfacePage(BasePage):
    """ Интерфейс резервирования """
    
    def __init__ (self, driver, base_url):
        super().__init__(driver, base_url)
        self.base_url = base_url
        self.ri_url = f"{self.base_url}/pickuppoint/?ID="
