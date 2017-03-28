from django import forms
from django.contrib.auth.models import User
from .models import *

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['question_text', 'question_title', 'is_anon']

	def clean_question(self):
		question_text = self.cleaned_data.get('question_text')
		return question_text
		
# Adding login functionality
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	
	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
		
	# def clean_email(self):
	# 	email = self.cleaned_data['email']
	# 	domain = email.split('@')[1]
	# 	domain_list = ["student.u-46.org", "aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com", "google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com", "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk", "email.com", "games.com", "gmx.net", "hush.com", "hushmail.com", "icloud.com", "inbox.com", "lavabit.com", "love.com", "outlook.com", "pobox.com", "rocketmail.com", "safe-mail.net", "wow.com", "ygm.com", "ymail.com", "zoho.com", "fastmail.fm", "bellsouth.net", "charter.net", "comcast.net", "cox.net", "earthlink.net", "juno.com", "btinternet.com", "virginmedia.com", "blueyonder.co.uk", "freeserve.co.uk", "live.co.uk", "ntlworld.com", "o2.co.uk", "orange.net", "sky.com", "talktalk.co.uk", "tiscali.co.uk", "virgin.net", "wanadoo.co.uk", "bt.com", "sina.com", "qq.com", "naver.com", "hanmail.net", "daum.net", "nate.com", "yahoo.co.jp", "yahoo.co.kr", "yahoo.co.id", "yahoo.co.in", "yahoo.com.sg", "yahoo.com.ph", "hotmail.fr", "live.fr", "laposte.net", "yahoo.fr", "wanadoo.fr", "orange.fr", "gmx.fr", "sfr.fr", "neuf.fr", "free.fr", "gmx.de", "hotmail.de", "live.de", "online.de", "t-online.de", "web.de", "yahoo.de", "mail.ru", "rambler.ru", "yandex.ru", "ya.ru", "list.ru", "hotmail.be", "live.be", "skynet.be", "voo.be", "tvcablenet.be", "telenet.be", "hotmail.com.ar", "live.com.ar", "yahoo.com.ar", "fibertel.com.ar", "speedy.com.ar", "arnet.com.ar", "hotmail.com", "gmail.com", "yahoo.com.mx", "live.com.mx", "yahoo.com", "hotmail.es", "live.com", "hotmail.com.mx", "prodigy.net.mx", "msn.com"]
	# 	if domain not in domain_list:
	# 		raise forms.ValidationError['Please enter a valid email address with a different domain']
	# 	return email
		
	class Meta:
		model = User
		fields = ['username', 'email', 'password']
		
class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = []

class ClassForm(forms.ModelForm):
	class Meta:
		model = UserDefinedClass
		fields = ['name', 'description', 'is_private']

	def clean_name(self):
		class_name = self.cleaned_data.get('name')
		return class_name

	def clean_description(self):
		description = self.cleaned_data.get('description')

		return description
		
class SchoolForm(forms.ModelForm):
	class Meta:
		model = School
		fields = ['state', 'school_name']
		
	def __init__(self, *args, **kwargs):
		super(SchoolForm, self).__init__(*args, **kwargs)
		self.fields['school_name'].required = False
		
	def is_valid(self):
		valid = super(SchoolForm, self).is_valid()
		if not valid:
			return valid
		