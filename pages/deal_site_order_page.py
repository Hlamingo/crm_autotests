from pages.deal_boutiques_page import DealButiquesPage
from api.crm_api_client import ApiClient
import allure

class SiteDealCreate():
    """ Сделка 'Забрать с сайта' """
    
    def __init__ (self, api_client):
        self.api = api_client
        self.webhook = self.api.site_deal_create
    
    def check_method_status(self):
        """ Проверяет доступность rest-метода """
        response = self.api.get(self.webhook)
        return response.status_code
    
    def make_site_order(self, data):
        """ Отправляет пакет с заказом с сайта """
        response = self.api.post(self.webhook, data)
        return response.status_code, response.json()
    
    def get_deal_details(self, deal_id):
        """ Получает данные по сделке """
        response = self.api.get(f"{self.api.crm_deal_get}?id={deal_id}")
        return response.status_code, response.json()
