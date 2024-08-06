# Магазин

### Настройки проекта
+ cоздать файл **.env** в корне проекта с полями, аналогичными *.env.example*
+ заполнение БД - ``python manage.py seed``
+ создание суперпользователя - ``python manage.py createadmin``
+ создание групп пользователей - ``python manage.py user_groups``

#### Приложения
+ ``authen`` - пользователи
+ ``product`` - товары
+ ``blog`` - блоги

#### Модели
* ``authen``
  + ``User`` - пользователь
  +  ``Country`` - страна
* ``product``
  + ``Category`` - категория
  + ``Product``  - товар
  + ``ProductVersion`` - версия товара
+ ``blog``
  + ``Blog`` - блог


#### Контроллеры
+ ``product`` - товар CRUID
+ ``blog`` - блог CRUID
+ ``authen`` - пользователь: авторизация, выход из системы, регистрация, редактирование, сброс пароля


#### Формы
* ``product``
  + ``ProductForm`` - товар
  + ``ProductVersionForm`` - веосия товара
+ ``blog``
  + ``BlogForm`` - блог
* ``authen``
  + ``AuthForm`` - авторизация пользователя
  + ``RegisterForm`` - регистрация пользователя
  + ``ProfileForm`` - редактирование пользователя
  + ``CustomPasswordResetForm`` - сброс пароля пользователя

#### Кэширование
+ ``product.views.ProductDetailView`` - на уровне представления
+ ``product.services.get_object_list_from_cache`` - запросы списка элементов модели
+ ``libs.env.env()`` - функция чтения конфигурационного файла .env
