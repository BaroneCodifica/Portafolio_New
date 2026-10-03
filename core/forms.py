from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'image', 'tech_stack', 'repo_url', 'live_url']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-lg p-2.5 focus:border-cyan-500 focus:outline-none'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-lg p-2.5 focus:border-cyan-500 focus:outline-none',
                'rows': 3
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-cyan-950 file:text-cyan-400 hover:file:bg-cyan-900'
            }),
            'tech_stack': forms.TextInput(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-lg p-2.5 focus:border-cyan-500 focus:outline-none',
                'placeholder': 'Python, Django, Tailwind'
            }),
            'repo_url': forms.URLInput(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-lg p-2.5 focus:border-cyan-500 focus:outline-none'
            }),
            'live_url': forms.URLInput(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-lg p-2.5 focus:border-cyan-500 focus:outline-none'
            }),
        }