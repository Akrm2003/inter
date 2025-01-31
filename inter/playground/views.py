from django.shortcuts import render
from django.http import HttpResponse
# request handler
def say_hello(request):
    return render(request, 'html/hello.html', {"name": "akram", "age": 21}) #render already returns an HttpResponse 
def wellcome(request):
    return HttpResponse("wellcome to my playground")
def test_endpoints(request):
	return render(request, 'html/test_endpoints.html')
def read_pdf(request):
    if request.method == "POST":
        data = request.POST.get("data", "hi")
        return HttpResponse(f"Received: {data}")
    return HttpResponse("provide data.")