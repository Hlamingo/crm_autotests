import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json

def read_json(file_path):
    """ Считывает файл json и возвращает содержимое """
    with open(file_path) as data:
        return json.load(data)

def get_file_path(relative_path):
    load_dotenv()
    base_dir = os.getenv('BASE_DIR', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, relative_path)
