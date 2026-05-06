from django.urls import path
from . import views
urlpatterns=[
    path("", views.home, name="home"),
    path("records/", views.records_list, name="records_list"),
    path("records/add/", views.add_record, name="add_record"),
    path("records/<int:pk>/edit/", views.edit_record, name="edit_record"),
    path("records/<int:pk>/delete/", views.delete_record, name="delete_record"),
    path("passbook/all/", views.passbook_all, name="passbook_all"),
    path("passbook/branch/", views.passbook_branch, name="passbook_branch"),
    path("passbook/applicant/", views.passbook_applicant, name="passbook_applicant"),
    path("sql/", views.sql_queries, name="sql_queries"),
    path("source/", views.source_code, name="source_code"),
    path("health/", views.healthcheck, name="healthcheck"),
]
