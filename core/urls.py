from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.BaseView.as_view()),
    path("polarize/", views.PolarizeFunctionView.as_view()),
    path("truth-table/", views.TruthTableView.as_view()),
    path("extends/", views.IndexView.as_view())
]
