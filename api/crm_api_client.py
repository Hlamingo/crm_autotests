import os
from dotenv import load_dotenv
import requests

class ApiClient:
    """ Работа с REST-Методами CRM """
    def __init__(self, base_url):
        load_dotenv()
        self.user_id = os.getenv("USER_ID")
        self.token = os.getenv("TOKEN")
        self.base_url = base_url
        self.response = None
        
    def site_deal_create(self):
        """ REST-метод site.deal.create """
        return f"{self.base_url}/rest/{self.user_id }/{self.token}/site.deal.create"
    
    def get(self, url):
        """ Отправляет GET-запрос """
        self.response = requests.get(url)
        return self.response
    
    def post(self, url, data=None):
        """ Отправляет POS-запрос """
        if data:
            self.response  = requests.post(url, json=data)
            return self.response
        else:
            self.response = requests.post(url)
            return self.response
    
    def status_code(self):
        """ Возвращает код ответа """
        return self.response.status_code

    def response_json(self):
        """ Возвращает ответ в формате json """
        try:
            return self.response.json()
        except ValueError:
            raise Exception
    
