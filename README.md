Организация тестов в `pytest` зависит от нескольких факторов, включая сложность функционала, количество проверок и предпочтения команды. Вот несколько рекомендаций по организации тестов:

### 1. Разделение по функционалу

Рекомендуется разделять тесты по функционалу, создавая отдельные файлы для различных аспектов приложения. Например, вы можете иметь:

- `test_authorization.py` для тестов авторизации
- `test_deals.py` для тестов сделок
- `test_profile.py` для тестов профиля пользователя

### 2. Использование функций для тестов

Каждый тест должен проверять одну конкретную вещь. Это делает тесты более понятными и легкими для отладки. Например, вместо того чтобы объединять все проверки авторизации в одну функцию, лучше создать отдельные тесты для каждой проверки:

```python
def test_open_auth_page(auth_page):
    """ Проверка доступности страницы авторизации """
    auth_page.open_page()
    assert auth_page.checking_auth_page_is_open() == "Авторизация"

def test_enter_login(auth_page):
    """ Проверка ввода логина """
    auth_page.enter_login()
    assert auth_page.checking_login_field() == AuthData.LOGIN

def test_enter_password(auth_page):
    """ Проверка ввода пароля """
    auth_page.enter_password()
    assert auth_page.checking_password_field() == AuthData.PASSWORD

def test_click_login_button(auth_page):
    """ Проверка нажатия кнопки 'Войти' """
    auth_page.click_login_button()
    assert not auth_page.authorization_error()

def test_checking_login_successful(auth_page):
    """ Проверка успешной авторизации """
    assert auth_page.checking_login_successful() == "Новости"
```

### 3. Группировка тестов

Если у вас есть много тестов, которые относятся к одной и той же функциональности, вы можете использовать классы или модули для группировки тестов. Например:

```python
class TestAuthorization:
    def test_open_auth_page(self, auth_page):
        # ...

    def test_enter_login(self, auth_page):
        # ...

    # Другие тесты...
```

### 4. Использование параметризации

Если у вас есть похожие тесты с разными входными данными, вы можете использовать параметризацию для уменьшения дублирования кода:

```python
import pytest

@pytest.mark.parametrize("login, password, expected", [
    (AuthData.LOGIN, AuthData.PASSWORD, "Новости"),
    # Другие комбинации...
])
def test_login(auth_page, login, password, expected):
    auth_page.enter_login(login)
    auth_page.enter_password(password)
    auth_page.click_login_button()
    assert auth_page.checking_login_successful() == expected
```

### 5. Чистота и поддерживаемость

Важно, чтобы тесты были чистыми и поддерживаемыми. Если вы видите, что тесты становятся слишком сложными или длинными, это может быть признаком того, что их стоит разбить на более мелкие части.

### Заключение

В общем, лучше создавать отдельные функции для проверки каждого элемента функционала, чтобы тесты были более понятными и легкими для отладки. Это также упрощает поддержку и расширение тестов в будущем.

# Описание проекта

### Запуск тестов
Запуск тестов выполоняется следующей командой:
`pytest tests` - запускает все тесты, находящиеся в папке 'tests'
`pytest tests/path/to/file.py` - запускает тесты в указанном модуле

Опции:
`-v` - выводит в консоль подробное описание ошибок
`-s` - выводит в консоль print() из методов
`--env=prod` - запускает тесты в продуктовой среде
`--env=dev` - запускает тесты на тестовой площадке
`--alluredir=allure-results` - запуск теста с генерацией отчета Allure

Если требуется запустить тесты на конкретной тестовой площадке, то требуется запустить тесты с опциями:
`--env=dev --url=54448` - запускает тесты на тестовой площадке 54448

Просмотр отчета после выполнении тестов:
`allure serve allure-results` - запустить команду после завершения всех тестов

Пример запуска:
```pytest --alluredir=allure-results --env=dev --url=54448 -v tests/base/test_authorization.py tests/deal/test_reorder_boutiques.py```
В данном примере запускается автотест test_reorder_boutiques.py с генерацией атчета Allure, в dev-среде (https://54448.crm.taskfactory.ru/) с подробным выводом результатов в консаоль 

