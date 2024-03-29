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
oldTimestamp = "1"


@get('/mpec/data')
def getAll():
    global TempWater
    global TempAir
    global oldTimestamp
 
    timeJson = requests.get('https://closingtime.szyszki.de/api/time') #61*60
    time = timeJson.json()['symSec']   #1
    #print(timeJson.json()['symSec'])

    timestampJson = requests.get('https://closingtime.szyszki.de/api/prettytime')
    timestamp = timestampJson.json()['symTime']   #1
    #print(timestamp)
    
    timeInd = int((time/60)/5)
    print(timeInd)

    TempWater = float(tabTempWater[timeInd])
    TempAir = float(tabTempAir[timeInd])
    
    #mpec = {'WaterTemp' : str(TempWater),
     #   'AirTemp' : str(TempAir),
      #  'WaterPress' : str(PressWater)}


    if timestamp != oldTimestamp:
        try:
            requests.post('https://anoldlogcabinforsale.szyszki.de/provider/log', json={
            "status": "Run",
            "warm_water_stream_Fzm": str(PressWater),
            "incoming_water_temp_Tzm": str(TempWater),
            "failure": "False",
            "outside_temp_To": str(TempAir),
            "timestamp": timestamp} )
        except:
            print("Dominiki baza nie działa :)")

        try:
            requests.post('https://layanotherlogonthefire.szyszki.de/provider/log', json={
            "status": "Run",
            "warm_water_stream_Fzm": str(PressWater),
            "incoming_water_temp_Tzm": str(TempWater),
            "failure": "False",
            "outside_temp_To": str(TempAir),
            "timestamp": timestamp} )
        except:
            print("Mateusza baza nie działa :) ")
            
    oldTimestamp = timestamp
    
    return{'WaterTemp' : str(TempWater),
        'AirTemp' : str(TempAir),
        'WaterPress' : str(PressWater)}
    
@post('/mpec/setPressure')
def setPressure():
    global PressWater
    PressWater = float(request.json.get('PressWater'))
    print(PressWater)

run(host='0.0.0.0', port=8080, debug=True)
#run(host='localhost', port=8081, debug=True)

