class Config:
    """ Список окружений """
    DEV_URLS = {
        "44444":"https://44444.crm.taskfactory.ru",
        "48930":"https://48930.crm.taskfactory.ru",
        "51804":"https://51804.crm.taskfactory.ru",
        "52268":"https://52268.crm.taskfactory.ru",
        "54448":"https://54448.crm.taskfactory.ru"
    }
    PROD_URL = "https://crm.l-wine.ru"

def get_url(environment, specific_url=None):
    """ Возвращает URL окружения (prod или dev)"""
    if environment == "prod":
        return Config.PROD_URL
    if specific_url and specific_url in Config.DEV_URLS:
        return Config.DEV_URLS[specific_url]
    return list(Config.DEV_URLS.values())[4]
