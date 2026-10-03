from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from .models import Project, Visit
from .forms import ProjectForm

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# --- Vista Pública ---
def index(request):
    ip = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    Visit.objects.create(ip_address=ip, user_agent=user_agent, path=request.path)

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
    return render(request, 'core/project_list.html', {'projects': projects})

# --- DASHBOARD: Redirección genérica ---
@login_required
def dashboard(request):
    # Redirige por defecto a la gestión de proyectos
    return redirect('core:dashboard_projects')

# --- DASHBOARD: Vista de Proyectos (CRUD) ---
@login_required
def dashboard_projects(request):
    projects = Project.objects.all()
    form = ProjectForm()
    context = {
        'projects': projects,
        'form': form,
        'active_tab': 'projects'
    }
    return render(request, 'core/dashboard_projects.html', context)

# --- DASHBOARD: Vista de Métricas ---
@login_required
def dashboard_metrics(request):
    visits = Visit.objects.all()[:30]  # Últimas 30 visitas
    total_visits = Visit.objects.count()
    context = {
        'visits': visits,
        'total_visits': total_visits,
        'active_tab': 'metrics'
    }
    return render(request, 'core/dashboard_metrics.html', context)

# --- Funciones CRUD HTMX ---
@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            projects = Project.objects.all()
            return render(request, 'core/dashboard_project_list.html', {'projects': projects})
    return HttpResponse(status=400)

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            projects = Project.objects.all()
            return render(request, 'core/dashboard_project_list.html', {'projects': projects})
    else:
        form = ProjectForm(instance=project)
    return render(request, 'core/project_form_modal.html', {'form': form, 'project': project})

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        projects = Project.objects.all()
        return render(request, 'core/dashboard_project_list.html', {'projects': projects})
    return HttpResponse(status=400)