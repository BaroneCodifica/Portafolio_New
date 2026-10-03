from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_projects, name='search_projects'),
    
    # Rutas del Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/proyectos/', views.dashboard_projects, name='dashboard_projects'),
    path('dashboard/metricas/', views.dashboard_metrics, name='dashboard_metrics'),
    
    # Acciones CRUD HTMX
    path('dashboard/proyectos/crear/', views.create_project, name='create_project'),
    path('dashboard/proyectos/editar/<int:pk>/', views.edit_project, name='edit_project'),
    path('dashboard/proyectos/eliminar/<int:pk>/', views.delete_project, name='delete_project'),
]