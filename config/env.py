from pathlib import Path

config_file = str(Path(__file__).resolve().parent.parent) + '/.env'
"""Конфигурационный файл в корне проекта"""
param_list = {}
"""словарь ключей"""

try:
    with open(config_file) as file:
        for line in file:
            try:
                key, value = line.split("=")
                param_list[key.strip()] = value.replace('\n', '').strip()
            except ValueError:
                continue
except FileNotFoundError:
    print(f"Файл .env не существует. Создайте файл .env. Пример файла - .env.example")


def env(param: str):
    """Извлекает значение параметра"""
    if param in param_list:
        return param_list[param]
    else:
        raise Exception(f"Параметр {param} не существует в .env-файле")
