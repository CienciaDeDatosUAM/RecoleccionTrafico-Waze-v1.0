import os
import requests
import json
from datetime import datetime
import pytz
import random
import time
import dotenv #Se debe agregar esta libreria para poder utilizar el archivo .env

class WazeAPI:
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/92.0.902.67 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Chrome/91.0.4472.124",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0",
        "Mozilla/5.0 (Linux; Android 10; Pixel 4 XL Build/QP1A.190711.020) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Mobile Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Version/13.1.2 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edge/90.0.818.66",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edge/83.0.478.56",
        "Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0",
        "Mozilla/5.0 (Linux; Android 11; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; AS; AS-Device) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
    ]
    # Lee el archivo .env
    dotenv.load_dotenv()
    ruta_mac = os.environ.get("ruta_mac")
    def __init__(self, cuadrantes):
        self.cuadrantes = cuadrantes

    def obtener_limites(self, coordenadas):
        longitudes = [coord[0] for coord in coordenadas]
        latitudes = [coord[1] for coord in coordenadas]
        top = max(latitudes)
        bottom = min(latitudes)
        left = min(longitudes)
        right = max(longitudes)
        return top, bottom, left, right

    def realizar_peticion(self):
        todos_los_datos = {}
        for nombre_cuadrante, coordenadas in self.cuadrantes.items():
            top, bottom, left, right = self.obtener_limites(coordenadas)
            url = f'https://www.waze.com/live-map/api/georss?top={top}&bottom={bottom}&left={left}&right={right}&env=row&types=alerts,traffic,users'
            respuesta = requests.get(url, headers={"User-Agent": random.choice(self.user_agents)})
            if respuesta.status_code == 200:
                datos = respuesta.json()
                todos_los_datos[nombre_cuadrante] = datos
                print(f"Datos del {nombre_cuadrante} obtenidos exitosamente.")
            else:
                print(f"Error al acceder a la API para {nombre_cuadrante}: {respuesta.status_code}")
            time.sleep(random.uniform(0, 3))
        self.guardar_datos(todos_los_datos)

    def guardar_datos(self, datos):
        date_str=datetime.now().strftime('%d-%m-%y')
        output_dir= f'{self.ruta_mac}/{date_str}'
        os.makedirs(output_dir, exist_ok=True)

        timezone_cdmx = pytz.timezone('America/Mexico_City')
        fecha_hora = datetime.now(timezone_cdmx).strftime("%d-%m-%y %H:%M")
        datos_con_fecha = {fecha_hora: datos}
        try:
            with open(f'{output_dir}/datos.json', 'r') as archivo:
                datos_existentes = json.load(archivo)
        except FileNotFoundError:
            datos_existentes = {}
        datos_existentes.update(datos_con_fecha)
        with open(f'{output_dir}/datos.json', 'w') as archivo:
            json.dump(datos_existentes, archivo, indent=4)
        print("Los datos se han guardado en 'datos.json'")