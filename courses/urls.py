from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.academy_home, name='academy_home'),
    path('<slug:slug>/', views.course_detail, name='course_detail'),
]