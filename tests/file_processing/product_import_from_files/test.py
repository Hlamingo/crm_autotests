import pysftp
import io
from dbfread import DBF
import os
from dotenv import load_dotenv
import pandas as pd
import tempfile

load_dotenv()
key_path = os.getenv("SSH_KEY")
ssh_log = os.getenv("SSH_LOGIN")
hostname = "crm.taskfactory.ru"

dbf_file_path = "/home/dev/admin_files/PRLIST.DBF"

# Подключение к SFTP и чтение DBF файла
with pysftp.Connection(host=hostname, username=ssh_log, private_key=key_path) as sftp:
    with sftp.open(dbf_file_path) as remote_file:
        with sftp.open(dbf_file_path) as remote_file:
            print("Соединение установлено")
        # Создаем временный файл
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                # Записываем содержимое удаленного файла во временный файл
                temp_file.write(remote_file.read())
                temp_file_path = temp_file.name
                # ~ # Читаем содержимое файла в память
                # ~ file_content = io.BytesIO(remote_file.read())
                # ~ print("Файл считан в память")
                # Читаем DBF файл из памяти
            dbf_file = DBF(temp_file_path)
            print("Файл считан")
            # Обработка данных
            for record in dbf_file:
                print(record)
    
