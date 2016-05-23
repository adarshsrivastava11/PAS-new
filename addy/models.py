from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime 
from django.utils import timezone
from django import forms
from django.forms import ModelForm
#from datetime import date


# Different programs available for departments
class Program(models.Model):
	program_name = models.CharField(max_length = 200)
	def __str__(self):
		return self.program_name



class Department(models.Model):
	deptt_name = models.CharField(max_length = 200)
	def __str__(self):
		return self.deptt_name



# All the required fields commmon to all the students are declared below.
# An one-to-one relationship has been established between django default user and students model.
# A foreign key of Program and Department model has been made to avoid unnecessary searches.


class Student (models.Model):
	MALE = 'Male'
	FEMALE = 'Female'
	GENDER_CHOICES = ((MALE,'Male'),(FEMALE,'Female'),)
	GENERAL = 'GN'
	SC = 'SC'
	ST = 'ST'
	OTHERS = 'OTHERS'
	CATEGORY_CHOICES = ((GENERAL,'General'),(SC,'SC'),(ST,'ST'),(OTHERS,'Other'),)
	user = models.OneToOneField(User)
	program = models.ForeignKey(Program, on_delete = models.CASCADE)
	department = models.ForeignKey(Department, on_delete = models.CASCADE)
	roll_number = models.IntegerField()
	spo_registration_number = models.IntegerField(default = 0)
	full_name=models.CharField(max_length=200)
	father_name=models.CharField(max_length=200)
	gender=models.CharField(max_length = 50, choices = GENDER_CHOICES)
	dob = models.DateField()
	category = models.CharField(max_length = 50, choices = CATEGORY_CHOICES, default = GENERAL)
	local_address = models.CharField(max_length=1000)
	permanent_address = models.CharField(max_length=1000)
	mobile_number = models.IntegerField(default=0)
	friend_mobile_number = models.IntegerField(default = 0)
	phone_number = models.IntegerField(default = 0)
	emergency_number1 = models.IntegerField(default = 0)
	emergency_number2 = models.IntegerField(default = 0)
	emergency_name1 = models.CharField(max_length = 200)
	emergency_name2 = models.CharField(max_length = 200)
	email_iitk = models.EmailField(max_length = 200)
	entrance_rank = models.IntegerField(default = 0)
	cpi = models.DecimalField(max_digits = 5, decimal_places = 3)
	expected_graduation_date = models.DateField()
	marks_10 = models.FloatField()
	year_10 = models.IntegerField()
	board_10 = models.CharField(max_length = 200)
	marks_12 = models.FloatField()
	year_12 = models.IntegerField()
	board_12 = models.CharField(max_length = 200)	
	def __str__(self):
		return self.full_name


class StudentForm(ModelForm):
	class Meta:
		model = Student
		exclude = ['user']
		widgets = {
		'email_iitk': forms.TextInput(attrs = {'disabled':'yes'}),
		'roll_number' : forms.TextInput(attrs = {'disabled' : ''}),
		}


class Dual_Datas(models.Model):
	student = models.OneToOneField(Student)
	internship = models.CharField(max_length = 200)
	place_of_internship = models.CharField(max_length = 200)
	ppo = models.CharField(max_length = 200)
	spo_internship = models.CharField(max_length = 200)
	ug_cpi = models.DecimalField(max_digits = 5, decimal_places = 3)
	pg_cpi = models.DecimalField(max_digits = 5, decimal_places = 3)



class Pg_Datas(models.Model):
	student = models.OneToOneField(Student)
	ug_college = models.CharField(max_length = 200)
	funding_institute = models.CharField(max_length = 200)
	sponsored = models.CharField(max_length = 200)
	work_experience = models.CharField(max_length = 200)
	ug_marks = models.DecimalField(max_digits = 5, decimal_places = 3)
	ug_marks_scale = models.IntegerField()
	name_of_degree = models.CharField(max_length = 200)
	year_of_ug = models.IntegerField()
	specialisation = models.CharField(max_length = 200)



class Phd_Datas(models.Model):
	student = models.OneToOneField(Student)
	pg_marks = models.DecimalField(max_digits = 5, decimal_places = 3)
	pg_marks_scale = models.IntegerField()
	name_of_pg_degree = models.CharField(max_length = 200)
	sponsored = models.CharField(max_length = 200)
	funding_institute = models.CharField(max_length = 200)
	phd_thesis = models.CharField(max_length = 200)
	work_experience = models.CharField(max_length = 200)
	pg_university = models.CharField(max_length = 200)
	pg_thesis = models.CharField(max_length = 200)
	pg_super1_name = models.CharField(max_length = 200)
	pg_super1_name = models.EmailField(max_length = 200)
	pg_super2_name = models.CharField(max_length = 200)
	pg_super2_name = models.EmailField(max_length = 200)
	pg_specialisation = models.CharField(max_length = 200)
	year_of_pg = models.IntegerField()
	ug_marks = models.DecimalField(max_digits = 5, decimal_places = 3)
	ug_marks_scale = models.IntegerField()
	ug_college = models.CharField(max_length = 200)
	name_of_ug_degree = models.CharField(max_length = 200)
	ug_specialisation = models.CharField(max_length = 200)
	year_of_ug = models.IntegerField()



