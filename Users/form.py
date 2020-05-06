# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from .models import Profile
#
# class MyUserReg(UserCreationForm):
#     email: forms.EmailField(required=True)
#
#     class Meta:
#         model = User
#         fields=['username', 'password1', 'password2', 'email']
#
# class UserUpdateForm(forms.ModelForm):
#     email: forms.EmailField()
#
#     class Meta:
#         model = User
#         fields=['username', 'email']
#
# class ProfileImage(forms.ModelForm):
#     img: forms.ImageField()
#     def __init__(self, *args, **kwards):
#         super(ProfileImage, self).__init__(*args, **kwards)
#         self.fields['img'].label= "Изображение профиля"
#
#     class Meta:
#         model = Profile
#         fields=['img']
