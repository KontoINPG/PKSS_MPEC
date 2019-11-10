from bottle import run, get, request, post
import csv
import requests


tabTempAir = []
tabTempWater = []



with open('Temperatura.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile,delimiter=';')
    for row in reader:
        #print(row['AirTemp'])
        tabTempAir.append(row['AirTemp'])
        tabTempWater.append(row['WaterTempAGH'])



TempWater = 70
TempAir = 6
PressWater = 1.0



@get('/mpec/data')
def getAll():
    global TempWater
    global TempAir
 
    timeJson = requests.get('https://closingtime.szyszki.de/api/time') #61*60
    time = timeJson.json()['symSec']   #1
    #print(timeJson.json()['symSec'])

    
    timeInd = int((time/60)/5)
    print(timeInd)

    TempWater = float(tabTempWater[timeInd])
    TempAir = float(tabTempAir[timeInd])
    
    mpec = [{'WaterTemp' : str(TempWater),},
        {'AirTemp' : str(TempAir),},
        {'WaterPress' : str(PressWater)}]
    
    return{'mpec':mpec}

@post('/mpec/setPressure')
def setPressure():
    global PressWater
    PressWater = request.json.get('PressWater')
    print(PressWater)

run(host='0.0.0.0', port=8080, debug=True)
