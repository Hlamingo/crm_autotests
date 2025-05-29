from utils.server_client import ServerClient
from utils.utils import read_file
import tempfile
import pytest
import sqlite3

@pytest.fixture(scope='session')
def db_connection():
    """ Фикстура для подключения к БД """
    conn = sqlite3.connect("test_data.db")
    yield conn
    conn.close()

@pytest.fixture(scope="session")
def product_properties(base_url, api_client, db_connection):
    """ Фикстура для работы с тестовыми данными из БД """
    # ~ product_processing = ProductImportFromFiles(base_url)
    # ~ product_processing.create_crm_products_table(db_connection)
    # ~ product_list = product_processing.product_list(api_client)
    # ~ product_processing.insert_product_list(product_list, db_connection)
    # ~ product_price = product_processing.product_price(api_client)
    # ~ product_processing.update_product_price(product_price, db_connection)
    return db_connection

def load_files(env, file_name, sort_value):
    """Загружает данные из файла и возвращает список"""
    if env == "dev": # Загружает данные из локального файла PRLIST.DBF

        folder_path = "data/prlist_dbf"
        sorted_file = read_file(f"{folder_path}/{file_name}").sort_values(sort_value)
        return [(product_code, file_data) for product_code, file_data in sorted_file.groupby(sort_value)]

    elif env == "prod": # Загружает файл PRLIST.DBF c FTP

        server_client = ServerClient("https://54448.crm.taskfactory.ru")
        ftp_file = server_client.ftp_file_reader(file_name)

        if file_name.endswith(".csv"):

            sorted_prlist = read_file(ftp_file).sort_values(sort_value)
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

def pytest_pycollect_makeitem(collector, name, obj):
    """ Передаёт параметры в тестовый класс в зависимости от CLI
    --env=dev: загружает данные из локального файла и передаёт, в качестве параметра
    --env=prod: загружает файл с FTP, считывает данные и передаёт в качестве параметра
    """
    env = collector.config.getoption("env")
    if env == "prod" and name == "TestFileUploadAndProcessing":
        pytest.mark.skip(reason=f"{name} пропущен. Тест запускается только в dev среде")(obj)

    if name == "TestPrlistDBF":
        data = load_files(env, "PRLIST.DBF", "CODE")
        if data is False:
            pytest.fail(reason=f"Передан неизвестный параметр: {env}")

        pytest.mark.parametrize("product_code, prlist_dbf_data", data)(obj)

    if name == "TestProductsDataCsv":
        data = load_files(env, "ProductsData.csv", "ProductCode")
        if data is False:
            pytest.fail(reason=f"Передан неизвестный параметр: {env}")

        pytest.mark.parametrize("code, products_data_csv", data)(obj)