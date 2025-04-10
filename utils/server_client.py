import paramiko
import pysftp
from dotenv import load_dotenv
import os

class PHPScripts:
    """ Список PHP-скриптов """
    def __init__ (self):
        self.product_import_from_files = "local/php_interface/console product_import_from_files"

class ServerClient:
    """ Класс для взаимодействия с сервером """
    def __init__ (self):
        load_dotenv()
        self.key_path = os.getenv("SSH_KEY")
        self.ssh_log = os.getenv("SSH_LOGIN")
        self.hostname = "crm.taskfactory.ru"
        self.environment = None

    def php_script_runner(self, php_script_path, option=None):
        """ Запускает php скрипт на тестовой площадке 
        stdin: стандартный поток ввода, можно использовать если скрипт 
        ждет данные
        stdout: стандартный поток вывода
        stderr: стандартный поток ошибок
        """
        key = paramiko.RSAKey.from_private_key_file(self.key_path)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.hostname, username=self.ssh_log, pkey=key)
        
        command = f'php www/{self.environment}/{php_script_path}'
        if option:
            command = f'php www/{self.environment}/{php_script_path} {option}'
        print(command)
        stdin, stdout, stderr = ssh.exec_command(command)
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        ssh.close()
    
    def ftp_file_uploader(self, local_file_path):
        """ Загружает файлы на FTP тестовой площадки """
        remote_file_path = f"/home/dev/www/{self.environment}/admins_files"
        
        with pysftp.Connection(
            host=self.hostname, username=self.ssh_log, 
            private_key=self.key_path) as sftp:
            sftp.chdir(remote_file_path)
            sftp.put(local_file_path)
            return sftp.listdir()
