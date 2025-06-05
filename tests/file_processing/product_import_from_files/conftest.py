from utils.server_client import ServerClient
from pages.products import ProductImportFromFiles
from utils.utils import read_file, read_file_from_buffer
from utils.allure_report_mode import AllureFileLoggerMode
import tempfile
import pytest
import sqlite3
import allure_commons
from allure_commons.logger import AllureFileLogger

@pytest.fixture(scope='session')
def db_connection():
    """ Фикстура для подключения к БД """
    conn = sqlite3.connect(":memory:")
    yield conn
    conn.close()

@pytest.fixture(scope="session")
def product_properties_from_crm(base_url, api_client, db_connection):
    """ Фикстура получает данные по товарам из БД Bitrix24"""
    product_processing = ProductImportFromFiles(base_url)
    product_processing.create_crm_products_table(db_connection)
    product_list = product_processing.product_list(api_client)
    product_processing.insert_product_list(product_list, db_connection)
    product_price = product_processing.product_price(api_client)
    product_processing.update_product_price(product_price, db_connection)
    return db_connection

def cleanup_factory(plugin):
    """ Вспомогательная функция для очистки удаления плагина
    (взят из файла allure_pytest/plugin.py)
    """
    def clean_up():
        name = allure_commons.plugin_manager.get_name(plugin)
        allure_commons.plugin_manager.unregister(name=name)
    return clean_up

def load_files(env, file_name, sort_value):
    """Загружает данные из файла и возвращает список"""
    if env == "dev": # Загружает данные из локального файла

        folder_path = "data/prlist_dbf"
        sorted_file = read_file(f"{folder_path}/{file_name}").sort_values(sort_value)
        return [(product_code, file_data) for product_code, file_data in sorted_file.groupby(sort_value)]

    elif env == "prod": # Загружает файл c FTP

        server_client = ServerClient("https://crm.l-wine.ru")
        ftp_file = server_client.ftp_file_reader(file_name)

        if file_name.endswith(".csv"):

            sorted_prlist = read_file_from_buffer(ftp_file, 'csv').sort_values(sort_value)
            return [(product_code, prlist_dbf_data) for product_code, prlist_dbf_data in
                    sorted_prlist.groupby(sort_value)]
        else:
            # Записываем содержимое удаленного файла во временный файл
            with tempfile.NamedTemporaryFile(suffix=".DBF", delete=True) as temp_file:
                temp_file.write(ftp_file)
                temp_file.flush()
                sorted_prlist = read_file(temp_file.name).sort_values(sort_value)
                return [(product_code, prlist_dbf_data) for product_code, prlist_dbf_data in
                        sorted_prlist.groupby(sort_value)]
    else:
        return False

def pytest_sessionstart(session):
    registered_plugins = allure_commons.plugin_manager.get_plugins()
    for plugin in registered_plugins:
        if isinstance(plugin, allure_commons.logger.AllureFileLogger):
            name = allure_commons.plugin_manager.get_name(plugin)
            allure_commons.plugin_manager.unregister(name=name)

            report_dir = session.config.option.allure_report_dir
            clean = False if session.config.option.collectonly else session.config.option.clean_alluredir
            file_logger = AllureFileLoggerMode(report_dir, clean)
            allure_commons.plugin_manager.register(file_logger)
            session.config.add_cleanup(cleanup_factory(file_logger))


def pytest_pycollect_makeitem(collector, name, obj):
    """ Передаёт параметры в тестовый класс в зависимости от CLI
    --env=dev: загружает данные из локального файла и передаёт, в качестве параметра
    --env=prod: загружает файл с FTP, считывает данные и передаёт в качестве параметра
    """
    env = collector.config.getoption("env")
    
    prlist_dbf_prod_path = "/home/ex/0002/PRLIST.DBF"
    products_data_csv_prod_path = "/home/ex/Products/ProductsData.csv"
    products_more_csv_prod_path = "/home/ex/Products/ProductsMore.csv"
    
    # Пропускаем тест TestFileUploadAndProcessing на продуктивной среде
    if env == "prod" and name == "TestFileUploadAndProcessing":
        pytest.mark.skip(reason=f"{name} пропущен. Тест запускается только в dev среде")(obj)
        
    # Параметризируем тест TestPrlistDBF
    if name == "TestPrlistDBF":
        if env == "prod":
            data = load_files(env, prlist_dbf_prod_path, "CODE")
        else:
            data = load_files(env, "PRLIST.DBF", "CODE")
        if data is False:
            pytest.fail(reason=f"Передан неизвестный параметр: {env}")
        
        ids = [f"Product code: {code[0]}" for code in data]
        pytest.mark.parametrize("code, prlist_dbf_data", data, ids=ids)(obj)
    
    # Параметризируем тест TestProductsDataCsv
    if name == "TestProductsDataCsv":
        if env == "prod":
            data = load_files(env, products_data_csv_prod_path, "ProductCode")
        else:
            data = load_files(env, "ProductsData.csv", "ProductCode")
        if data is False:
            pytest.fail(reason=f"Передан неизвестный параметр: {env}")
        
        ids = [f"Product code: {code[0]}" for code in data]
        pytest.mark.parametrize("code, products_data_csv", data, ids=ids)(obj)
    
    # Параметризируем тест TestProductsMoreCsv
    if name == "TestProductsMoreCsv":
        if env == "prod":
            data = load_files(env, products_more_csv_prod_path, "ProductCode")
        else:
            data = load_files(env, "ProductsMore.csv", "ProductCode")
        if data is False:
            pytest.fail(reason=f"Передан неизвестный параметр: {env}")
        
        ids = [f"Product code: {code[0]}" for code in data]
        pytest.mark.parametrize("code, products_more_csv", data, ids=ids)(obj)