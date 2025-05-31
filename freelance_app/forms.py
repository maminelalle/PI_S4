from django import forms
from .models import JobOffer, Application, Message, Resource, Review, Comment
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.contrib.auth import get_user_model


# class LoginForm(AuthenticationForm):
#     username = forms.EmailField(label="Email")

# class RegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES)

#     class Meta:
#         model = User
#         fields = [
#             'username', 'email', 'password', 'profile_photo', 'user_type',
#             'skills', 'experience', 'portfolio_url', 'cv_file', 'location',
#             'company_name', 'description', 'website'
#         ]

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])
#         if commit:
#             user.save()
#         return user
    

User = get_user_model()

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'profile_photo', 'user_type',
            'skills', 'experience', 'portfolio_url', 'cv_file', 'location',
            'company_name', 'description', 'website'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class JobOfferForm(forms.ModelForm):
    class Meta:
        model = JobOffer
        fields = ['title', 'description', 'category', 'location', 'budget', 'is_remote', 'deadline']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'content', 'file']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
