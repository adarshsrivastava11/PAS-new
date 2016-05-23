from django import forms
from datetime import date

class Student1(forms.Form):

	roll_number=forms.CharField(label='Roll No.',max_length=200)
	full_name=forms.CharField(label='Full Name.' , max_length=200)
	gender=forms.IntegerField(label='Gender')
	#dob = forms.DateField(_("Date"), default=date.today)
	local_address=forms.CharField(label='Local Address',max_length=200)
	permanent_address=forms.CharField(label='Permanent Address',max_length=200)
	mobile_number=forms.CharField(label='Mobile Number',max_length=200)
	phone_number = forms.CharField(label='Phone Number',max_length=200)
	emergency_number1=forms.CharField(label='Emergency Number 1',max_length=200)
	emergency_number2=forms.CharField(label='Emergency Number 2',max_length=200)
	emergency_name1 = forms.CharField(label='Emergency Name 1',max_length=200)
	emergency_name2 = forms.CharField(label='Emergency Name 2',max_length=200)
	email_iitk=forms.EmailField(max_length=200)
	email_other=forms.EmailField(max_length=200)
	jee_rank =  forms.CharField(max_length=200)

class Login(forms.Form):

	username=forms.CharField(label='User Name',max_length=200,widget = forms.TextInput(attrs = {'class':'input-block','placeholder':'Username'}))
	
	#password=forms.CharField(label='Password' , max_length=200)
	password = forms.CharField(widget=forms.TextInput(attrs={'type': 'password','class':'input-block','placeholder':'Password'}))

class Signup(forms.Form):
	 firstname=forms.CharField(label='First Name',max_length=200,widget = forms.TextInput(attrs = {'class':'input-block','placeholder':'First name'}))
	 lastname=forms.CharField(label='Last Name',max_length=200,widget = forms.TextInput(attrs = {'class':'input-block','placeholder':'Last name'}))
	 username_signup=forms.CharField(label='CC-Username',max_length=200,widget = forms.TextInput(attrs = {'class':'input-block','placeholder':'Username'}))
	 roll_number=forms.CharField(label='Roll Number',max_length=200,widget = forms.TextInput(attrs = {'class':'input-block','placeholder':'Roll Number'}))
	 

class ChangePassword(forms.Form):
	oldpass = forms.CharField(label='Old Password:',max_length=20,widget=forms.TextInput(attrs={'type': 'password','class':'form-control','placeholder':'Old password'}))
	newpass = forms.CharField(label='New Password:',max_length=20,widget=forms.TextInput(attrs={'type': 'password','class':'form-control','placeholder':'New password'}))

class Poweruser(forms.Form):
	test = forms.CharField(widget=forms.TextInput(attrs={'type':'submit','value':'4'}))