from django.db import models

from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    image = models.ImageField(upload_to='projects/', verbose_name="Imagen del Proyecto")
    tech_stack = models.CharField(max_length=200, verbose_name="Tecnologías (ej: Python, Django, Tailwind)")
    repo_url = models.URLField(blank=True, null=True, verbose_name="Enlace al Repositorio (GitHub)")
    live_url = models.URLField(blank=True, null=True, verbose_name="Enlace a Demo/Sitio en vivo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        ordering = ['-created_at'] # Muestra los proyectos más recientes primero

    def __str__(self):
        return self.title