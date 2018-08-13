from django.shortcuts import render
from django.http import HttpResponse
from django.http import FileResponse
from reportlab.pdfgen import canvas
import json
import base64
import reportlab
import io

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

def getPDF(request):
	if request.method=="POST":

		'''Formdata = request.POST

		eorMethod = Formdata.get("eorMethod","")
		eorDescription = Formdata.get("eorDescription","")
		VPN = Formdata.get("VPN","")
		TIR = Formdata.get("TIR","")
		PBT = Formdata.get("PBT","")
		ROI = Formdata.get("ROI","")
		imgBase64 = Formdata.get("imgBase64","")

		imgBase64 = imgBase64.split(",")[1]
		imgBase64 = bytes(imgBase64,'utf-8')


		with open("ImageToSave.jpg","wb") as fh:
			fh.write(base64.decodebytes(imgBase64))

		'''	

		http_response = HttpResponse(content_type='application/pdf')
		http_response['Content-Disposition'] = 'inline; filename="report.pdf"'

		buffer = io.BytesIO()
		p=canvas.Canvas(buffer)
		p.drawString(100,100, "Hello World")

		p.showPage()
		p.save()

		pdf = buffer.getvalue()
		buffer.close()
		http_response.write(pdf)
		

		return http_response