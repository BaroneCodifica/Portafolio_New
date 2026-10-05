import logging
import smtplib

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.db.models import Q
from django.urls import reverse
from django.views.decorators.http import require_POST
from .models import Project, Visit
from .forms import ContactForm, ProjectForm
from courses.models import Course
from courses.forms import CourseForm

logger = logging.getLogger(__name__)


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
    return render(request, 'core/index.html', {
        'projects': projects,
        'contact_form': ContactForm(),
    })


@require_POST
def contact(request):
    form = ContactForm(request.POST)
    if not form.is_valid():
        return render(request, 'core/index.html', {
            'projects': Project.objects.all(),
            'contact_form': form,
        }, status=400)

    name = form.cleaned_data['name']
    sender = form.cleaned_data['email']
    subject = form.cleaned_data['subject']
    body = form.cleaned_data['message']
    message_body = f"Mensaje de {name} <{sender}>\n\n{body}"

    try:
        sent_count = EmailMessage(
            subject=f"[Portafolio] {subject}",
            body=message_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_EMAIL],
            reply_to=[sender],
        ).send(fail_silently=False)
    except (OSError, smtplib.SMTPException):
        logger.exception("No se pudo enviar un mensaje desde el formulario de contacto.")
        messages.error(
            request,
            "No se pudo enviar tu mensaje en este momento. Inténtalo más tarde o escríbeme directamente por correo.",
        )
    else:
        if sent_count != 1:
            logger.error("El backend de correo no aceptó el mensaje del formulario de contacto.")
            messages.error(
                request,
                "No se pudo confirmar el envío de tu mensaje. Inténtalo más tarde o escríbeme directamente por correo.",
            )
        else:
            messages.success(request, "¡Gracias! Tu mensaje fue enviado correctamente.")

    return redirect(f"{reverse('core:index')}#contacto")

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




# --- DASHBOARD: Vista de Cursos (CRUD) ---
@login_required
def dashboard_courses(request):
    courses = Course.objects.all()
    form = CourseForm()
    context = {
        'courses': courses,
        'form': form,
        'active_tab': 'courses'
    }
    return render(request, 'core/dashboard_courses.html', context)

# --- DASHBOARD: Vista de Métricas Mejoradas ---
@login_required
def dashboard_metrics(request):
    # Límite estricto de máximo 10 registros por tabla
    portfolio_visits = Visit.objects.filter(path='/')[:10]
    course_visits = Visit.objects.filter(path__startswith='/cursos/')[:10]
    
    total_visits = Visit.objects.count()
    total_course_visits = Visit.objects.filter(path__startswith='/cursos/').count()

    context = {
        'portfolio_visits': portfolio_visits,
        'course_visits': course_visits,
        'total_visits': total_visits,
        'total_course_visits': total_course_visits,
        'active_tab': 'metrics'
    }
    return render(request, 'core/dashboard_metrics.html', context)

# --- Funciones CRUD HTMX para Cursos ---
@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            courses = Course.objects.all()
            return render(request, 'core/dashboard_course_list.html', {'courses': courses})
    return HttpResponse(status=400)

@login_required
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        courses = Course.objects.all()
        return render(request, 'core/dashboard_course_list.html', {'courses': courses})
    return HttpResponse(status=400)