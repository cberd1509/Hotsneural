from django.shortcuts import render
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import HttpResponse
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import time
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

		ts = int(time.time())

		Formdata = request.POST

		eorMethod = Formdata.get("eorMethod","")
		eorDescription = Formdata.get("eorDescription","")
		VPN = Formdata.get("VPN","")
		TIR = Formdata.get("TIR","")
		PBT = Formdata.get("PBT","")
		ROI = Formdata.get("ROI","")
		ProdAcum = Formdata.get("ProdAcum","")
		imgBase64 = Formdata.get("imgBase64","")

		imgBase64 = imgBase64.split(",")[1]
		imgBase64 = bytes(imgBase64,'utf-8')


		with open("static/plots/%s.png"%ts,"wb") as fh:
			fh.write(base64.decodebytes(imgBase64))
		
			
		http_response = HttpResponse(content_type='application/pdf')
		http_response['Content-Disposition'] = 'attachment; filename="%s.pdf"'%ts
		buffer = io.BytesIO()
		p=canvas.Canvas(buffer, pagesize=letter)
		

		im = ImageReader('static/images/templateBase.jpg')

		p.drawImage(im,x=0,y=0,width=8.5*inch, height=11*inch)

		im = ImageReader('static/plots/%s.png'%ts)
		p.drawImage(im,x=0.454*inch,y=3.971*inch,width=7.592*inch, height=3.796*inch, mask='auto')

		pdfmetrics.registerFont(TTFont('Bebas', 'static/fonts/BebasNeue.ttf'))
		pdfmetrics.registerFont(TTFont('Flama', 'static/fonts/Flama.ttf'))

		
		p.setFont('Bebas',29)
		p.drawRightString( 8.165*inch , 8.46*inch, eorMethod)

		p.setFont('Flama',12)
		p.drawCentredString( 4.686*inch , 3.061*inch, VPN) #Valor Presente Neto
		p.drawCentredString( 4.686*inch , 2.66*inch, TIR) #Tasa Interna de Retorno
		p.drawCentredString( 4.686*inch , 2.243*inch, PBT) #Payback Time
		p.drawCentredString( 4.686*inch , 1.824*inch, ROI) #Retorno a la Inversión
		p.drawCentredString( 4.686*inch , 1.417*inch, ProdAcum) #Producción Acumulada



		p.showPage()
		p.save()

		pdf = buffer.getvalue()
		buffer.close()
		http_response.write(pdf)


		return http_response