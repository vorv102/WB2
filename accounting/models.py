from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Department(models.Model):
    """Подразделение предприятия (нефтегазовой компании)."""

    name = models.CharField(max_length=150, verbose_name="Название подразделения")
    code = models.CharField(max_length=20, unique=True, verbose_name="Код")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Software(models.Model):
    """Программное обеспечение, используемое на предприятии."""

    CATEGORY_CHOICES = [
        ("geology", "Геология и разведка"),
        ("drilling", "Бурение"),
        ("production", "Добыча нефти и газа"),
        ("refining", "Переработка и нефтехимия"),
        ("transport", "Транспорт и логистика"),
        ("scada", "SCADA / АСУ ТП"),
        ("erp", "ERP и финансы"),
        ("security", "Информационная безопасность"),
        ("it", "ИТ-инфраструктура"),
        ("cad", "САПР и проектирование"),
    ]

    name = models.CharField(max_length=200, verbose_name="Наименование")
    vendor = models.CharField(max_length=150, verbose_name="Разработчик / вендор")
    version = models.CharField(max_length=50, verbose_name="Версия")
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, verbose_name="Категория"
    )
    is_critical = models.BooleanField(default=False, verbose_name="Критичное ПО")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Программное обеспечение"
        verbose_name_plural = "Программное обеспечение"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} {self.version}"

    def get_absolute_url(self):
        return reverse("accounting:software_detail", args=[self.pk])

    def license_count(self):
        return self.licenses.count()


class License(models.Model):
    """Учётная запись / лицензия на ПО, закреплённая за подразделением."""

    STATUS_CHOICES = [
        ("active", "Активна"),
        ("expiring", "Истекает"),
        ("revoked", "Аннулирована"),
        ("reserve", "Резерв"),
    ]

    software = models.ForeignKey(
        Software,
        on_delete=models.CASCADE,
        related_name="licenses",
        verbose_name="Программное обеспечение",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="licenses",
        verbose_name="Подразделение",
    )
    inventory_number = models.CharField(
        max_length=50, unique=True, verbose_name="Инвентарный номер"
    )
    license_key = models.CharField(max_length=200, blank=True, verbose_name="Лицензионный ключ")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    purchase_date = models.DateField(verbose_name="Дата покупки")
    expiry_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания")
    responsible = models.CharField(max_length=150, verbose_name="Ответственный")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="active", verbose_name="Статус"
    )
    notes = models.TextField(blank=True, verbose_name="Примечание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Учтено")
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Добавил",
    )

    class Meta:
        verbose_name = "Лицензия"
        verbose_name_plural = "Лицензии"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.inventory_number} — {self.software.name}"

    def get_absolute_url(self):
        return reverse("accounting:license_detail", args=[self.pk])

    @property
    def days_left(self):
        """Сколько дней осталось до окончания лицензии."""
        if not self.expiry_date:
            return None
        return (self.expiry_date - date.today()).days
