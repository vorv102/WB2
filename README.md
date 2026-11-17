# Учёт программного обеспечения на предприятии нефтегазовой отрасли

Веб-приложение на **Django 5.2 + SQLite** для учёта ПО, лицензий и подразделений нефтегазового предприятия.

## Возможности

- Авторизация: регистрация, вход/выход, защита всех страниц через `@login_required`
- 3 таблицы БД: `Department` (подразделения), `Software` (ПО), `License` (лицензии)
- Формы (`ModelForm`) для создания и редактирования всех сущностей
- Дашборд со сводкой: всего ПО, лицензий, активных, истекающих через 30 дней
- Поиск и фильтры по ПО (категория, вендор) и лицензиям (статус, ПО, подразделение, инв. номер)
- Полный CRUD с подтверждением удаления
- Админка `/admin/`
- Демо-данные загружаются миграциями: 6 подразделений, 16 позиций известного ПО (Microsoft, Oracle, 1С, SAP, AutoCAD, Siemens, ABB, Kaspersky, Schlumberger, AspenTech) и 17 лицензий

## Запуск

```powershell
python -m pip install django
python manage.py migrate
python manage.py createsuperuser   # для доступа к /admin/
python manage.py runserver
```

Откройте http://127.0.0.1:8000/ и зарегистрируйтесь.

База данных `db.sqlite3` не хранится в репозитории — она создаётся командой `migrate` вместе с демо-данными.

## Структура

```
softaccount/
├── manage.py
├── neftegaz/            # настройки проекта
│   ├── settings.py
│   └── urls.py
├── accounting/          # приложение учёта ПО
│   ├── models.py        # Department, Software, License
│   ├── forms.py         # 4 формы
│   ├── views.py         # логика и CRUD
│   ├── urls.py
│   ├── admin.py
│   ├── migrations/      # 0001–0003 (в т.ч. демо-данные)
│   └── templates/
│       ├── base.html
│       ├── registration/login.html
│       └── accounting/*.html
└── static/style.css
```
