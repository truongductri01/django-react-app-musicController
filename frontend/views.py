from django.shortcuts import render

# Create your views here.
def index(request, *args, **kwargs):
    return render(request, "frontend/index.html")  # reference to the html file inside templates folder
