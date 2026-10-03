from django.shortcuts import render, get_object_or_404
from .models import Course, Category, Testimonial

def academy_home(request):
    featured_courses = Course.objects.filter(is_published=True)[:6]
    categories = Category.objects.all()
    testimonials = Testimonial.objects.all().order_by('-created_at')[:5]
    
    context = {
        'featured_courses': featured_courses,
        'categories': categories,
        'testimonials': testimonials,
    }
    return render(request, 'courses/academy_home.html', context)

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    return render(request, 'courses/course_detail.html', {'course': course})