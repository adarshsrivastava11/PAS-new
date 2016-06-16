from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth import authenticate,login
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required,user_passes_test
from django.core.mail import send_mail
import time
from datetime import datetime 
from django.utils import timezone 
import re
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt


def student_check(user):
  return Student.objects.filter(user = user).exists()

def company_check(user):
  return Companies.objects.filter(user = user).exists()

def poweruser_check(user):
  return Poweruser.objects.filter(user = user).exists()


def main_page(request):
  return render(request,'index.html')



def login_page(request):
  error = ''
  if request.user.is_authenticated():
    if request.GET.__contains__('next'):
      m = re.search('^/(?P<username>[a-zA-Z_]+)',request.GET.__getitem__('next'))
      return redirect(m.group(0) + '/dashboard/')
  if request.method == 'POST':
    form = Login(request.POST)

    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      user = authenticate(username = username,password = password)

      if user is not None:
        if user.is_active:
          login(request, user)
          
          if Temp_Student.objects.filter(user = request.user,student_isAccepted=True).exists():
            return redirect('/' + username + '/fillform/')

          elif Student.objects.filter(user = request.user).exists():
            return redirect('/' + username + '/dashboard/')

          elif Companies.objects.filter(user = request.user).exists():
            return redirect('/' + username + '/homepage/')

          elif Poweruser.objects.filter(user = request.user).exists():
            return redirect('/' + username + '/panel/')
            # /SPO/ used 


        else:
          error = 'Your account is not yet made active by SPO'

      else:
        error = 'Invalid credentials. Please try again'

  else:
    form = Login()

  return render(request, 'login.html', {'form': form,'error':error}) 



def logout_view(request):
  logout(request)
  return redirect('/login/') 



def signup(request):
  error = ''
  if request.method == 'POST':
    form = Signup(request.POST)

    if form.is_valid():
      # username here is CC Username
      firstname = form.cleaned_data['firstname']
      lastname = form.cleaned_data['lastname']
      student_name=firstname+" "+lastname
      username = form.cleaned_data['username_signup']
      roll_number = form.cleaned_data['roll_number']
      password = User.objects.make_random_password()

      if User.objects.filter(username=username).exists():
        error = 'Username already exists'
      else:
        email_usr = username+'@iitk.ac.in'
        user = User.objects.create_user(username = username, password = password,email=email_usr,is_active = True)
        user.save()
        send_mail('Your Pas Password', password , 'pasiitk16@gmail.com',[username+'@iitk.ac.in'], fail_silently=True)
        model = Temp_Student(user = user,student_name = student_name,student_roll = roll_number,student_username = username)
        model.save()
        return redirect('/signup_success/')           
  else:
    form = Signup()

  return render(request, 'signup.html', {'form': form,'error':error})

def signup_success(request):
  return render(request, 'post_signup.html')



def company_signup(request):
  error = ""
  if request.method == 'POST':        
    form = CompanyApplicationForm(request.POST)

    if form.is_valid():
      form.save()
      form = CompanyApplicationForm()
      error = "You have been signed up. Wait for SPO to contact you."
    else:
      error = "Form data problem"
  else:
    form = CompanyApplicationForm()

  return render(request, 'company_signup.html', {'form': form,'error':error})



@login_required(login_url = '/login/')
def dashboard(request,user_name):
  
  template = get_template('dashboard.html')
  
  if user_name != request.user.username:
    return redirect('/login/')
  else:

    if Temp_Student.objects.filter(user = request.user).exists():
      return redirect('/' + user_name + '/fillform/')

    elif Student.objects.filter(user = request.user).exists():
      student = Student.objects.get(user = request.user)
      username = request.user.username
      email_user= request.user.email
      lastlogin = request.user.last_login
      name = student.full_name
      if News.objects.filter().exists():
        allnews = News.objects.all().order_by('-time_date')
        update_time = timezone.now()-News.objects.latest('time_date').time_date     
      else:
        allnews = News.objects.none()
        update_time = timezone.now() - timezone.now()
      variables = Context({
        'name_user':name,
        'lastlogin':lastlogin,
        'user_name':username,
        'email_user':email_user,
        'allnews':allnews,
        'update_time':update_time,
        'user_name':user_name,
        })
      output = template.render(variables)
      return HttpResponse(output)
    elif Companies.objects.filter(user = request.user).exists():
      return redirect('/' + user_name + '/homepage/')

@login_required(login_url = '/login/')
@user_passes_test(student_check,login_url = '/login/')
def student_profile(request,username):
  if username != request.user.username:
    return redirect('/login/')
  else:
    student = Student.objects.get(user = request.user)
    if request.method == 'POST':
      form = StudentForm(request.POST,instance = student)
      if form.is_valid:
        form.save()
      else:
        error = form.errors
    else:
      form = StudentForm(instance = student)
    return render(request,'profile.html',{'form':form,'username':username})


