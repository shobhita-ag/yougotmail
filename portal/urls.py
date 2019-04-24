from django.conf.urls import url
from portal import views

urlpatterns = [
	# views for page loading
    url(r'^$', views.HomePage.as_view(), name='home'),
    url(r'^send_email$', views.SendEmail.as_view(), name='login')
]