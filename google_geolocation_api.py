import requests
import urllib.parse
import pandas as pd
import csv
import time

GOOGLE_API_KEY = 'xxxx'

df = pd.read_csv('C:/LABURO/1-1000.csv', delimiter=';')
filas_procesadas = []


for index, row in df.iterrows():
    matricula = row['MATRICULA']
    domicilio = row['DOMICILIO']
    cp = str(row['CP'])
    localidad = row['LOCALIDAD']
    provincia = row['PROVINCIA']
    
    # Guardar los campos en variables o hacer alguna operación
    api_key = GOOGLE_API_KEY
    address = "'" + domicilio + ", "  + localidad + ", "  + cp + ", " + provincia + ", " + "Argentina" + "'" 
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    endpoint = f"{base_url}?address={urllib.parse.quote(address)}&key={api_key}"
    
    print(endpoint)
    
    print(f'MATRICULA: {matricula}, DOMICILIO: {domicilio}, CP: {cp}, LOCALIDAD: {localidad}, PROVINCIA: {provincia}')
    
    response = requests.get(endpoint)
    
    if response.status_code not in range(200, 299):
        print(response.status_code)
        lat = 0
        lon = 0
    try:
        results = response.json()['results'][0]
        lat = results['geometry']['location']['lat']
        lon = results['geometry']['location']['lng']
    except:
       pass
    finally:  
        fila_procesada = [matricula, domicilio, cp, localidad, provincia, lat, lon]
        filas_procesadas.append(fila_procesada)
        time.sleep(2)

with open('C:/LABURO/salida.csv', mode='w', newline='', encoding='utf-8') as archivo_salida:
    escritor_csv = csv.writer(archivo_salida, delimiter=';')
    escritor_csv.writerow(['MATRICULA', 'DOMICILIO', 'CP', 'LOCALIDAD', 'PROVINCIA' , 'LATITUD' , 'LONGITUD'])
    escritor_csv.writerows(filas_procesadas)

print('terminado')
