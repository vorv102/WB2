from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Department, License, Software


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": "Имя пользователя",
            "password1": "Пароль",
            "password2": "Подтверждение пароля",
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ("name", "code", "description")
        labels = {
            "name": "Название подразделения",
            "code": "Код",
            "description": "Описание",
        }
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}


class SoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        fields = ("name", "vendor", "version", "category", "is_critical", "description")
        labels = {
            "name": "Наименование",
            "vendor": "Разработчик / вендор",
            "version": "Версия",
            "category": "Категория",
            "is_critical": "Критичное ПО",
            "description": "Описание",
        }
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}


class LicenseForm(forms.ModelForm):
    class Meta:
        model = License
        fields = (
            "software",
            "department",
            "inventory_number",
            "license_key",
            "quantity",
            "purchase_date",
            "expiry_date",
            "responsible",
            "status",
            "notes",
        )
        labels = {
            "software": "Программное обеспечение",
            "department": "Подразделение",
            "inventory_number": "Инвентарный номер",
            "license_key": "Лицензионный ключ",
            "quantity": "Количество",
            "purchase_date": "Дата покупки",
            "expiry_date": "Дата окончания",
            "responsible": "Ответственный",
            "status": "Статус",
            "notes": "Примечание",
        }
        widgets = {
            "purchase_date": forms.DateInput(attrs={"type": "date"}),
            "expiry_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