@login_required(login_url = '/login/')
@user_passes_test(student_check,login_url = '/login/')
def student_data(request,username):
  error = ''
  if username != request.user.username:
    return redirect('/login/')
  else:
    student = Student.objects.get(user = request.user)
    if request.method == 'POST':
      if student.program.value == 1:
        inst = Ug_Datas(student = student)
        form = UgDatasForm(request.POST,instance = inst)
      elif student.program.value == 2:
        inst = Pg_Datas(student = student)
        form = PgDatasForm(request.POST,instance = inst)
      elif student.program.value == 3:
        inst = Dual_Datas(student = student)
        form = DualDatasForm(request.POST,instance = inst)
      elif student.program.value == 4:
        inst = PhdDatasForm(student = student)
        form = PhdDatasForm(request.POST,instance = inst)

      if form.is_valid():
        form.save()
      else:
        error = 'Form not valid'
    else:
      if student.program.value == 1:
        if Ug_Datas.objects.filter(student = student).exists():
          inst = Ug_Datas.objects.get(student = student)
        else:
          inst = Ug_Datas(student = student)
        form = UgDatasForm(instance = inst)
      elif student.program.value == 2:
        if Pg_Datas.objects.filter(student = student).exists():
          inst = Pg_Datas.objects.get(student = student)
        else:
          inst = Pg_Datas(student = student)
        form = PgDatasForm(instance = inst)
      elif student.program.value == 3:
        if Dual_Datas.objects.filter(student = student).exists():
          inst = Dual_Datas.objects.get(student = student)
        else:
          inst = Dual_Datas(student = student)
        form = DualDatasForm(instance = inst)
      elif student.program.value == 4:
        if Phd_Datas.objects.filter(student = student).exists():
          inst = Phd_Datas.objects.get(student = student)
        else:
          inst = Phd_Datas(student = student)
        form = PhdDatasForm(instance = inst)
    return render(request,'data.html',{'form':form,'username':username,'error':error})


@login_required(login_url = '/login/')
@user_passes_test(student_check,login_url = '/login/')
def job_application(request,username):
  if username != request.user.username:
    redirect('/login/')
  else:
    student = Student.objects.get(user = request.user)
    job_list = Job_Openings.objects.filter(eligible_departments  = student.department).order_by('-application_deadline')
    return render(request,'job_applications.html',{'job_list':job_list,'username':username})



@login_required(login_url = '/login/')
@user_passes_test(company_check,login_url = '/login/')
def homepage(request,username):
  if username != request.user.username:
    return redirect('/login/')
  else:
    company = Companies.objects.get(user = request.user)
    email_user = company.email
    name = company.name
    lastlogin = request.user.last_login
    if Job_Openings.objects.filter(company = company).exists():
      job_list = Job_Openings.objects.filter(company = company)
    else:
      job_list = Job_Openings.objects.none()
    return render(request,'homepage.html',{
      'name_user':name,
      'lastlogin':lastlogin,
      'username':username,
      'email_user':email_user,
      'job_list':job_list,
      })



@login_required(login_url = '/login/')
@user_passes_test(company_check,login_url = '/login/')
def job_opening(request,username):
  if username != request.user.username:
    return redirect('/login/')
  else:
    company = Companies.objects.get(user = request.user)
    job = Job_Openings(company = company)
    if request.method == 'POST':
      
      form = JobOpeningsForm(request.POST,instance = job)
      if form.is_valid():
        form.save()
        return redirect('/' + username + '/homepage/' )
      else:
        error = "Form data problem"
    else:
      form = JobOpeningsForm(instance = job)
      return render(request,'job_opening.html',{'form':form,'username':username})


@login_required(login_url = '/login/')
def changepassword(request,user_name):
  if user_name != request.user.username:
    redirect('/login/')
  username = user_name
  error=''
  user = User.objects.get(username=username)

  if request.method == 'POST':
    form = ChangePassword(request.POST)
    if form.is_valid():
      oldpass = form.cleaned_data['oldpass']
      newpass = form.cleaned_data['newpass']
      if user.check_password(oldpass):
        user.set_password(newpass)
        user.save()
        return redirect('/login')
      else:
        error = 'Wrong old password entered!'
  else:
      form = ChangePassword()

  return render(request, 'password.html', {'form': form,'username':username,'error':error})

