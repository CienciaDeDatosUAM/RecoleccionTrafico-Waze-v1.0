
import os
import json
from datetime import datetime
import dotenv #Se debe agregar esta libreria para poder utilizar el archivo .env

class FiltrarDatosJson:
    # Lee el archivo .env
    dotenv.load_dotenv()
    ruta_mac = os.environ.get("ruta_mac")
    def __init__(self, datos_sin_filtrar):
        self.datos_sin_filtrar = datos_sin_filtrar

    def filtrar_datos(self):
        date_str = datetime.now().strftime('%d-%m-%y')
        input_dir = f'{self.ruta_mac}/{date_str}'
        output_dir = f'{self.ruta_mac}/{date_str}'
        os.makedirs(output_dir, exist_ok=True)

        with open(f'{input_dir}/{self.datos_sin_filtrar}.json', 'r') as archivo:
            datos = json.load(archivo)

        datos_filtrados = {}
        for timestamp, cuadrantes in datos.items():
            cuadrantes_filtrados = {}
            for cuadrante, info in cuadrantes.items():
                alerts_filtrados = []
                for alert in info.get("alerts", []):
                    entry = {
                        "id": alert["id"],
                        "tipo": alert["type"],
                        "subtipo": alert["subtype"],
                        "latitud": alert["location"]["y"],
                        "longitud": alert["location"]["x"]
                    }
                    alerts_filtrados.append(entry)
                cuadrantes_filtrados[cuadrante] = alerts_filtrados
            datos_filtrados[timestamp] = cuadrantes_filtrados

        with open(f'{output_dir}/Datos_waze_filtrados.json', 'w') as archivo:
            json.dump(datos_filtrados, archivo, indent=4)
            archivo.write('\n')

        print("Filtrado completo. Datos actualizados guardados.")
        return datos_filtrados