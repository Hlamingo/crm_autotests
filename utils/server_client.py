import paramiko
import pysftp
from dotenv import load_dotenv
from utils.config import Config
import os
import io

class PHPScripts:
    """ Список PHP-скриптов """
    def __init__ (self):
        self.product_import_from_files = "local/php_interface/console product_import_from_files"

class ServerClient:
    """ Класс для взаимодействия с сервером """
    def __init__ (self, base_url):
        load_dotenv()
        self.key_path = os.getenv("SSH_KEY")
        self.ssh_log = os.getenv("SSH_LOGIN")
        self.base_url = base_url
        self.hostname = self.hostname_url()
        self.environment = self.environment_url()
        
    def environment_url(self):
        """ Вспомогательный метод для получения окружения """
        if self.base_url == Config.PROD_URL:
            return Config.PROD_URL
        else:
            return next(
                key for key, value in Config.DEV_URLS.items() if value == self.base_url
                )
            
    def hostname_url(self):
        """ Вспомогательный метод для получения url FTP-сервера """
        if self.base_url == Config.PROD_URL:
            pass #здесь ввести url для подключения к FTP-прода
        else:
            return "crm.taskfactory.ru"

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
        
        output = []
        error_output = []
        
        # Считывает вывод cmd до завершения запуска скрипта
        while True:
            line = stdout.readline()
            if not line:
                break
            output.append(line)
            print(line, end='')  # Вывод в консоль
    
        # Считывает ошибки из cmd
        while True:
            line = stderr.readline()
            if not line:
                break
            error_output.append(line)
            print(line, end='')
    
        ssh.close()
        
        error_output = ''.join(error_output)
        message = ''.join(output)
        
        # Проверяет результат завершения выполнения скрипта: 0 - успех
        exit_status = stdout.channel.recv_exit_status()
        
        if exit_status != 0 or "ошибка" in error_output.lower():
            return False, error_output or message
        else:
            return True, message
            
    def ftp_file_uploader(self, local_file_path):
        """ Загружает файлы на FTP тестовой площадки """
        remote_file_path = f"/home/dev/www/{self.environment}/admins_files"
        
        with pysftp.Connection(
            host=self.hostname, username=self.ssh_log, 
            private_key=self.key_path) as sftp:
            sftp.chdir(remote_file_path)
            sftp.put(local_file_path)
            return sftp.listdir()
    
    def ftp_file_reader(self, remote_file_path):
        """ Считывает содержимое файлов на FTP """
        ftp_file_path = f"/home/dev/admin_files/{remote_file_path}"
        with pysftp.Connection(host=self.hostname, username=self.ssh_log, private_key=self.key_path) as sftp:
            with sftp.open(ftp_file_path) as remote_file:
                if "DBF" in ftp_file_path:
                    return remote_file.read()
                else:
                    file_content = io.BytesIO(remote_file.read())
                    return file_content
    
