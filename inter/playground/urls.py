from django.urls import path
from . import views

# this is called a URLconf
urlpatterns = [
	path('hello/', views.say_hello),
	path('read_pdf/', views.read_pdf),
	path('test_endpoints/', views.test_endpoints),
	path('', views.wellcome)
]
