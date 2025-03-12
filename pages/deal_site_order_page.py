from pages.deal_boutiques_page import DealButiquesPage
from api.crm_api_client import ApiClient


class SiteOrderPage(DealButiquesPage):
    """ Сделка 'Забрать с сайта' """
    
    def __init__ (self, driver, base_url):
        super().__init__(driver, base_url)
        self.base_url = base_url
        self.api = ApiClient(base_url)
        self.webhook = self.api.site_deal_create()
        
    def check_method_status(self):
        """ Отправляет првоеряет доступность rest-метода """
        response = self.api.get(self.webhook)
        return response.status_code
    
    def make_site_order(self, data):
        """ Отправляет пакет с заказом с сайта """
        response = self.api.post(self.webhook, data)
        return response.status_code, response.json()
