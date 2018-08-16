from keras.models import load_model
from keras import optimizers
from keras.models import Model
from keras.models import model_from_json
from sklearn.externals import joblib
from xgboost import XGBClassifier
from keras.utils import np_utils
import numpy as np
import keras


def getEORMethod(Area, Porosidad, Permeabilidad, Depth, API, Viscosidad, Temp, Soi):

    jsonFile = open('static/models/modelClassif.json','r')
    loaded_model_json = jsonFile.read()
    jsonFile.close()
    keras.backend.clear_session()

    model = model_from_json(loaded_model_json)
    model.load_weights('static/models/modelClassif.h5')

    model.compile(optimizer="adam",loss="categorical_crossentropy",metrics=["accuracy"])

    Datos = np.array([Area, Porosidad, Permeabilidad, Depth, API, Viscosidad, Temp, Soi])
    Datos = Datos/np.max(Datos)

    Datos = np.reshape(Datos,(1,8))

    DataFinal = model.predict(Datos)
    DataFinal = np.round(DataFinal)

    EORMethod = "No EOR"
    if np.array_equal(DataFinal,[[0,0,0,0,0,0,0]]):
        EORMethod = "Inyección de Polímeros"
    elif np.array_equal(DataFinal,[[0,1,0,0,0,0,0]]):
        EORMethod = "Inyección Cíclica de Vapor"
    elif np.array_equal(DataFinal,[[0,0,0,0,0,0,1]]):
        EORMethod = "Inyección continua de Vapor"
    elif np.array_equal(DataFinal,[[0,0,1,0,0,0,0]]): 
        EORMethod = "Inyección de Aire"
    elif np.array_equal(DataFinal,[[0,0,0,0,0,1,0]]): 
        EORMethod = "SAGD"
    elif np.array_equal(DataFinal,[[0,0,0,0,1,0,0]]):
        EORMethod = "Inyección de Agua Caliente"
    elif np.array_equal(DataFinal,[[1,0,0,0,0,0,0]]):
        EORMethod = "Inyección de CO2"

    return EORMethod, DataFinal

def CumulativeProduction(prodArray):

  cumulativeArray  = []
  A = 0

  for i in range(0,4):
  	YearProd = prodArray[0][i]
  	A = YearProd * 365
  	np.append(cumulativeArray,A)

  return cumulativeArray,A



def analisis_financiero(NWP, NPI, Np, bbl_cost, LC, transport_cost, WS_fr=4, WS_cost=100000, t_interes = 0.1):
    
    #NPW = Numero de pozos productores
    #NPI = numero de pozos inyectores
    #WS_fr es frecuencia de well service en años
    #WS_cost es costo de well service en dolares americanos
    #LC es lifting cost en dolares americanos
    #Np es producción acumulada
    #t_interes es la tasa de interes de oportunidad anual 
    T_eval = 5 #Tiempo de evaluacion en años
    No_WS = T_eval/WS_fr # Número de well services
    ingresos = np.zeros(5)
    for i in range(len(Np)):
        ingresos[i] = Np[i]*bbl_cost
    #Egresos en tiempo cero
    E_cero = (No_WS*NWP + No_WS*NPI)*WS_cost + transport_cost
    
    #Egresos en el resto del año
    #Regalias, no creo que haya más que explicar
    egresos = np.zeros(5)
    for i in range(len(ingresos)):
        egresos[i] = 0.1*ingresos[i] + LC*Np[i]
    flujos_de_caja = np.zeros(5)
    for i in range(len(egresos)):
        flujos_de_caja[i] = ingresos[i] - egresos[i]
    flujos_de_caja_1 = np.zeros(6)
    flujos_de_caja_1[0] = E_cero*(-1)
    for i in range(len(ingresos)):
        flujos_de_caja_1[i+1] = flujos_de_caja[i]
        
    VPN = np.npv(t_interes,flujos_de_caja_1) 
    
    flujo_acumulado = np.zeros(5)
    flujo_acumulado1 = np.cumsum(flujos_de_caja_1,axis=0)
    idx = np.max(np.where(flujo_acumulado1 <= 0)[0]) #Posicion del ultimo periodo con flujo de caja negativo
    flujo_acumulado_cero_mas_uno = flujo_acumulado1[idx+1]
    flujo_neto_cero_mas_uno = flujos_de_caja[idx+1]
    Payback_time = idx + (flujo_acumulado_cero_mas_uno/flujo_neto_cero_mas_uno) #Anual
    

    TIR = np.irr(flujos_de_caja_1)
    ingresos_para_vpn = np.zeros(6)
    ingresos_para_vpn[0] = 0
    for i in range(len(ingresos)):
        ingresos_para_vpn[i+1] = ingresos[i]
    egresos_para_vpn = np.zeros(6)
    egresos_para_vpn[0] = -E_cero
    for i in range(len(ingresos)):
        egresos_para_vpn[i+1] = egresos[i]

    VPN_ingresos = np.npv(t_interes, ingresos_para_vpn)
    
    VPN_egresos = np.npv(t_interes, egresos_para_vpn)
    RBC = VPN_ingresos/VPN_egresos
    
    return VPN, TIR, Payback_time, RBC


