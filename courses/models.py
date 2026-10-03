from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(models.Model):
    COURSE_TYPE_CHOICES = [
        ('free', 'Curso Gratuito'),
        ('tutorized', 'Curso Tutorizado'),
        ('offline', 'Curso Offline / Descargable'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    subtitle = models.CharField(max_length=255, help_text="Ej: Aprende paso a paso con ejercicios prácticos")
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    course_type = models.CharField(max_length=20, choices=COURSE_TYPE_CHOICES, default='free')
    
    # Precios y visibilidad
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_published = models.BooleanField(default=True)
    cover_image = models.ImageField(upload_to='courses/covers/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    student_name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    comment = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='testimonials')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reseña de {self.student_name}"


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=1, help_text="Orden de la lección en el curso")
    video_url = models.URLField(blank=True, null=True, help_text="Enlace de YouTube o Vimeo")
    content = models.TextField(blank=True, help_text="Explicación, ejercicios o código de la lección")
    is_free_preview = models.BooleanField(default=False, help_text="¿Es una vista previa gratuita?")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.order}. {self.title}"