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
  (r'^signup_fail/$', signup_fail),
  (r'^(?P<user_name>[a-zA-Z]+)/dashboard/$', dashboard),
  (r'^(?P<user_name>[a-zA-Z]+)/changepassword/$', changepassword),
  (r'^(?P<user_name>[a-zA-Z]+)/fillform/$', fillform),
  (r'^(?P<user_name>[a-zA-Z]+)/notconfirmed/$', notconfirmed),
  (r'^poweruser/$', poweruser),
  (r'^newsmanage/$', manage_news),
  (r'^(?P<user_name>[a-zA-Z]+)/resume/$', resume_manage),
  (r'^companysignup/$', company_signup),
  (r'^(?P<username>[a-zA-Z]+)/homepage/$', homepage),
  (r'^(?P<username>[a-zA-Z]+)/opening/$', job_opening),

  
 
  
  
  (r'^admin/', include(admin.site.urls)),
  
  
  )


