from allure_commons import hookimpl
from allure_commons.logger import AllureFileLogger

INDENT = 4

class AllureFileLoggerMode(AllureFileLogger):
    """ Класс генерирует json файлы Allure отчёта
    - если тест passed - json файл не генерируется
    - в остальных случаях - генерируется
    """
    def __init__(self, report_dir, clean=False):
        super().__init__(report_dir, clean=False)

    @hookimpl
    def report_result(self, result):
        """ Сохраняет json фал теста """
        if result.status == "passed":
            pass
        else:
            self._report_item(result)

    @hookimpl
    def report_container(self, container):
        """ Сохраняет json файл фикстур и параметров """
        if container.befores[0].status == "passed":
            pass
        else:
            self._report_item(container)