# -*- coding: UTF-8 -*-
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm

class LoginForm(forms.Form):
	username = forms.CharField(label=u"Login", max_length=64, required=False)
	password = forms.CharField(label=u"Hasło", max_length=64, widget=forms.PasswordInput(), required=False)
	
	def clean(self):
		self.user = None
		cleaned_data = super(LoginForm, self).clean()
		clean_username = cleaned_data.get('username')
		clean_password = cleaned_data.get('password')
		if clean_username and clean_password:
			try:
				self.user = authenticate(username=clean_username, password=clean_password)
			except:
				pass
			if self.user is None:
				raise forms.ValidationError("Nieprawidłowe dane logowania!")
			elif not self.user.is_active:
				raise forms.ValidationError("Twoje konto nie zostało jeszcze aktywowane!")
		else: raise forms.ValidationError("Niekompletne dane logowania!")

class ChangePasswordForm(PasswordChangeForm):
	pass