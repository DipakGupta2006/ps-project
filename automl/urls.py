from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('build/', views.build_model, name='build_model'),
    path('predict/<str:model_name>/', views.predict, name='predict'),
    path('monitor/<str:model_name>/', views.monitor, name='monitor'),
]
