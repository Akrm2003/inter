from .models import PDFSummary
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
import fitz
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from django.views.decorators.csrf import csrf_exempt


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

def pdf_summary(request):
    summary_text = None

    if request.method == "POST":
        user = request.POST.get("user")
        if not user:
            print("No user specified")
            return JsonResponse({"error": "No user specified"}, status=400)

        if "file" not in request.FILES:
            return JsonResponse({"error": "No file provided"}, status=400)

        pdf_file = request.FILES["file"]

        try:
            doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            pdf_text = "".join(page.get_text() for page in doc)
        except Exception as e:
            return JsonResponse({"error": f"Error reading PDF: {str(e)}"}, status=400)
        
        chat = ChatGroq(temperature=0, model_name="llama-3.1-8b-instant")
        system = "You are a helpful assistant, specialized in summarizing texts"
        human = "{text}"
        prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
        chain = prompt | chat

        try:
            result = chain.invoke({"text": pdf_text})
            summary_text = result.content
        except Exception as e:
            return JsonResponse({"error": f"Error generating summary: {str(e)}"}, status=500)

        PDFSummary.objects.create(
            user=user,
            full_text=pdf_text,
            summary=summary_text
        )
        # return render(request, "html/pdf_summary.html", {"summary": summary_text, "user": user})
        return JsonResponse({"summary": summary_text, "user": user}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=405)

def user_history(request):
    if request.method == "GET":
        user = request.GET.get("user")
        if not user:
            return JsonResponse({"error": "No user specified"}, status=400)
            # return render(request, "html/user_history.html", {"error": "No user specified"})

        summaries = PDFSummary.objects.filter(user=user)

        if not summaries:
            return JsonResponse({"error": "No history found for this user"}, status=404)
            # return render(request, "html/user_history.html", {"error": "No history found for this user"})
        return JsonResponse({"summaries": [summary.summary for summary in summaries]}, status=200)
        # return render(request, "html/user_history.html", {"summaries": summaries})
    return JsonResponse({"error": "Invalid request method"}, status=405)
    # return render(request, "html/user_history.html", {"error": "Invalid request method"})