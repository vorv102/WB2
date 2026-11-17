from datetime import date, timedelta

from django.db import migrations


def load_demo_data(apps, schema_editor):
    Department = apps.get_model("accounting", "Department")
    Software = apps.get_model("accounting", "Software")
    License = apps.get_model("accounting", "License")

    departments = {}
    for code, name, description in [
        ("GEO", "Геологическая служба", "Геологоразведочные работы, поиск и разведка месторождений"),
        ("DRL", "Управление бурения", "Проектирование и сопровождение буровых работ"),
        ("PRD", "Управление добычи нефти и газа", "Эксплуатация скважин и промысловое оборудование"),
        ("REF", "Нефтеперерабатывающий завод", "Переработка сырья и контроль технологических процессов"),
        ("LOG", "Служба логистики", "Транспортировка и учёт материальных потоков"),
        ("IT", "Служба информационных технологий", "Поддержка ИТ-инфраструктуры предприятия"),
    ]:
        departments[code], _ = Department.objects.get_or_create(
            code=code, defaults={"name": name, "description": description}
        )

    software = {}
    for key, name, vendor, version, category, critical, description in [
        ("petrel", "Petrel", "Schlumberger", "2023.1", "geology", True, "Геомоделирование и интерпретация сейсмических данных"),
        ("eclipse", "Eclipse", "Schlumberger", "2022.2", "production", True, "Гидродинамическое моделирование месторождений"),
        ("rms", "RMS", "Roxar", "12.0", "geology", False, "Построение геологических и резервуарных моделей"),
        ("landmark", "Landmark DecisionSpace", "Halliburton", "15.0", "drilling", True, "Проектирование траекторий скважин и буровых работ"),
        ("hysys", "Aspen HYSYS", "AspenTech", "14.0", "refining", True, "Моделирование и оптимизация технологических процессов НПЗ"),
        ("experion", "Honeywell Experion PKS", "Honeywell", "R520", "scada", True, "Распределённая система управления технологическими процессами"),
        ("sap", "SAP ERP", "SAP", "S/4HANA", "erp", False, "Управление финансами, закупками и персоналом"),
        ("kaspersky", "Kaspersky Industrial CyberSecurity", "Kaspersky", "4.0", "security", True, "Защита промышленных сетей и АСУ ТП"),
    ]:
        software[key], _ = Software.objects.get_or_create(
            name=name,
            defaults={
                "vendor": vendor,
                "version": version,
                "category": category,
                "is_critical": critical,
                "description": description,
            },
        )

    today = date.today()
    records = [
        ("petrel", "GEO", "LIC-GEO-001", "PTRL-2023-8891", 5, -400, 330, "Иванов И.С.", "active", "Годовая подписка"),
        ("eclipse", "PRD", "LIC-PRD-002", "ECL-2022-4410", 3, -380, 20, "Петров А.В.", "expiring", "Требуется продление"),
        ("rms", "GEO", "LIC-GEO-003", "RMS-12-7734", 2, -300, 420, "Сидоров К.П.", "active", ""),
        ("landmark", "DRL", "LIC-DRL-004", "LM-15-0021", 4, -250, 95, "Кузнецов Д.Н.", "active", "Расширение пула лицензий"),
        ("hysys", "REF", "LIC-REF-005", "ASP-14-6650", 6, -200, 15, "Смирнов В.И.", "active", "Плановое продление в текущем квартале"),
        ("experion", "REF", "LIC-REF-006", "HW-520-1198", 10, -500, 250, "Попова Е.А.", "active", "Лицензии на серверы и рабочие станции"),
        ("sap", "IT", "LIC-IT-007", "SAP-S4-2024-77", 50, -180, 540, "Морозов П.Л.", "active", "Корпоративная лицензия"),
        ("kaspersky", "IT", "LIC-IT-008", "KICS-4-3021", 25, -100, 265, "Орлов С.М.", "active", ""),
        ("petrel", "DRL", "LIC-DRL-009", "PTRL-2023-8892", 2, -90, 275, "Васильев Р.Т.", "reserve", "Резервный комплект"),
        ("sap", "LOG", "LIC-LOG-010", "SAP-S4-2024-78", 8, -120, -30, "Никитина О.В.", "revoked", "Лицензии аннулированы при реорганизации"),
    ]
    for soft_key, dep_code, inv, key, qty, purchased, expires, responsible, status, notes in records:
        License.objects.get_or_create(
            inventory_number=inv,
            defaults={
                "software": software[soft_key],
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
    dependencies = [("accounting", "0001_initial")]

    operations = [
        migrations.RunPython(load_demo_data, migrations.RunPython.noop),
    ]
