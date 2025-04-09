import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json

def read_file(file_path):
    """ Считывает файл и возвращает содержимое """
    if "json" in str(file_path):
        with open(file_path, 'r', encoding='utf-8') as data:
            return json.load(data)
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
    """ Вовзращает абсолютный путь к файлу """
    load_dotenv()
    base_dir = os.getenv('BASE_DIR', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, relative_path)
