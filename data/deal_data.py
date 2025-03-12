class DealData:
    """ Класс данных для cделок """
    def __init__(self, company_name, company_id, contact_name, contact_id, product_id):
        self.company = {"ID":company_id, "NAME":company_name}
        self.contact = {"ID":contact_id, "NAME":contact_name}
        self.product_id = product_id

class DealButiquesData(DealData):
    """ Класс данных для cделок 'Бутики' """
    def __init__(self, company_name, company_id, contact_name, contact_id, product_id, store_address_name):
        super().__init__(company_name, company_id, contact_name, contact_id, product_id)
        self.store_address_name = store_address_name
