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

    timestampJson = requests.get('https://closingtime.szyszki.de/api/prettytime')
    timestamp = timestampJson.json()['symTime']   #1

    timeInd = int((time/60)/5)
    print(timeInd)

    TempWater = float(tabTempWater[timeInd])
    TempAir = float(tabTempAir[timeInd])
    
    mpec = [{'WaterTemp' : str(TempWater),},
        {'AirTemp' : str(TempAir),},
        {'WaterPress' : str(PressWater)}]


    response = requests.post('https://anoldlogcabinforsale.szyszki.de/provider/log', json={
    "status": "run",
    "warm_water_stream_Fzm": str(PressWater),
    "incoming_water_temp_Tzm": str(TempWater),
    "failure": "False",
    "outside_temp_To": str(TempAir),
    "timestamp": timestamp} )
    
    return{'mpec':mpec}

@post('/mpec/setPressure')
def setPressure():
    global PressWater
    PressWater = request.json.get('PressWater')
    print(PressWater)

run(host='localhost', port=8081, debug=True)
