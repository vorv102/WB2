from datetime import date, timedelta

from django.db import migrations, models


CATEGORIES = [
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

OLD_SOFTWARE_NAMES = {
    "Petrel",
    "Eclipse",
    "RMS",
    "Landmark DecisionSpace",
    "Aspen HYSYS",
    "Honeywell Experion PKS",
    "SAP ERP",
    "Kaspersky Industrial CyberSecurity",
}

SOFTWARE = [
    ("Microsoft Windows Server", "Microsoft", "2022", "it", True, "Операционная система для серверов и доменной инфраструктуры"),
    ("Microsoft SQL Server", "Microsoft", "2022", "it", True, "СУБД для корпоративных информационных систем"),
    ("Microsoft 365", "Microsoft", "2024", "it", False, "Офисный пакет и облачные сервисы совместной работы"),
    ("Oracle Database", "Oracle", "19c", "it", True, "Корпоративная СУБД для критически важных приложений"),
    ("1С:Предприятие 8.3", "1С", "8.3", "erp", True, "Автоматизация бухгалтерского, кадрового и управленческого учёта"),
    ("SAP S/4HANA", "SAP", "2023", "erp", True, "ERP для управления финансами, закупками и логистикой"),
    ("AutoCAD", "Autodesk", "2024", "cad", False, "САПР для проектирования и выпуска чертежей"),
    ("Autodesk Navisworks", "Autodesk", "2024", "cad", False, "Координация и визуализация проектной документации"),
    ("Siemens SIMATIC PCS 7", "Siemens", "9.0", "scada", True, "Распределённая система управления технологическими процессами"),
    ("ABB Ability 800xA", "ABB", "6.1", "scada", True, "Платформа автоматизации для добычи и переработки"),
    ("Schneider EcoStruxure", "Schneider Electric", "2023", "scada", False, "Управление и мониторинг инженерной инфраструктуры"),
    ("Kaspersky Endpoint Security", "Kaspersky", "12.0", "security", True, "Защита рабочих станций и серверов"),
    ("Kaspersky Industrial CyberSecurity", "Kaspersky", "4.0", "security", True, "Защита промышленных сетей и АСУ ТП"),
    ("Petrel", "Schlumberger", "2023.1", "geology", True, "Геомоделирование и интерпретация сейсмических данных"),
    ("Eclipse", "Schlumberger", "2022.2", "production", True, "Гидродинамическое моделирование месторождений"),
    ("Aspen HYSYS", "AspenTech", "14.0", "refining", True, "Моделирование и оптимизация процессов НПЗ"),
]

LICENSES = [
    ("Microsoft Windows Server", "IT", "LIC-IT-001", "MS-WIN-2022-001", 50, -400, 330, "Морозов П.Л.", "active", "Корпоративная лицензия"),
    ("Microsoft SQL Server", "IT", "LIC-IT-002", "MS-SQL-2022-014", 20, -350, 15, "Орлов С.М.", "active", "Требуется продление"),
    ("Microsoft 365", "IT", "LIC-IT-003", "M365-2024-210", 200, -200, 165, "Морозов П.Л.", "active", "Подписка E5"),
    ("Oracle Database", "IT", "LIC-IT-004", "ORA-19C-0071", 12, -300, 240, "Ким А.Ю.", "active", ""),
    ("1С:Предприятие 8.3", "IT", "LIC-IT-005", "1C-83-45120", 60, -250, 280, "Никитина О.В.", "active", "Корпоративная лицензия на 60 рабочих мест"),
    ("SAP S/4HANA", "IT", "LIC-IT-006", "SAP-S4-2023-77", 50, -180, 540, "Соколов А.И.", "active", ""),
    ("AutoCAD", "DRL", "LIC-DRL-007", "ACD-2024-118", 15, -150, 210, "Кузнецов Д.Н.", "active", "Проектирование буровых"),
    ("AutoCAD", "GEO", "LIC-GEO-008", "ACD-2024-119", 10, -120, 60, "Иванов И.С.", "active", ""),
    ("Autodesk Navisworks", "REF", "LIC-REF-009", "NAV-2024-033", 5, -100, 265, "Попова Е.А.", "active", ""),
    ("Siemens SIMATIC PCS 7", "REF", "LIC-REF-010", "SIE-PCS7-2201", 8, -500, 30, "Смирнов В.И.", "active", "АСУ ТП установки катализа"),
    ("ABB Ability 800xA", "PRD", "LIC-PRD-011", "ABB-800XA-410", 6, -450, 120, "Петров А.В.", "active", ""),
    ("Schneider EcoStruxure", "LOG", "LIC-LOG-012", "SCH-ECO-114", 4, -220, 140, "Васильев Р.Т.", "active", ""),
    ("Kaspersky Endpoint Security", "IT", "LIC-IT-013", "KES-12-9081", 250, -90, 275, "Орлов С.М.", "active", ""),
    ("Kaspersky Industrial CyberSecurity", "REF", "LIC-REF-014", "KICS-4-3021", 25, -80, 285, "Попова Е.А.", "active", "Защита контура АСУ ТП"),
    ("Petrel", "GEO", "LIC-GEO-015", "PTRL-2023-8891", 5, -380, 20, "Сидоров К.П.", "active", "Годовая подписка"),
    ("Aspen HYSYS", "REF", "LIC-REF-016", "ASP-14-6650", 6, -200, 15, "Смирнов В.И.", "active", "Плановое продление"),
    ("Eclipse", "PRD", "LIC-PRD-017", "ECL-2022-4410", 3, -360, 95, "Петров А.В.", "reserve", "Резервный комплект"),
]


def update_catalog(apps, schema_editor):
    Software = apps.get_model("accounting", "Software")
    License = apps.get_model("accounting", "License")
    Department = apps.get_model("accounting", "Department")

    # Удаляем только демонстрационные записи, сохранённые пользователем данные не трогаем
    License.objects.filter(inventory_number__startswith="LIC-").delete()
    Software.objects.filter(name__in=OLD_SOFTWARE_NAMES).delete()

    softwares = {}
    for name, vendor, version, category, critical, description in SOFTWARE:
        softwares[name], _ = Software.objects.get_or_create(
            name=name,
            defaults={
                "vendor": vendor,
                "version": version,
                "category": category,
                "is_critical": critical,
                "description": description,
            },
        )

    departments = {dep.code: dep for dep in Department.objects.all()}
    today = date.today()
    for name, dep_code, inv, key, qty, purchased, expires, responsible, status, notes in LICENSES:
        License.objects.get_or_create(
            inventory_number=inv,
            defaults={
                "software": softwares[name],
                "department": departments[dep_code],
                "license_key": key,
                "quantity": qty,
                "purchase_date": today + timedelta(days=purchased),
                "expiry_date": today + timedelta(days=expires),
                "responsible": responsible,
                "status": status,
                "notes": notes,
            },
        )


class Migration(migrations.Migration):
    dependencies = [("accounting", "0002_demo_data")]

    operations = [
        migrations.AlterField(
            model_name="software",
            name="category",
            field=models.CharField(choices=CATEGORIES, max_length=20, verbose_name="Категория"),
        ),
        migrations.RunPython(update_catalog, migrations.RunPython.noop),
    ]
