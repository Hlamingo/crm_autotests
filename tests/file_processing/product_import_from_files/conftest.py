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

def pytest_pycollect_makeitem(collector, name, obj):
    env = collector.config.getoption("env")
    if env == "dev":
        try:
            if obj.__name__ and obj.__name__ == "TestPrlistDBF":
                folder_path = "data/prlist_dbf"
                sorted_prlist = read_file(f"{folder_path}/PRLIST.DBF").sort_values('CODE')
                data = [(code, prlist_dbf_data) for code, prlist_dbf_data in sorted_prlist.groupby('CODE')]
                pytest.mark.parametrize("product_code, prlist_data", data)(obj)
        except AttributeError:
            pass
    elif env == "prod":
        try:
            if obj.__name__ and obj.__name__ == "TestPrlistDBF":
                server_client = ServerClient("https://54448.crm.taskfactory.ru")
                prlist_dbf = server_client.ftp_file_reader("PRLIST.DBF")
                # Записываем содержимое удаленного файла во временный файл
                with tempfile.NamedTemporaryFile(suffix=".DBF", delete=True) as temp_file:
                    temp_file.write(prlist_dbf)
                    temp_file.flush()
                    sorted_prlist = read_file(temp_file.name).sort_values('CODE')
                    data = [(code, prlist_dbf_data) for code, prlist_dbf_data in sorted_prlist.groupby('CODE')]
                    pytest.mark.parametrize("product_code, prlist_data", data)(obj)
        except AttributeError:
            pass

    else:
        pytest.fail(reason="Передан неизвестный параметр: {}".format(env))