from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.hello, name="hello"),
    path("risk-demo/", views.risk_demo, name="risk_demo"),
    path("loan-applications/", views.loan_applications, name="loan_applications"),
]