from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_marks, name='student_predict'),
    path('dashboard/', views.dashboard, name='student_dashboard'),
]
