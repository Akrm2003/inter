from django.shortcuts import render
from django.http import HttpResponse

def root_message(request):
    return render(request, 'html/cat.html', {"name": "akram", "age": 21})