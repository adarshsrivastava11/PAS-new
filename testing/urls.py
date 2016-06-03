from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import *
from addy.views import *


## Note Include POWer USER URLS !!! To be updated

urlpatterns = patterns('',
  (r'^$', main_page),
  (r'^login/$', login_page),
  (r'^logout/$', logout_view),
  (r'^signup/$', signup),
  (r'^signup_success/$', signup_success),
  (r'^(?P<user_name>[a-zA-Z0-9_]+)/dashboard/$', dashboard),
  (r'^(?P<user_name>[a-zA-Z0-9_]+)/changepassword/$', changepassword),
  (r'^(?P<user_name>[a-zA-Z0-9_]+)/fillform/$', fillform),
  #(r'^poweruser/$', poweruser),
  #(r'^newsmanage/$', manage_news),
  (r'^(?P<user_name>[a-zA-Z0-9_]+)/resume/$', resume_manage),
  (r'^companysignup/$', company_signup),
  (r'^(?P<username>[a-zA-Z0-9_]+)/homepage/$', homepage),
  (r'^(?P<username>[a-zA-Z0-9_]+)/opening/$', job_opening),
  (r'^(?P<username>[a-zA-Z0-9_]+)/profile/$', student_profile),
  (r'^(?P<username>[a-zA-Z0-9_]+)/data/$', student_data),
  (r'^(?P<username>[a-zA-Z0-9_]+)/jobapplications/$', job_application),
  (r'^(?P<username>[a-zA-Z0-9_]+)/panel/$', panel),
  (r'^(?P<username>[a-zA-Z0-9_]+)/panel/activate_temp_student$', activate_temp_student),
  (r'^(?P<username>[a-zA-Z0-9_]+)/panel/deactivate_temp_student$', deactivate_temp_student),
  (r'^(?P<username>[a-zA-Z0-9_]+)/panel/add_news$', add_news),
  
  
 
  
  
  (r'^admin/', include(admin.site.urls)),
  
  
  )


