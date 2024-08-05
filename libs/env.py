import os.path
from pathlib import Path

"""
    Конфигурационный файл в корне проекта
    Погружение не более 3 уровней вверх от корневой папки
"""
param_list = {}
"""словарь ключей"""

immersion = 1
# начальная папка поиска
root_dir = Path(__file__).resolve().parent
dir_start = str(root_dir)

while True:
    if os.path.isfile(str(root_dir.resolve()) + '/manage.py'):
        # поиск корневой папки конфиг.файла
        config_file = str(root_dir) + '/.env'
        if os.path.isfile(config_file):
            # поиск конфиг.файла
            with open(config_file) as file:
                # чтение параметров конфиг.файла
                for line in file:
                    try:
                        key, value = line.split("=")
                        param_list[key.strip()] = value.replace('\n', '').strip()
                    except ValueError:
                        continue
            break
        else:
            raise FileNotFoundError("Файл .env не найден. Создайте файл .env. Пример файла - .env.example")
    else:
        # защита, если что-то пошло не так
        if immersion > 3:
            raise FileNotFoundError(f"Файл .env не найден. Начало поиска - {dir_start}")
        immersion += 1

        root_dir = root_dir.parent


def env(param: str):
    """Извлекает значение параметра"""
    if param in param_list:
        return param_list[param]
    else:
        raise Exception(f"Параметр {param} не существует в .env-файле")
