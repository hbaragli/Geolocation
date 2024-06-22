import requests
import urllib.parse
import pandas as pd
import csv
import time



df = pd.read_csv('C:/LABURO/1-5000.csv', delimiter=';')
filas_procesadas = []


for index, row in df.iterrows():
    matricula = row['MATRICULA']
    domicilio = row['DOMICILIO']
    cp = str(row['CP'])
    localidad = row['LOCALIDAD']
    provincia = row['PROVINCIA']
    
    # Guardar los campos en variables o hacer alguna operación
    
    address = "'" + domicilio + ", "  + localidad + ", "  + cp + ", " + provincia + ", " + "Argentina" + "'" 
    url = 'https://nominatim.openstreetmap.org/search?q=' + urllib.parse.quote(address) +'&format=json&limit=1'
    print(url)
    print(f'MATRICULA: {matricula}, DOMICILIO: {domicilio}, CP: {cp}, LOCALIDAD: {localidad}, PROVINCIA: {provincia}')
    try:
        response = requests.get(url)
        response.raise_for_status()
        response_json = response.json()
        print(response)
        lat = response_json[0]["lat"]
        lon = response_json[0]["lon"]
    except requests.exceptions.HTTPError as http_err:
       lat = 0
       lon = 0
    except Exception as err:
       lat = 0
       lon = 0
    finally:  
        fila_procesada = [matricula, domicilio, cp, localidad, provincia, lat, lon]
        filas_procesadas.append(fila_procesada)
        time.sleep(2)

with open('C:/LABURO/salida.csv', mode='w', newline='', encoding='utf-8') as archivo_salida:
    escritor_csv = csv.writer(archivo_salida, delimiter=';')
    escritor_csv.writerow(['MATRICULA', 'DOMICILIO', 'CP', 'LOCALIDAD', 'PROVINCIA' , 'LATITUD' , 'LONGITUD'])
    escritor_csv.writerows(filas_procesadas)

print('terminado')