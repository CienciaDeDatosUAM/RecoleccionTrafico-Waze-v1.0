import os
from datetime import datetime
from cuadrantes_CDMX import GraficarCDMX
from recoleccion_waze import WazeAPI
from filtrar_waze import FiltrarDatosJson
from filtrar_datos import FiltrarDatosExcel
import dotenv #Se debe agregar esta libreria para poder utilizar el archivo .env
import strings

# Lee el archivo .env
dotenv.load_dotenv()
# Usar la fecha actual para nombrar la carpeta
date_str = datetime.now().strftime('%d-%m-%y')
ruta_mac = strings.ruta_mac
output_dir = f"{ruta_mac}/{date_str}"
os.makedirs(output_dir, exist_ok=True)

# Primero creo el mapa
mapa = GraficarCDMX(geojson_path= "cdmx.geojson")
mapa.crear_mapa(output_dir, n=16, color_cuadrantes='green')

# Obtengo los puntos de cada cuadrante
vertices_cuadrantes = mapa.obtener_vertices()
for i, vertices in enumerate(vertices_cuadrantes, 1):
    print(f"Cuadrante {i}: {vertices}")

cuadrantes_diccionario = {f'Cuadrante {i}': vertices for i, vertices in enumerate(vertices_cuadrantes, 1)}

# Crear una instancia de WazeAPI con los vértices de los cuadrantes
waze_api = WazeAPI(cuadrantes_diccionario)
# Realizar la petición a la API de Waze
waze_api.realizar_peticion()

# Filtrar los datos JSON
filtrar = FiltrarDatosJson('datos')
nombre_datos_filtrados = filtrar.filtrar_datos()

# Guardar los datos filtrados en CSV
guardar_excel = FiltrarDatosExcel(nombre_datos_filtrados)
guardar_excel.guardar_en_csv()
