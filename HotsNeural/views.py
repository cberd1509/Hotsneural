from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def animsition(request):
	return render(request,'animsitiontrial.html')

def processData(request):
	if request.method=="POST":
		return render(request, 'economicanalysis.html')
		#return("Hola Mundo")
# Create your views here.
