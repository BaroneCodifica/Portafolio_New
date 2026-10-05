from django import forms
from .models import Project


class ContactForm(forms.Form):
    name = forms.CharField(
        label="Tu nombre",
        max_length=100,
        widget=forms.TextInput(attrs={
            'autocomplete': 'name',
            'placeholder': '¿Cómo te llamas?',
        }),
    )
    email = forms.EmailField(
        label="Tu correo",
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'placeholder': 'tu@correo.com',
        }),
    )
    subject = forms.CharField(
        label="Asunto",
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': '¿En qué puedo ayudarte?',
        }),
    )
    message = forms.CharField(
        label="Mensaje",
        max_length=5000,
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Cuéntame un poco sobre tu idea o proyecto...',
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = (
                'mt-2 w-full rounded-xl border border-slate-700 bg-slate-950/70 '
                'px-4 py-3 text-sm text-white placeholder:text-slate-500 '
                'outline-none transition focus:border-cyan-400 focus:ring-2 '
                'focus:ring-cyan-400/20'
            )

    def clean_subject(self):
        subject = self.cleaned_data['subject']
        if '\r' in subject or '\n' in subject:
            raise forms.ValidationError("El asunto debe ocupar una sola línea.")
        return subject


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