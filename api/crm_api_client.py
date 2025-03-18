import os
from dotenv import load_dotenv
import requests

class ApiClient:
    """ Работа с REST-Методами CRM """
    def __init__(self, base_url):
        load_dotenv()
        user_id = os.getenv("USER_ID")
        token = os.getenv("TOKEN")
        self.base_url = f"{base_url}/rest/{user_id }/{token}"
        self.site_deal_create = f"{self.base_url}/site.deal.create" # вубхук создания сделки
        self.crm_deal_get  = f"{self.base_url}/crm.deal.get.json" # вебхук получения данных по сделке
    
    def get(self, url):
        """ Отправляет GET-запрос """
        return requests.get(url)
    
    def post(self, url, data=None):
        """ Отправляет POS-запрос """
        if data:
            return requests.post(url, json=data)
        else:
            return requests.post(url)
    
