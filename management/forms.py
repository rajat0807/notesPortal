from django import forms
from django.forms import widgets
from django.forms import ModelForm
from django.contrib.auth.models import User
from management.models import UserProfile,noteDetail,noteFile,Image
from django.contrib import admin

class UserForm( forms.ModelForm ):
	password=forms.CharField(widget=forms.PasswordInput())
	confirm_password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model= User
		fields = ('username', 'email', 'password','confirm_password')
	

admin.site.unregister( User )
admin.site.register( User)

class UserProfileForm(ModelForm):
	"""form for extended auth User model"""
	class Meta:
		model = UserProfile
		fields = ('department','year')

class UserForm2(forms.ModelForm):

	class Meta:
		model = User
		fields = ('username',)

class UserPhotoUpdateForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ('picture',)

class AddCourseForm(ModelForm):
	class Meta: 
		model = noteDetail
		fields = ('branch','year')

class AddSubjectForm(ModelForm):
	class Meta:
		model = noteFile
		fields = ('notes','subjectName')


class FileFieldForm(forms.Form):
	images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
	class Meta:
		model = Image
		fields = ('image',)