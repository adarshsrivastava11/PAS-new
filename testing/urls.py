from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import *
from addy.views import *




urlpatterns = patterns('',
  (r'^$', main_page),
  (r'^login/$', login_page),
  (r'^logout/$', logout_view),
  (r'^signup/$', signup),
  (r'^signup_success/$', signup_success),
  (r'^(?P<user_name>[a-zA-Z_]+)/dashboard/$', dashboard),
  (r'^(?P<user_name>[a-zA-Z_]+)/changepassword/$', changepassword),
  (r'^(?P<user_name>[a-zA-Z_]+)/fillform/$', fillform),
  (r'^poweruser/$', poweruser),
  (r'^newsmanage/$', manage_news),
  (r'^(?P<user_name>[a-zA-Z_]+)/resume/$', resume_manage),
  (r'^companysignup/$', company_signup),
  (r'^(?P<username>[a-zA-Z_]+)/homepage/$', homepage),
  (r'^(?P<username>[a-zA-Z_]+)/opening/$', job_opening),

  
 
  
  
  (r'^admin/', include(admin.site.urls)),
  
  
  )


