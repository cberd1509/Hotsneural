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
import HotsNeural.neuralmodels as NM


def home(request):
    return render(request, 'home.html')

def animsition(request):
	pr = NM.prueba()
	return HttpResponse(pr)

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
		PYac = float(Formdata.get("PYac",""))
		WellNumber = float(Formdata.get("WellNumber",""))
		Espesor = float(Formdata.get("espesor",""))
		InyWellNumber = float(Formdata.get("InyWellNumber",""))

		EOR,OHE_EOR = NM.getEORMethod(Area,Porosidad,Permeabilidad,Profundidad,GravedadAPI,Viscosidad,Temperatura,Soi)

		return render(request, 'economicanalysis.html',dict(EOR=EOR,MetodoOHE=OHE_EOR,Area=Area,Porosidad=Porosidad,Permeabilidad=Permeabilidad,Profundidad=Profundidad,GravedadAPI=GravedadAPI,Viscosidad=Viscosidad,Temperatura=Temperatura,Soi=Soi,PYac=PYac,WellNumber=WellNumber,Espesor=Espesor,InyWellNumber=InyWellNumber));
		#return("Hola Mundo")
# Create your views here.

def forecast(request):
	if request.method == "POST":
		Formdata = request.POST

		Area = float(Formdata.get("Area"))
		Porosidad = float(Formdata.get("Porosidad"))
		Permeabilidad = float(Formdata.get("Permeabilidad"))
		Profundidad = float(Formdata.get("Profundidad"))
		GravedadAPI = float(Formdata.get("GravedadAPI"))
		Viscosidad = float(Formdata.get("Viscosidad"))
		Temperatura = float(Formdata.get("Temperatura"))
		Soi = float(Formdata.get("Soi"))
		PYac = float(Formdata.get("PYac"))
		WellNumber = float(Formdata.get("WellNumber"))
		Espesor = float(Formdata.get("Espesor"))
		InyWellNumber = float(Formdata.get("InyWellNumber"))
		EORMethod = Formdata.get("EORMethod")

		tripDistance = float(Formdata.get("tripDistance"))
		bblCost = float(Formdata.get("bblCost"))
		liftingCost = float(Formdata.get("liftingCost"))
		wsFreq = float(Formdata.get("wsFreq"))
		tInteres = float(Formdata.get("tInteres"))
		wsCost = float(Formdata.get("wsCost"))


		ProdArray = NM.regresion(Permeabilidad, Porosidad, Profundidad, GravedadAPI, Viscosidad, Espesor, PYac, WellNumber, Temperatura)
		CumulativeArray, CumProdTotal = NM.CumulativeProduction(ProdArray)


		if(EORMethod=="Inyección de Polímeros"):
			EORMethod="Inyección de Agua Caliente"


		eorDescription=""
		if(EORMethod=="SAGD"):
			eorDescription = "Es un método de recobro térmico que consiste en perforar un par de pozos horizontales paralelos, un inyector arriba y un productor abajo separados a una distancia vertical de unos 5 m. En el pozo superior se inyecta vapor al yacimiento, y a medida que el vapor se expande este calienta al crudo, reduciendo su viscosidad y logrando que drene por gravedad hacia el pozo productor."
		elif(EORMethod=="Inyección Cíclica de Vapor"):
			eorDescription = "Método de recobro térmico en el que se inyecta vapor en un pozo y luego se vuelve a poner en producción. Esto se logra en tres etapas: Una de inyección, en la cual se introduce vapor en el yacimiento. La siguiente etapa requiere cerrar el pozo durante varios días para permitir la distribución uniforme del vapor, y la última etapa en la cual se produce el petróleo calentado a través del mismo pozo."
		elif(EORMethod=="Inyección continua de Vapor"):
			eorDescription = "Método de recobro térmico por el cual el vapor generado en la superficie se inyecta en el yacimiento a través de pozos de inyección distribuidos especialmente en patrones. Cuando el vapor entra al yacimiento, este calienta al petróleo crudo y reduce su viscosidad, impulsando su movilidad y producción."
		elif(EORMethod == "Inyección de Aire"):
			eorDescription = "Método de recobro térmico en el que se genera un frente de combustión dentro del yacimiento mediante la inyección de aire. El calor generado por la ignición del aire produce la quema y craqueo de buena parte del crudo en sitio. A medida que el fuego se desplaza, el frente empuja hacia los pozos productores una mezcla de gases calientes, vapor y agua que reduce la viscosidad del petróleo y lo desplaza."
		elif(EORMethod == "Inyección de Agua Caliente"):
			eorDescription = "Método de recobro térmico en el cual se inyecta agua caliente en un yacimiento a través de pozos distribuidos especialmente en patrones. El agua caliente reduce la viscosidad del crudo, aumentando su movilidad hacia los pozos productores. Este método de recobro es preferible en condiciones donde la formación es altamente sensible al agua dulce."
		elif(EORMethod == "Inyección de CO2"):
			eorDescription = "Método de recobro mejorado en el cual se inyecta dióxido de carbono en condiciones donde la presión del yacimiento es inferior a la presión mínima de miscibilidad del CO2. En este caso el CO2 y el crudo no se mezclan, y es el dióxido de carbono el que barre al petróleo in situ, aumentando la recuperación de crudo hacia los pozos productores."
		elif(EORMethod=="Inyección de Polímeros"):
			eorDescription = "Este es un método de recobro químico, que consiste en la adicíón de sustancias polímericas en el agua de inyección cuyo objetivo es aumentar la viscosidad de esta. De esta forma, es posible mejorar la eficiencia macroscópica de barrido mejorando la relación de movilidad entre el agua de inyección y el crudo. El método tiene mejores resultados en viscosidades de crudo bajas."

		VPN, TIR, BCR = NM.analisis_financiero(WellNumber, InyWellNumber, ProdArray[0]*365, bblCost, liftingCost, tripDistance, wsFreq, wsCost, tInteres)

		DailyProd = json.dumps(ProdArray.tolist())
		CumulativeProd = json.dumps(CumulativeArray)
		return render(request, 'Results.html',dict(DailyProd=DailyProd, EORMethod=EORMethod, eorDescription=eorDescription, VPN=VPN, TIR=TIR, tripDistance=tripDistance, BCR=BCR, CumulativeProd=CumulativeProd, CumProdTotal=CumProdTotal));


def getPDF(request):
	if request.method=="POST":

		ts = int(time.time())

		Formdata = request.POST

		eorMethod = Formdata.get("eorMethod","")
		eorDescription = Formdata.get("eorDescription","")
		VPN = Formdata.get("VPN","")
		TIR = Formdata.get("TIR","")
		BCR = Formdata.get("BCR","")
		tripDistance = Formdata.get("tripDistance","")
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
		p.drawCentredString( 4.686*inch , 2.243*inch, tripDistance) #Distancia de transporte
		p.drawCentredString( 4.686*inch , 1.824*inch, BCR) #Relación Costo Beneficio
		p.drawCentredString( 4.686*inch , 1.417*inch, ProdAcum)#Producción Acumulada



		p.showPage()
		p.save()

		pdf = buffer.getvalue()
		buffer.close()
		http_response.write(pdf)


		return http_response