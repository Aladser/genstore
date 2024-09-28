from django.core.cache import cache


def get_object_list_from_cache(model, key_name: str):
    """Возвращает список элеменетов таблицы БД
        :param model: модель
        :param key_name: ключ кэша
    """

    object_list = cache.get(key_name)
    if object_list is None:
        object_list = model.objects.all()
        cache.set(key_name, object_list)

    return object_list