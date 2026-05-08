from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import JobPost, Application, ApplicantProfile


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = [
            'title', 'company_name', 'job_type', 'location', 'salary_range',
            'description', 'qualifications', 'requirements', 'deadline', 'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Enter job title'
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Company name'
            }),
            'job_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Job location'
            }),
            'salary_range': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'e.g., $50,000 - $70,000'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 5,
                'placeholder': 'Job description'
            }),
            'qualifications': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 4,
                'placeholder': 'Required qualifications'
            }),
            'requirements': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 4,
                'placeholder': 'Job requirements'
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'type': 'date'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['full_name', 'email', 'phone', 'address', 'cover_letter', 'resume']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'your@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Phone number'
            }),
            'address': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Your address'
            }),
            'cover_letter': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'rows': 5,
                'placeholder': 'Write your cover letter here...',
                'x-model': 'coverLetter'
            }),
            'resume': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg',
                'accept': '.pdf,.doc,.docx'
            }),
        }
class ApplicantRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'your@email.com'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'First name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Last name'
        })
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Choose a username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Confirm password'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class ApplicantLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Username',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Password',
            'autocomplete': 'current-password'
        })
    )


class ApplicantProfileForm(forms.ModelForm):
    class Meta:
        model = ApplicantProfile
        fields = ['phone', 'address', 'resume']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Phone number'
            }),
            'address': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Your address'
            }),
            'resume': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg',
                'accept': '.pdf,.doc,.docx'
            }),
        }
