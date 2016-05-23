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
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import send_mail
import time
from datetime import datetime 
from django.utils import timezone 


def main_page(request):
  template = get_template('index.html')
  variables = Context({
    'message': 'Welcome to PAS',     
  })
  output = template.render(variables)
  return HttpResponse(output)
	


def login_page(request):
  error = ''
  if request.method == 'POST':        
   form = Login(request.POST)
   if form.is_valid():
     username = form.cleaned_data['username']
     password = form.cleaned_data['password']

     user = authenticate(username=username,password=password)

     if user is not None:
      if user.is_active:
        login(request, user)
        #current_status = Temp_Student.objects.get(student_username=username)
        #if current_status.student_isAccepted == 1:
        if Temp_Student.objects.filter(user = request.user).exists():
          return redirect('/' + username + '/fillform/')
        elif Student.objects.filter(user = request.user).exists():
          return redirect('/' + username + '/dashboard/')
        elif Companies.objects.filter(user = request.user).exists():
          return redirect('/' + username + '/homepage/')
        #else:
          #return redirect('/'+username+'/notconfirmed/')
      else:
         error = 'Your account is not yet made active by SPO'
     else:
      error = 'Invalid credentials. Please try again'
  else:
        form = Login()

  return render(request, 'login.html', {'form': form,'error':error})

def notconfirmed(request,user_name):
  template = get_template('waiting.html')
  variables = Context({
    'message': 'Your Account has not yet been confirmed by the SPO',     
  })
  output = template.render(variables)
  return HttpResponse(output)

  

def logout_view(request):
  logout(request)
  return redirect('/login/')  


 

def signup(request):
  if request.method == 'POST':        
        form = Signup(request.POST)
        if form.is_valid():
           # username here is CC Username
           username = form.cleaned_data['username_signup']
           roll_number = form.cleaned_data['roll_number']
           password = User.objects.make_random_password()
           if User.objects.filter(username=username).exists():
            return redirect('/signup_fail/')
           else:
            email_usr = username+'@iitk.ac.in'
            user = User.objects.create_user(username = username, password = password,email=email_usr,first_name=password,is_active = False)
            user.save()
            
            #send_mail('Your Pas Password', password , 'pasiitk16@gmail.com',
    #[username+'@iitk.ac.in'], fail_silently=True)
            #template = get_template('signup.html')
            #variables = Context({
            #'message': 'Welcome to PAS',     
            #})
            #output = template.render(variables)
            #response= HttpResponse(output)
            model = Temp_Student(user = user,student_name =password,student_roll=roll_number,student_username=username)
            model.save()
            return redirect('/signup_success/')

            
            
           
  else:
    form = Signup()

  return render(request, 'signup.html', {'form': form})

def signup_success(request):


  if request.method == 'POST':
        
         form = Login(request.POST)


         if form.is_valid():
           username = form.cleaned_data['username']
           password = form.cleaned_data['password']
           user = authenticate(username=username,password=password)
           if user is not None:

            if user.is_active:
              login(request, user)
              return redirect('/'+username+'/dashboard/')
            else:
               error = 'inactive'

           else:
            error = 'Invalid'
  else:
        form = Login()  # why are we sending this form? It is not being used in post_signup anywhere

  return render(request, 'post_signup.html', {'form': form})

def signup_fail(request):

  template = get_template('signup_fail.html')
  variables = Context({
    'message': 'The Username Already Exists', 
    
    
  })
  output = template.render(variables)
  return HttpResponse(output)

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


@login_required
def dashboard(request,user_name):
  
  template = get_template('dashboard.html')
  
  if user_name != request.user.username:
    return redirect('/login/')
  else:
    if Temp_Student.objects.filter(user = request.user).exists():
      return redirect('/' + user_name + '/fillform/')
    elif Student.objects.filter(user = request.user).exists(): 
      username = request.user.username
      email_user= request.user.email
      firstname = request.user.first_name
      lastname = request.user.last_name
      lastlogin = request.user.last_login
      name = firstname + ' ' + lastname
      allnews = News.objects.all().order_by('-time_date')
      update_time = timezone.now()-News.objects.latest('time_date').time_date     
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

@login_required
def homepage(request,username):
  if username != request.user.username:
    return redirect('/login/')
  else:
    if Temp_Student.objects.filter(user = request.user).exists():
      return redirect('/' + username + '/fillform/')
    elif Student.objects.filter(user = request.user).exists():
      return redirect('/' + username + '/dashboard/')
    elif Companies.objects.filter(user = request.user).exists():
      company = Companies.objects.filter(user = request.user)
      email_user = request.user.email
      name = Companies.objects.get(user = request.user).name
      lastlogin = request.user.last_login
      if Job_Openings.objects.filter(company = company).exists():
        job_list = Job_Openings.objects.filter(company = company)
      return render(request,'homepage.html',{
        'name_user':name,
        'lastlogin':lastlogin,
        'username':username,
        'email_user':email_user,
        'job_list':job_list,
        })

@login_required
def job_opening(request,username):
  if username != request.user.username:
    return redirect('/login/')
  else:
    if Companies.objects.filter(user = request.user).exists():
      if request.method == 'POST':
        form = JobOpeningsForm(request.POST)
        if form.is_valid():
          form.save()
          return redirect('/' + username + '/homepage/' )
        else:
          error = "Form data problem"
      else:
        job = Job_Openings(company = Companies.objects.get(user =  request.user))
        form = JobOpeningsForm(instance = job)
        return render(request,'job_opening.html',{'form':form,'username':username})
    else:
      return redirect('/' + username + '/dashboard/')
@login_required
def changepassword(request,user_name):
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

@login_required
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


def poweruser(request): 
 data = request.POST.get('choice',False)
 query_res = Temp_Student.objects.filter(user__is_active = False)
 data_int  = int(data)
 if data_int != 0:
  stu  = User.objects.get(id=data_int)

  stu.is_active = True
  stu.save()
 return render(request, 'power_user.html', {'query_res':query_res})

@login_required
@permission_required('addy.add_news')
@permission_required('addy.delete_news')
def manage_news(request):
  
  comapny_name=request.POST.get('company_name',False)
  data_news = request.POST.get('news_data',False)
  #news_author = request.POST.get('author',False)
  if comapny_name != False:
   
   new_news = News(company_name=comapny_name,news=data_news,time_date=timezone.now())
   new_news.save()
  deletenews=request.POST.get('removeNews',False)
  deletenews = int(deletenews)
  if deletenews != 0:
   News.objects.filter(id=deletenews).delete()
  allnews = News.objects.all().order_by('-time_date')
  return render(request,'news_manage.html',{'allnews':allnews})

@login_required
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
