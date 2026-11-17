from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    DepartmentForm,
    LicenseForm,
    SoftwareForm,
    UserRegisterForm,
)
from .models import Department, License, Software


def register(request):
    """Регистрация нового пользователя."""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация выполнена. Добро пожаловать!")
            return redirect("accounting:dashboard")
    else:
        form = UserRegisterForm()
    return render(request, "accounting/register.html", {"form": form})


@login_required
def dashboard(request):
    """Сводка по учёту ПО."""
    today = date.today()
    expiring = License.objects.filter(
        expiry_date__range=[today, today + timedelta(days=30)]
    ).select_related("software", "department")

    category_titles = dict(Software.CATEGORY_CHOICES)
    by_category = [
        (category_titles[row["category"]], row["count"])
        for row in Software.objects.values("category").annotate(count=Count("licenses"))
    ]

    context = {
        "software_count": Software.objects.count(),
        "license_count": License.objects.count(),
        "active_count": License.objects.filter(status="active").count(),
        "expiring_count": expiring.count(),
        "expiring": expiring[:5],
        "recent": License.objects.select_related("software", "department").order_by("-created_at")[:5],
        "by_category": by_category,
        "top_departments": Department.objects.annotate(count=Count("licenses")).order_by("-count")[:5],
    }
    return render(request, "accounting/dashboard.html", context)


# --- Программное обеспечение ---

@login_required
def software_list(request):
    items = Software.objects.annotate(count=Count("licenses"))
    category = request.GET.get("category", "")
    q = request.GET.get("q", "")
    if category:
        items = items.filter(category=category)
    if q:
        items = items.filter(Q(name__icontains=q) | Q(vendor__icontains=q))
    return render(
        request,
        "accounting/software_list.html",
        {
            "items": items,
            "categories": Software.CATEGORY_CHOICES,
            "category": category,
            "q": q,
        },
    )


@login_required
def software_detail(request, pk):
    software = get_object_or_404(Software, pk=pk)
    licenses = software.licenses.select_related("department")
    return render(
        request,
        "accounting/software_detail.html",
        {"software": software, "licenses": licenses},
    )


@login_required
def software_create(request):
    if request.method == "POST":
        form = SoftwareForm(request.POST)
        if form.is_valid():
            software = form.save()
            messages.success(request, "ПО добавлено в реестр")
            return redirect("accounting:software_detail", pk=software.pk)
    else:
        form = SoftwareForm()
    return render(
        request,
        "accounting/software_form.html",
        {"form": form, "title": "Добавить программное обеспечение"},
    )


@login_required
def software_edit(request, pk):
    software = get_object_or_404(Software, pk=pk)
    if request.method == "POST":
        form = SoftwareForm(request.POST, instance=software)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные ПО обновлены")
            return redirect("accounting:software_detail", pk=software.pk)
    else:
        form = SoftwareForm(instance=software)
    return render(
        request,
        "accounting/software_form.html",
        {"form": form, "title": "Редактировать ПО", "software": software},
    )


@login_required
def software_delete(request, pk):
    software = get_object_or_404(Software, pk=pk)
    if request.method == "POST":
        software.delete()
        messages.success(request, "ПО удалено из реестра")
        return redirect("accounting:software_list")
    return render(
        request,
        "accounting/confirm_delete.html",
        {"object": software, "back_url": "accounting:software_list", "title": "ПО"},
    )


# --- Подразделения ---

@login_required
def department_list(request):
    items = Department.objects.annotate(count=Count("licenses"))
    return render(request, "accounting/department_list.html", {"items": items})


@login_required
def department_create(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Подразделение добавлено")
            return redirect("accounting:department_list")
    else:
        form = DepartmentForm()
    return render(
        request,
        "accounting/department_form.html",
        {"form": form, "title": "Добавить подразделение"},
    )


@login_required
def department_edit(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Подразделение обновлено")
            return redirect("accounting:department_list")
    else:
        form = DepartmentForm(instance=department)
    return render(
        request,
        "accounting/department_form.html",
        {"form": form, "title": "Редактировать подразделение", "department": department},
    )


@login_required
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        department.delete()
        messages.success(request, "Подразделение удалено")
        return redirect("accounting:department_list")
    return render(
        request,
        "accounting/confirm_delete.html",
        {"object": department, "back_url": "accounting:department_list", "title": "подразделение"},
    )


# --- Лицензии ---

@login_required
def license_list(request):
    items = License.objects.select_related("software", "department")
    status = request.GET.get("status", "")
    software_id = request.GET.get("software", "")
    department_id = request.GET.get("department", "")
    q = request.GET.get("q", "")

    if status:
        items = items.filter(status=status)
    if software_id:
        items = items.filter(software_id=software_id)
    if department_id:
        items = items.filter(department_id=department_id)
    if q:
        items = items.filter(
            Q(inventory_number__icontains=q)
            | Q(license_key__icontains=q)
            | Q(responsible__icontains=q)
            | Q(software__name__icontains=q)
        )

    return render(
        request,
        "accounting/license_list.html",
        {
            "items": items,
            "statuses": License.STATUS_CHOICES,
            "softwares": Software.objects.all(),
            "departments": Department.objects.all(),
            "filters": {
                "status": status,
                "software": software_id,
                "department": department_id,
                "q": q,
            },
        },
    )


@login_required
def license_detail(request, pk):
    license = get_object_or_404(License, pk=pk)
    return render(request, "accounting/license_detail.html", {"license": license})


@login_required
def license_create(request):
    if request.method == "POST":
        form = LicenseForm(request.POST)
        if form.is_valid():
            license = form.save(commit=False)
            license.created_by = request.user
            license.save()
            messages.success(request, "Лицензия учтена")
            return redirect("accounting:license_detail", pk=license.pk)
    else:
        form = LicenseForm()
    return render(
        request,
        "accounting/license_form.html",
        {"form": form, "title": "Учесть лицензию"},
    )


@login_required
def license_edit(request, pk):
    license = get_object_or_404(License, pk=pk)
    if request.method == "POST":
        form = LicenseForm(request.POST, instance=license)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные лицензии обновлены")
            return redirect("accounting:license_detail", pk=license.pk)
    else:
        form = LicenseForm(instance=license)
    return render(
        request,
        "accounting/license_form.html",
        {"form": form, "title": "Редактировать лицензию", "license": license},
    )


@login_required
def license_delete(request, pk):
    license = get_object_or_404(License, pk=pk)
    if request.method == "POST":
        license.delete()
        messages.success(request, "Лицензия удалена из учёта")
        return redirect("accounting:license_list")
    return render(
        request,
        "accounting/confirm_delete.html",
        {"object": license, "back_url": "accounting:license_list", "title": "лицензию"},
    )