@login_required(login_url = '/login/')
def fillform(request,user_name):
    username = request.user.username
    if username!=user_name:
      return redirect('/')  
    else:
      if not Temp_Student.objects.filter(user = request.user).exists():
        return redirect('/' + username + '/dashboard/')
      temp = Temp_Student.objects.get(user = request.user)
      student = Student(user = temp.user,roll_number = temp.student_roll, email_iitk = request.user.email)
      if request.method == 'POST':
        form = StudentForm(request.POST, instance = student)
        if form.is_valid():
          form.save()
          temp.delete()
      else:
          form = StudentForm(instance = student)

      return render(request, 'register.html', {'form': form,'username': username})


#def poweruser(request): 
# data = request.POST.get('choice',False)
# query_res = Temp_Student.objects.filter(user__is_active = False)
# data_int  = int(data)
# if data_int != 0:
#  stu  = User.objects.get(id=data_int)


#  stu.is_active = True
#  stu.save()
##return render(request, 'power_user.html', {'query_res':query_res})


@login_required(login_url = '/login/')
def resume_manage(request,user_name):
  template = get_template('resumes.html')
  username = request.user.username
  if user_name!=username:
    return redirect('/')
  variables = Context({
    'master_status': 'No Resume Uploaded yet', 
    'resumes_status':'No Resume yet'    
  })
  output = template.render(variables)
  return HttpResponse(output)


@user_passes_test(poweruser_check,login_url = '/login/')
#@permission_required('addy.view_Student')
#@permission_required('addy.edit_Student')
@csrf_exempt
@login_required(login_url = '/login/')
def panel(request,username):
  
  template = get_template('panel.html')
  
  if username != request.user.username:
    return redirect('/login/')
  else:

    if Poweruser.objects.filter(user = request.user).exists():
      poweruser = Poweruser.objects.get(user = request.user)
      #username = request.user.username
      email_user= request.user.email
      lastlogin = request.user.last_login
      
      

      # if News.objects.filter().exists():
       # allnews = News.objects.all().order_by('-time_date')
        #update_time = timezone.now()-News.objects.latest('time_date').time_date     
      
      #else:
       # allnews = News.objects.none()
        #update_time = timezone.now() - timezone.now()
      

      #if Companies.objects.filter().exists():
       # allcompanies = Companies.objects.all().order_by('-name')
      #else:
       # allcompanies = Companies.objects.none()
###
      variables = {
        
        'lastlogin':lastlogin,
        'username':username,
        'email_user':email_user,
      #  'allnews':allnews,
       # 'update_time':update_time,
        #'allcompanies':allcompanies,
        }
      
     
    return render(request, 'panel.html', variables)
    #return HttpResponse(output)
    #elif Companies.objects.filter(user = request.user).exists():
    #  return redirect('/' + user_name + '/homepage/')

#@permission_required('addy.view_Student')
#@permission_required('addy.edit_Student')
@user_passes_test(poweruser_check,login_url = '/login/')
@login_required(login_url = '/login/')
@csrf_exempt
def activate_temp_student(request,username):
  error=""
  if username != request.user.username:
    return redirect('/login/')
  else:

    if Poweruser.objects.filter(user = request.user).exists():
      poweruser = Poweruser.objects.get(user = request.user)
      email_user= request.user.email
      lastlogin = request.user.last_login
      
      if Temp_Student.objects.filter(student_isAccepted = False).exists():
        users=Temp_Student.objects.filter(student_isAccepted=False)
        data = request.POST.get('choice',False)
        data_int  = int(data)
        if data_int != 0:
          temp  = Temp_Student.objects.get(id=data_int)
          temp.student_isAccepted = True
          temp.save()
          return redirect('/'+ username + '/panel/activate_temp_student')
      else:
        users = Temp_Student.objects.none()
        error="All temp student accepted :)" 

  variables = {
    
  'username':username,
  'email_user':email_user,
  'users':users,
  'error':error,
  }
  return render(request, 'activate_temp_student.html', variables)
  
@user_passes_test(poweruser_check,login_url = '/login/')
#@permission_required('addy.view_Student')
#@permission_required('addy.edit_Student')
@login_required(login_url = '/login/')
@csrf_exempt
def deactivate_temp_student(request,username):
  
  error=""
  if username != request.user.username:
    return redirect('/login/')
  else:

    if Poweruser.objects.filter(user = request.user).exists():
      poweruser = Poweruser.objects.get(user = request.user)
      email_user= request.user.email
      lastlogin = request.user.last_login
      
      if Temp_Student.objects.filter(student_isAccepted = True).exists():
        users=Temp_Student.objects.filter(student_isAccepted=True)
        data = request.POST.get('choice',False)
        data_int  = int(data)
        if data_int != 0:
          temp  = Temp_Student.objects.get(id=data_int)
          temp.student_isAccepted = False
          temp.save()
          return redirect('/'+ username + '/panel/deactivate_temp_student')
      else:
        users = Temp_Student.objects.none()
        error="All temp student rejected :(" 

      
  variables = {
    
  'username':username,
  'email_user':email_user,
  'users':users,
  'error':error,
  }
  return render(request, 'deactivate_temp_student.html', variables)
  

