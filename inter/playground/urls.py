from django.urls import path
from . import views

# this is called a URLconf
urlpatterns = [
	path('hello/', views.say_hello),
	path('test_endpoints/', views.test_endpoints),
 	path("read-pdf/", views.pdf_summury),
	path('', views.wellcome)
]
