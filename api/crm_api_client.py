import os
from dotenv import load_dotenv
import requests

class APIMethods:
    """ Класс с методами Битрикс 24 """
    def __init__(self):
        self.site_deal_create = "/site.deal.create" # метод создания сделки
        self.crm_deal_get = "/crm.deal.get.json" # метод получения данных по сделке
        self.user_get = "user.get.json" # метод получения данных по пользователю

class ApiClient:
    """ Работа с REST-Методами CRM """
    def __init__(self, base_url):
        load_dotenv()
        user_id = os.getenv("USER_ID")
        token = os.getenv("TOKEN")
        self.base_url = f"{base_url}/rest/{user_id }/{token}"
        self.response = None
    
    def request(self, method, endpoint, data=None):
        """ Выполняет HTTP-запрос к указанному endpoint """
        url = f"{self.base_url}{endpoint}"
        if method == "GET":
            return requests.get(url)
        elif method == "POST":
            return requests.post(url, json=data)   