def regresion(K, Por, D, API, Visc, h, P_yac, NPW, T_yac):
    #Crear variables numéricas
    X_num = np.array([[K, Por, D, API, Visc, h, P_yac, NPW, T_yac], 
                     [K, Por, D, API, Visc, h, P_yac, NPW, T_yac], 
                     [K, Por, D, API, Visc, h, P_yac, NPW, T_yac], 
                     [K, Por, D, API, Visc, h, P_yac, NPW, T_yac], 
                     [K, Por, D, API, Visc, h, P_yac, NPW, T_yac]])
    #Crear variable categórica
    Years = np.array([['Y1', 'Y2', 'Y3', 'Y4', 'Y5']])
    Years1 = Years.reshape(5,1)

    def one_hot_encode_object_array(arr):
        uniques, ids = np.unique(arr, return_inverse=True)
        return np_utils.to_categorical(ids, len(uniques))
    Year_ohe =one_hot_encode_object_array(Years1) #Variable categórica
    X_tot = np.concatenate((X_num, Year_ohe),axis=1) #Vector de entrada
    
    #Montaje del escalador
    scaler = joblib.load('static/models/MinMaxscaler_X.save')
    X_scaled = scaler.transform(X_tot) #Vector de entrada escalado
    
    #Montaje del modelo
    model = joblib.load('static/models/finalized_model.sav')
    resultados = model.predict(X_scaled)
    
    #Montaje del scalador de la salida
    scaler_Y = joblib.load('static/models/MinMaxscaler_Y.save')
    resultados_reales = abs(scaler_Y.inverse_transform([resultados])) #Vector de entrada escalado
    
    return resultados_reales

def analisis_financiero(NWP, NPI, Np, bbl_cost, LC, recorrido, WS_fr=4, WS_cost=100000, t_interes = 0.1):
    
    #NPW = Numero de pozos productores
    #NPI = numero de pozos inyectores
    #WS_fr es frecuencia de well service en años
    #WS_cost es costo de well service en dolares americanos
    #LC es lifting cost en dolares americanos
    #Np_dia es producción diaria
    #t_interes es la tasa de interes de oportunidad anual 
    #Recorrido va en km
    
    if recorrido < 50:
        tarifa_transporte = 79.78
    elif 51<recorrido<100:
        tarifa_transporte = 72.47
    elif 101<recorrido<200:
        tarifa_transporte = 64.56
    elif 201<recorrido<300:
        tarifa_transporte = 54.67
    elif 301<recorrido<400:
        tarifa_transporte = 46.67
    elif 401<recorrido<600:
        tarifa_transporte = 39.51
    elif 601<recorrido<800:
        tarifa_transporte = 36.80
    elif 801<recorrido<1000:
        tarifa_transporte = 33.38
    elif 1001<recorrido<1400:
        tarifa_transporte = 31.36
    else:
        tarifa_transporte = 28.70
        
    tarifa_transporte_USD = tarifa_transporte/3000
    
    T_eval = 5 #Tiempo de evaluacion en años
    No_WS = T_eval/WS_fr # Número de well services
    ingresos = np.zeros(5)
    for i in range(len(Np)):
        ingresos[i] = Np[i]*bbl_cost
    #Egresos en tiempo cero
    E_cero = (No_WS*NWP + No_WS*NPI)*WS_cost 
    

    costo_transporte = np.zeros(5)
    for i in range(len(ingresos)):
        costo_transporte[i] = tarifa_transporte_USD*Np[i]*recorrido 
    
    #Egresos en el resto del año
    #Regalias, no creo que haya más que explicar
    egresos = np.zeros(5)
    for i in range(len(ingresos)):
        egresos[i] = 0.1*ingresos[i] + LC*Np[i] + costo_transporte[i]
    flujos_de_caja = np.zeros(5)
    for i in range(len(egresos)):
        flujos_de_caja[i] = ingresos[i] - egresos[i]
    flujos_de_caja_1 = np.zeros(6)
    flujos_de_caja_1[0] = E_cero*(-1)
    for i in range(len(ingresos)):
        flujos_de_caja_1[i+1] = flujos_de_caja[i]
        
    VPN = np.npv(t_interes,flujos_de_caja_1) 
    

    TIR = np.irr(flujos_de_caja_1)
    ingresos_para_vpn = np.zeros(6)
    ingresos_para_vpn[0] = 0
    for i in range(len(ingresos)):
        ingresos_para_vpn[i+1] = ingresos[i]
    egresos_para_vpn = np.zeros(6)
    egresos_para_vpn[0] = -E_cero
    for i in range(len(ingresos)):
        egresos_para_vpn[i+1] = egresos[i]

    VPN_ingresos = np.npv(t_interes, ingresos_para_vpn)
    
    VPN_egresos = np.npv(t_interes, egresos_para_vpn)
    RBC = VPN_ingresos/VPN_egresos
    
    return VPN, TIR, RBC