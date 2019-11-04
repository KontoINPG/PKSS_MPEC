from bottle import run, get, request, post
import csv


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
 
    time = 61*60
    
    timeInd = int((time/60)/5)
    print(timeInd)

    TempWater = float(tabTempWater[timeInd])
    TempAir = float(tabTempAir[timeInd])
    
    mpec = [{'WaterTemp' : TempWater,},
        {'AirTemp' : TempAir,},
        {'WaterPress' : PressWater}]
    
    return{'mpec':mpec}

@post('/mpec/setPressure')
def setPressure():
    global PressWater
    PressWater = request.json.get('PressWater')
    print(PressWater)

run(host='localhost', port=8081, debug=True)
