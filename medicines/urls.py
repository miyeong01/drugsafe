from django.urls import path
from . import views


urlpatterns = [
    path('drugs/', views.drug_list),
]
