import folium
import json
from shapely.geometry import shape, box

class GraficarCDMX:
    def __init__(self, geojson_path, nombre_archivo="mapa_cdmx.html"):
        self.geojson_path = geojson_path
        self.nombre_archivo = nombre_archivo
        self.puntos = self.crear_puntos()
        self.min_lat, self.max_lat = min([p[1] for p in self.puntos]), max([p[1] for p in self.puntos])
        self.min_lon, self.max_lon = min([p[0] for p in self.puntos]), max([p[0] for p in self.puntos])
        self.centro = ((self.min_lat + self.max_lat) / 2, (self.min_lon + self.max_lon) / 2)

    def crear_puntos(self):
        # Cargar el archivo GeoJSON
        with open(self.geojson_path, 'r') as f:
            geojson_data = json.load(f)

        puntos = []
        for feature in geojson_data['features']:
            coords = feature['geometry']['coordinates']
            # Asegurémonos de manejar tanto Polígonos como MultiPolígonos
            if feature['geometry']['type'] == 'Polygon':
                for point in coords[0]:
                    lon, lat = point
                    puntos.append((lon, lat))
            elif feature['geometry']['type'] == 'MultiPolygon':
                for polygon in coords:
                    for point in polygon[0]:
                        lon, lat = point
                        puntos.append((lon, lat))
        return puntos

    def dividir_area(self, n):
        cuadrantes = []
        puntos_cuadrantes = []
        lat_step = (self.max_lat - self.min_lat) / n
        lon_step = (self.max_lon - self.min_lon) / n
        for i in range(n):
            for j in range(n):
                min_x, min_y = self.min_lon + j * lon_step, self.min_lat + i * lat_step
                max_x, max_y = self.min_lon + (j + 1) * lon_step, self.min_lat + (i + 1) * lat_step
                cuadrante = box(min_x, min_y, max_x, max_y)
                cuadrantes.append(cuadrante)
                puntos_cuadrantes.append([(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)])
        return cuadrantes, puntos_cuadrantes

    def crear_mapa(self, output_dir='.', n=16, color_cuadrantes='blue'):
        cuadrantes, vertices_cuadrantes = self.dividir_area(n)
        geojson_data = self.cargar_geojson()
        m = folium.Map(location=self.centro, zoom_start=12)

        # Agregar el GeoJSON original al mapa
        folium.GeoJson(geojson_data).add_to(m)

        # Agregar los cuadrantes al mapa
        for i, cuadrante in enumerate(cuadrantes, 1):
            folium.GeoJson(
                data=cuadrante.__geo_interface__,
                style_function=lambda x: {'color': color_cuadrantes},
                tooltip=f"Cuadrante {i}"
            ).add_to(m)

        self.vertices_guardados = vertices_cuadrantes
        m.save(f"{output_dir}/{self.nombre_archivo}")
        print(f"Mapa guardado en {output_dir}/{self.nombre_archivo}")

    def cargar_geojson(self):
        with open(self.geojson_path, 'r') as f:
            return json.load(f)

    def obtener_vertices(self):
        return self.vertices_guardados

