import os.path
from pathlib import Path

param_list = {}
"""словарь ключей"""

immersion = 1
# начальная папка поиска
root_dir = Path(__file__).resolve().parent
dir_start = str(root_dir)

# поиск корневой папки конфиг.файла
while True:
    if os.path.isfile(str(root_dir) + '/manage.py'):
        config_file = str(root_dir) + '/.env'

        # поиск конфиг.файла
        if os.path.isfile(config_file):
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
            raise FileNotFoundError("Файл .env не найден. Создайте файл .env (пример файла - .env.example")
    else:
        # защита от бесконечного цикла
        if immersion > 3:
            raise FileNotFoundError(f"Файл .env не найден. Начало поиска - {dir_start}")
        immersion += 1

        root_dir = root_dir.parent


def env(param: str):
    """Извлекает значение параметра конфигурационный файла"""

    if param in param_list:
        return param_list[param]
    else:
        raise Exception(f"Параметр {param} не существует в .env-файле")
