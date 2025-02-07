
import os
import pandas as pd
from datetime import datetime
import dotenv #Se debe agregar esta libreria para poder utilizar el archivo .env



class FiltrarDatosExcel:
    # Lee el archivo .env
    dotenv.load_dotenv()
    ruta_mac = os.environ.get("ruta_mac")
    def __init__(self, datos_filtrados):
        self.datos_filtrados = datos_filtrados

    def guardar_en_csv(self, nombre_archivo="Datos_waze_filtrados.csv"):
        filas = []
        for timestamp, cuadrantes in self.datos_filtrados.items():
            for cuadrante, lista_de_eventos in cuadrantes.items():
                for evento in lista_de_eventos:
                    fila = {
                        "Fecha": timestamp,
                        "Id": evento.get("id"),
                        "Tipo": evento.get("tipo"),
                        "Sub-Tipo": evento.get("subtipo"),
                        "Latitud": evento.get("latitud"),
                        "Longitud": evento.get("longitud")
                    }
                    filas.append(fila)
        df = pd.DataFrame(filas)
        df.fillna('', inplace=True)
        
        # Usar la fecha actual para nombrar la carpeta
        date_str = datetime.now().strftime('%d-%m-%y')
        output_dir = f"{self.ruta_mac}/{date_str}"
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, nombre_archivo)
        df.to_csv(output_path, index=False)