from django.shortcuts import render
from django.db.models import Q
from .models import Project

def index(request):
    projects = Project.objects.all()
    return render(request, 'core/index.html', {'projects': projects})

def search_projects(request):
    query = request.GET.get('search', '')
    if query:
        projects = Project.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tech_stack__icontains=query)
        )
    else:
        projects = Project.objects.all()
    
    # Devolvemos ÚNICAMENTE la plantilla parcial 'project_list.html'
    return render(request, 'core/project_list.html', {'projects': projects})