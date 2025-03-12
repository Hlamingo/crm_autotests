class DealData:
    """ Классы данных для Сделок """
    def __init__(self, company_name, company_id, contact_name, contact_id, product_id):
        self.company = {"ID":company_id, "NAME":company_name}
        self.contact = {"ID":contact_id, "NAME":contact_name}
        self.product_id = product_id
