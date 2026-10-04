from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'subtitle', 'description', 'category', 'course_type', 'price', 'is_published', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-cyan-500'}),
            'subtitle': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-cyan-500'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-cyan-500'}),
            'category': forms.Select(attrs={'class': 'w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-cyan-500'}),
            'course_type': forms.Select(attrs={'class': 'w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-cyan-500'}),
            'price': forms.NumberInput(attrs={'class': 'w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-cyan-500'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'rounded bg-slate-900 border-slate-700 text-cyan-500 focus:ring-0'}),
            'cover_image': forms.FileInput(attrs={'class': 'w-full text-xs text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-slate-700 file:text-white hover:file:bg-slate-600'}),
        }