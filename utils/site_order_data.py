from utils.utils import read_file

class SiteOrderData:
    """ Класс получения данных из пакета 'Заказ с сайта' """
    
    def __init__ (self, file_path):
        self.data = read_file(file_path)
        self.products = self.products_data()
        self.pickup_today = self.data["PROPERTIES"]["PICKUP_TODAY"]["VALUE"]
        self.site_order_code = self.data["FIELDS"]["ID"]
        self.domain = self.data["FIELDS"]["LID"]
        self.user = self.data["FIELDS"]["USER"]
    
    def products_data(self):
        """ Вспомогательный метод: перебирает данные в поле 'BASKET' """
        values = []
        for value in self.data["BASKET"]:
            properties = {
                "CODE": value["PROPERTIES"]["PRODUCT_CODE"]["VALUE"],
                "NAME": value["NAME"],
                "QUANTITY": int(float(value["QUANTITY"])),
                "STORE_ADDRESS_ID": value["PROPERTIES"]["PICKPOINT_CRM"]["VALUE"]
            }
            values.append(properties)
        return sorted(values, key=lambda x: x["CODE"])
