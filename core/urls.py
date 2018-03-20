from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.IndexView.as_view()),
    path("truth-table/", views.TruthTableView.as_view()),
]
