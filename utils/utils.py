import os
from pathlib import Path
from dotenv import load_dotenv
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
from dbfread import DBF
import pandas as pd


def read_file(file_path=None, file_content=None):
    """ Считывает файл и возвращает содержимое """
    if file_content is not None:
        return pd.DataFrame(iter(DBF(file_content)))
    
    if "json" in str(file_path):
        with open(file_path, 'r', encoding='utf-8') as data:
            return json.load(data)
    elif "DBF" in str(file_path):
        return pd.DataFrame(iter(DBF(file_path)))
    elif "csv" in str(file_path):
        return pd.read_csv(file_path, dtype =str, encoding='cp1251', engine='python')
    else:
        with open(file_path, 'r') as data:
            return data.read()
            
def write_file(file_path, data):
    """ Записывает файл """
    if "json" in str(file_path):
        with open(file_path, 'w') as new_file:
            json.dump(data, new_file, indent=4)
    else:
        with open(file_path, 'w') as new_file:
            new_file.write(str(data))
            
def remove_file(file_path):
    """ Удаляет файл из директории """
    if os.path.exists(file_path):
        os.remove(file_path)
        
def remove_dir(file_path):
    """ Удаляет файл директорию """
    if os.path.isdir(file_path):
            os.rmdir(file_path)

def get_file_path(relative_path):
    """ Возвращает абсолютный путь к файлу """
    load_dotenv()
    base_dir = Path(os.getenv('BASE_DIR', Path(__file__).resolve().parent))
    return base_dir / relative_path

def get_file_from_dir(file_path):
    """ Возвращает список файлов из директории """
    return os.listdir(file_path)
