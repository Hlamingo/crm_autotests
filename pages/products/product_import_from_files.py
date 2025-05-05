from utils.utils import read_file, get_file_from_dir, get_file_path
from utils.server_client import ServerClient, PHPScripts
from utils.config import Config
import allure

class ProductImportFromFiles:
    """ Класс обработки товаров из файлов """
    
    def __init__ (self, base_url):
        self.base_url = base_url
        self.environment = self.environment_url()
        self.server_client = ServerClient(self.environment)
        self.php_script = PHPScripts()
        
    def environment_url(self):
        """ Вспомогательный метод для получения окружения """
        return next(
            key for key, value in Config.DEV_URLS.items() if value == self.base_url
            )
    
    def upload_file_to_ftp(self, folder_path):
        """ Загружает файлы на сервер """
        files = get_file_from_dir(folder_path)
        for file_name in files:
            with allure.step(f"Загрузка фала {file_name}"):
                local_file_path = get_file_path(f"{folder_path}/{file_name}")
                remote_path = self.server_client.ftp_file_uploader(local_file_path)
                assert file_name in remote_path, f"Файл отсутствует {file_name} на ftp"
    
    def processing_prlist_dbf(self, folder_path):
        """ Получает список файлов, добавляет его в качестве опции к 
        скрипту, запускает скрипт product_import_from_files """
        files = get_file_from_dir(folder_path)
        option = [f"/home/dev/www/{self.environment}/admins_files/{file_name}" for file_name in files]
        option.sort(key=lambda x: (x.endswith("PRLIST.DBF"), x))
        
        result, message = self.server_client.php_script_runner(
            self.php_script.product_import_from_files, ' '.join(option)
            )
            
        assert result, f"Ошибка при выполнении скрипта: {message}"
    
    def product_list(self, api_client):
        """ Выгружает свойства товаров по REST-методу 'catalog.product.list'"""
        product_list = api_client.bx.get_all(
            'catalog.product.list',
            params = {
            "filter": {"iblockId": 27},
            "select": ["id", "iblockId", "price", "name", "property135", 
            "property229", "property883", "property731", "property731",
            "property151", "property626", "property541", "property339",
            "property244", "property728","property739", "property304",
            "property737", "property173"]
            }
        )
        
        return product_list
    
    def product_price(self, api_client):
        """ Выгружает цены товаров по REST-методу 'crm.product.list' """
        product_price = api_client.bx.get_all(
            'crm.product.list',
            params={"select":["ID","PRICE"]})
        
        return product_price
    
    def create_crm_products_table(self, db_connection):
        """ Создёт таблицу для тестовых данных """
        cur = db_connection.cursor()
        create_table = """ CREATE TABLE IF NOT EXISTS crm_products (
            ID INTEGER, NAME TEXT, PRODUCT_ID TEXT, ANALOG_CODE TEXT,
            STIE_PRICE TEXT, MOC_PRICE TEXT, MRC_PRICE TEXT, 
            RRC_PRICE TEXT, UNIT_WEIGHT TEXT, PACKAGE_QTY TEXT,
            EAN_CODE TEXT, PROD_CATEGORY_NAME TEXT, 
            СAPACITY TEXT, GUID TEXT, MANUFACTURER TEXT, ASS_DISTRIB TEXT)"""
        cur.execute(create_table)
        db_connection.commit()
    
    def insert_product_list(self, product_list, db_connection):
        """Добавляет полученные свойства по REST-методу 
        'catalog.product.list' в БД"""
        cur = db_connection.cursor()
        
        for i in range(0, len(product_list), 100):
            batch = product_list[i:i + 100]
            data_to_insert = [(
                product.get('id'),
                product.get('name'),
                product.get('property135', {}).get('value') if product.get('property135') else None,
                product.get('property229', {}).get('value') if product.get('property229') else None,
                product.get('property883', {}).get('value') if product.get('property883') else None,
                product.get('property731', {}).get('value') if product.get('property731') else None,
                product.get('property151', {}).get('value') if product.get('property151') else None,
                product.get('property626', {}).get('value') if product.get('property626') else None,
                product.get('property541', {}).get('value') if product.get('property541') else None,
                product.get('property339', {}).get('value') if product.get('property339') else None,
                product.get('property244', {}).get('value') if product.get('property244') else None,
                product.get('property728', {}).get('value') if product.get('property728') else None,
                product.get('property739', [{}])[0].get('value') if product.get('property739') else None,
                product.get('property304', {}).get('value') if product.get('property304') else None,
                product.get('property737', {}).get('value') if product.get('property737') else None,
                product.get('property173', {}).get('value') if product.get('property173') else None
                )for product in batch
            ]
            cur.executemany("INSERT INTO crm_products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data_to_insert)
            
        db_connection.commit()
        
    def update_product_price(self, product_price, db_connection):
        """ "Добавляет полученные цены по REST-методу 
        'crm.product.list' в БД """
        
        cur = db_connection.cursor()
        cur.execute("PRAGMA table_info(crm_products)")
        columns = [column[1] for column in cur.fetchall()]
        
        if "PRICE" not in columns:
            cur.execute("ALTER TABLE crm_products ADD COLUMN PRICE TEXT")
            
        update_query = """ UPDATE crm_products SET PRICE = CASE ID {cases} END WHERE ID IN ({ids}) """
        
        cases = []
        ids = []
        
        for product in product_price:
            product_id = product['ID']
            price = product['PRICE']
            
            if product_id is not None:
                if price is None:
                    cases.append(f"WHEN {product_id} THEN NULL")
                else:
                    cases.append(f"WHEN {product_id} THEN '{price}'")
                ids.append(product_id)
            ids.append(product_id)
        
        update_query = update_query.format(cases=' '.join(cases), ids=','.join(ids))
        
        cur.execute(update_query)
        db_connection.commit()
