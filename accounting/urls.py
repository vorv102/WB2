from django.urls import path

from . import views

app_name = "accounting"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),

    path("software/", views.software_list, name="software_list"),
    path("software/new/", views.software_create, name="software_create"),
    path("software/<int:pk>/", views.software_detail, name="software_detail"),
    path("software/<int:pk>/edit/", views.software_edit, name="software_edit"),
    path("software/<int:pk>/delete/", views.software_delete, name="software_delete"),

    path("departments/", views.department_list, name="department_list"),
    path("departments/new/", views.department_create, name="department_create"),
    path("departments/<int:pk>/edit/", views.department_edit, name="department_edit"),
    path("departments/<int:pk>/delete/", views.department_delete, name="department_delete"),

    path("licenses/", views.license_list, name="license_list"),
    path("licenses/new/", views.license_create, name="license_create"),
    path("licenses/<int:pk>/", views.license_detail, name="license_detail"),
    path("licenses/<int:pk>/edit/", views.license_edit, name="license_edit"),
    path("licenses/<int:pk>/delete/", views.license_delete, name="license_delete"),
]
