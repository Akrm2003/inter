from .models import PDFSummary
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import fitz
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


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
def pdf_summury(request):
    summary_text = None

    if request.method == "POST":
        user = request.POST.get("user")  # Get username from form

        if "file" not in request.FILES:
            return render(request, "html/upload_pdf.html", {"error": "No file provided"})

        pdf_file = request.FILES["file"]

        try:
            doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            pdf_text = "".join(page.get_text() for page in doc)
        except Exception as e:
            return render(request, "html/upload_pdf.html", {"error": str(e)})

        chat = ChatGroq(temperature=0, model_name="llama-3.1-8b-instant")
        system = "You are a helpful assistant, specialized in summarizing texts"
        human = "{text}"
        prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
        chain = prompt | chat

        result = chain.invoke({"text": pdf_text})
        summary_text = result.content

        PDFSummary.objects.create(
            user=user,
            full_text=pdf_text,
            summary=summary_text
        )

    return render(request, "html/upload_pdf.html", {"human": summary_text})


from django.shortcuts import render
from .models import PDFSummary

@csrf_exempt
def user_history(request):
    if request.method == "GET":
        user = request.GET.get("user")
        if not user:
            return render(request, "html/user_history.html", {"error": "No user specified"})

        summaries = PDFSummary.objects.filter(user=user)

        if not summaries:
            return render(request, "html/user_history.html", {"error": "No history found for this user"})

        return render(request, "html/user_history.html", {"summaries": summaries})

    return render(request, "html/user_history.html", {"error": "Invalid request method"})