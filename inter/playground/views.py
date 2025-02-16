from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import fitz
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

@csrf_exempt
def read_pdf_view(request):
    if request.method == "POST":
        if "file" not in request.FILES:
            return JsonResponse({"error": "No file provided"}, status=400)

        pdf_file = request.FILES["file"]

        try:
            doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()

            # Rendering the response with extracted content
            return render(request, 'html/upload_pdf.html', {'content': text})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # For GET request, just render the upload form
    return render(request, 'html/upload_pdf.html')
# def read_pdf_view(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

#     if "file" not in request.FILES:
#         return JsonResponse({"error": "No file provided"}, status=400)

#     pdf_file = request.FILES["file"]

#     try:
#         doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
#         text = ""
#         for page in doc:
#             text += page.get_text()
#         return JsonResponse({"content": text}, status=200)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)