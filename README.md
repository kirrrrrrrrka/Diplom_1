## Задание 1: Юнит-тесты

### Автотесты для проверки программы, которая помогает заказать бургер в Stellar Burgers

### Реализованные сценарии

Созданы юнит-тесты, покрывающие классы `Burger`

Процент покрытия 100% (отчет: `htmlcov/index.html`)

В тестах используются моки и параметризация.

Покрытие кода: 100% для praktikum/burger.py

### Структура проекта

- `praktikum` - код программы
- `tests` - тесты



### Запуск автотестов

**Установка зависимостей**

> `$ pip install -r requirements.txt`

**Запуск автотестов и создание HTML-отчета о покрытии**

>  `python -m pytest -v --cov=praktikum.burger --cov-report=term-missing`
>  `python -m pytest --cov=praktikum.burger --cov-report=html`
