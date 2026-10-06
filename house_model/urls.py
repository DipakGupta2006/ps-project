from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_price, name='house_predict'),
    path('dashboard/', views.dashboard, name='house_dashboard'),
]
