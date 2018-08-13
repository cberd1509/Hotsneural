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

		eorMethod="Inyección Contínua de Vapor"

		eorDescription = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer tristique rutrum dui, a facilisis ante sodales vitae. Sed venenatis metus purus, id fringilla urna interdum rutrum. In et est nec leo blandit ornare. Nullam vehicula massa ex, nec placerat nibh pharetra at. Suspendisse vel ipsum velit. Fusce bibendum nisi vitae ligula cursus, et placerat est hendrerit. Sed euismod finibus elit non tristique. Aliquam rutrum velit sit amet dignissim egestas. Aliquam ut quam commodo, varius felis at, condimentum purus. Vivamus gravida pellentesque turpis, vel tincidunt metus dapibus sed. Mauris leo eros, dapibus scelerisque sem et, porta malesuada lorem. Etiam id lorem a turpis aliquam iaculis. Vivamus vel bibendum dui, vitae cursus urna."

		VPN = 250000000
		TIR = 80
		PBT = 3
		ROI = 50

		row = [5000,4200,3500,2400,1900]
		jsonArray = json.dumps(row)

		return render(request, 'Results.html',dict(DailyProd=jsonArray, eorMethod=eorMethod, eorDescription=eorDescription, VPN=VPN, TIR=TIR, PBT=PBT, ROI=ROI));