class Ug_Datas(models.Model):
	student = models.OneToOneField(Student)
	internship = models.CharField(max_length = 200)
	place_of_internship = models.CharField(max_length = 200)
	ppo = models.CharField(max_length = 200)
	spo_internship = models.CharField(max_length = 200)



class Companies(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length = 200)
	email = models.CharField(max_length = 200)
	day = models.IntegerField(default  = 0)
	def __str__(self):
		return self.name


class Job_Openings(models.Model):
	company = models.ForeignKey(Companies, on_delete = models.CASCADE)
	nature = models.CharField(max_length = 200)
	designation = models.CharField(max_length = 200)
	description = models.TextField()
	internship = models.BooleanField()
	package_btech = models.CharField(max_length = 200)
	package_mtech = models.CharField(max_length = 200)
	package_dual  = models.CharField(max_length = 200)
	package_msci = models.CharField(max_length = 200)
	package_msc2 = models.CharField(max_length = 200)
	package_mba = models.CharField(max_length = 200)
	package_mdes = models.CharField(max_length = 200)
	package_phd = models.CharField(max_length = 200)
	package_details = models.CharField(max_length = 200)
	bond = models.BooleanField()
	bond_details = models.CharField(max_length = 200)
	medical_requirments = models.CharField(max_length = 200)
	resume_shortlist = models.BooleanField()
	resume_criteria = models.CharField(max_length = 200)
	aptitude = models.BooleanField()
	group_discussion = models.BooleanField()
	tech_test = models.BooleanField()
	tech_interview = models.BooleanField()
	hr_interview = models.BooleanField()
	number_of_rounds = models.IntegerField(default = 0)
	contact_details1 = models.CharField(max_length = 1024)
	contact_details2 = models.CharField(max_length = 1024)
	contact_details3 = models.CharField(max_length = 1024)
	application_deadline = models.DateField()
	eligiblity = models.CharField(max_length = 1024)
	name = models.CharField(max_length = 200)
	published = models.BooleanField()
	deadline = models.DateField()
	ctc_btech = models.CharField(max_length = 200)
	ctc_mtech = models.CharField(max_length = 200)
	ctc_dual = models.CharField(max_length = 200)
	ctc_msci = models.CharField(max_length = 200)
	ctc_msc2 = models.CharField(max_length = 200)
	ctc_mba = models.CharField(max_length = 200)
	ctc_mdes = models.CharField(max_length = 200)
	ctc_phd = models.CharField(max_length = 200)
	aptitude_duration = models.CharField(max_length = 200)
	tech_test_duration = models.CharField(max_length = 200)
	gd_duration = models.CharField(max_length = 200)
	gd_strength = models.CharField(max_length = 200)
	tech_interview_duration = models.CharField(max_length = 200)
	hr_interview_duration = models.CharField(max_length = 200)
	def __str__(self):
		return self.name

class JobOpeningsForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(JobOpeningsForm, self).__init__(*args, **kwargs)
		for field in self: 
			field.field.widget.attrs['class'] = 'form-control'
	class Meta:
		model = Job_Openings
		fields = '__all__'

	

		

class Job_Application(models.Model):
	job_opening = models.ForeignKey(Job_Openings, on_delete = models.CASCADE)
	student = models.ForeignKey(Student, on_delete = models.CASCADE)
	status = models.IntegerField(default = 0)


class News(models.Model):

	company_name = models.CharField(max_length=200)
	news = models.CharField(max_length=800)
	author = models.CharField(max_length=200)
	
	time_date = models.DateTimeField('Date Published')

	def __str__(self):
		return self.company_name

class Temp_Student(models.Model):
	user = models.OneToOneField(User,on_delete = models.CASCADE)
	#Password is stored as the Student Name because Mail Port is not working
	student_name = models.CharField(max_length=200)
	student_roll = models.IntegerField(default=0)
	student_username = models.CharField(max_length=200)
	student_isAccepted = models.IntegerField(default=0)
	def __str__(self):
		return self.student_username

class CompanyApplication(models.Model):
	companyname = models.CharField(max_length = 200)
	contactperson = models.CharField(max_length = 200)
	designation = models.CharField(max_length = 200)
	email = models.CharField(max_length = 200)
	phone = models.IntegerField()
	def __str__(self):
		return self.companyname

class CompanyApplicationForm(ModelForm):
	class Meta:
		model = CompanyApplication
		fields = '__all__'
		widgets = {
		'companyname': forms.TextInput(attrs = {'class':'input-block','placeholder':'Enter full name of organization'}),
		'contactperson' : forms.TextInput(attrs = {'class':'input-block','placeholder':'Contact Person'}),
		'designation' : forms.TextInput(attrs = {'class':'input-block','placeholder':'Designation'}),
		'email' : forms.EmailInput(attrs = {'class':'input-block','placeholder':'E-mail ID'}),
		'phone' : forms.TextInput(attrs = {'class':'input-block','placeholder':'Phone number'}),
		}
	