@user_passes_test(poweruser_check,login_url = '/login/')
#@permission_required('addy.view_Student')
#@permission_required('addy.edit_Student')
@csrf_exempt
@login_required(login_url = '/login/')
def add_news(request,username):
  
  error=""
  if username != request.user.username:
    return redirect('/login/')
  else:

    if request.method == 'POST':
      form = NewsForm(request.POST)
      if form.is_valid():
        news = form.save(commit=False)
        news.time_date=timezone.now()
        news.save()
        #news = News(time_date = timezone.now())
      
        return redirect('/'+ username + '/panel/add_news')
      else:
          error = form.errors
    else:
      form = NewsForm()

  allnews = News.objects.all().order_by('-time_date')
  return render(request,'add_news.html',{'username':username,'form':form,'allnews':allnews})


@login_required(login_url = '/login/')
@user_passes_test(poweruser_check,login_url = '/login/')
#@permission_required('addy.view_News')
#@permission_required('addy.edit_News')
#@permission_required('addy.delete_News')
def deletenews(request,username):
  
  if username != request.user.username:
    return redirect('/login/')
  else:

    if Poweruser.objects.filter(user = request.user).exists():
      poweruser = Poweruser.objects.get(user = request.user)
      email_user= request.user.email
      lastlogin = request.user.last_login
      
      if News.objects.filter().exists():
        users=News.objects.filter()
        data = request.POST.get('choice',False)
        data_int  = int(data)
        if data_int != 0:
          temp  = Temp_Student.objects.get(id=data_int)
          temp.student_isAccepted = False
          temp.save()
          return redirect('/'+ username + '/panel/deactivate_temp_student')
      else:
        users = Temp_Student.objects.none()
        error="All temp student rejected :(" 
  
      variables = {
        
        'user_name':username,
        'email_user':email_user,
        'allnews':allnews,
        }
     
@login_required(login_url = '/login/')
@user_passes_test(poweruser_check,login_url = '/login/')
@permission_required('addy.view_Job_Openings')
@permission_required('addy.edit_Job_Openings')
def approve_job_notice(request,user_name):
  
  template = get_template('approve_job_notice.html')
  
  if user_name != request.user.username:
    return redirect('/login/')
  else:

    if Poweruser.objects.filter(user = request.user).exists():
      poweruser1 = Poweruser.objects.get(user = request.user)
      username = request.user.username
      email_user= request.user.email
      
      alljobs=Job_Openings.objects.filter(published=False).order_by('-pub_date')


      
      variables = Context({
        
        'user_name':username,
        'email_user':email_user,
        'alljobs':alljobs,
        })
      output = template.render(variables)
      return HttpResponse(output)
    #elif Companies.objects.filter(user = request.user).exists():
    #  return redirect('/' + user_name + '/homepage/')

@login_required(login_url = '/login/')
@user_passes_test(poweruser_check,login_url = '/login/')
@permission_required('addy.view_Job_Openings')
@permission_required('addy.edit_Job_Openings')
def reject_job_notice(request,user_name):
  
  template = get_template('reject_job_notice.html')
  
  if user_name != request.user.username:
    return redirect('/login/')
  else:

    if Poweruser.objects.filter(user = request.user).exists():
      poweruser1 = Poweruser.objects.get(user = request.user)
      username = request.user.username
      email_user= request.user.email
      
      alljobs=Job_Openings.objects.filter(published=True).order_by('-company.name')


      
      variables = Context({
        
        'user_name':username,
        'email_user':email_user,
        'alljobs':alljobs,
        })
      output = template.render(variables)
      return HttpResponse(output)
    #elif Companies.objects.filter(user = request.user).exists():
    #  return redirect('/' + user_name + '/homepage/')


def generate_xls(request):
  workbook = xlsxwriter.Workbook('addy/Job.xlsx')
  worksheet = workbook.add_worksheet()
  bold = workbook.add_format({'bold': 1})
  row=1
  col=0
  worksheet.set_column(row, col, 15)
  worksheet.write('A1', 'Student Name', bold)
  jobs_applications = Job_Application.objects.all()
  application_list = list(jobs_applications)
  for jobs in application_list:
    worksheet.write(row, 0,str(jobs.student))
    row = row+1
    

######################## POWER USER THINGS LEFT
# Temp User
# Company Add/Delete/Edit
# Student Add/Delete/Edit
# News Add
# View Job Application
