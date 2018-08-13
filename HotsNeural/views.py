from django.shortcuts import render
from django.http import HttpResponse
import json

def home(request):
    return render(request, 'home.html')

def animsition(request):
	return render(request,'animsitiontrial.html')

def processData(request):
	if request.method=="POST":
		Formdata = request.POST

		Area = float(Formdata.get("Area",""))
		Porosidad = float(Formdata.get("Porosidad",""))
		Permeabilidad = float(Formdata.get("Permeabilidad",""))
		Profundidad = float(Formdata.get("Profundidad",""))
		GravedadAPI = float(Formdata.get("GravedadAPI",""))
		Viscosidad = float(Formdata.get("Viscosidad",""))
		Temperatura = float(Formdata.get("Temperatura",""))
		Soi = float(Formdata.get("Soi",""))
		EvTime = float(Formdata.get("EvTime",""))
		WellNumber = float(Formdata.get("WellNumber",""))

		#return(HttpResponse("Se obtienen valores de %f %f %f %f %f" %(Area,Porosidad,Permeabilidad,Profundidad,GravedadAPI)))
		return render(request, 'economicanalysis.html',dict(prueba="prueba",prueba2="prueba2"));
		#return("Hola Mundo")
# Create your views here.

def forecast(request):
	if request.method == "POST":
		Formdata = request.POST

		row = [5000,4200,3500,2400,1900]
		jsonArray = json.dumps(row)

		return render(request, 'Results.html',dict(DailyProd=jsonArray));



