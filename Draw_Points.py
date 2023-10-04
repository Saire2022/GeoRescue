import folium
import requests
from geopy.geocoders import Nominatim

def Draw_Points(list_points):
    """Draws points on a map."""
    if not list_points:
        print("The list of points is empty.")
        return
    # Calculate the maximum and minimum latitude and longitude coordinates
    min_lat = min(float(point[2]) for point in list_points)
    max_lat = max(float(point[2]) for point in list_points)
    min_lon = min(float(point[3]) for point in list_points)
    max_lon = max(float(point[3]) for point in list_points)

    # Calculate the center of the coordinates
    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2

    # Create the map centered at the calculated coordinates
    map = folium.Map(location=[center_lat, center_lon], zoom_start=10)
    for point in list_points:
        map.add_child(folium.Marker([point[2], point[3]], popup=(str(point[0]),str(point[1]),f'Lat: {str(point[2])}',f'Lng: {str(point[3])}')))
    map.save("Map_Points.html")

# URL de la API
api_url = 'http://192.168.0.14:5000/obtener_puntos?usuario_id=1050440799'

response = requests.get(api_url)

if response.status_code == 200:
    puntos_data = response.json()['puntos']
    puntos_para_mapa = [(f'Date: {p["fecha"]}',f'Point: {p["id"]}', p['latitud'], p['longitud']) for p in puntos_data]
    print(puntos_para_mapa)
    Draw_Points(puntos_para_mapa)
else:
    print('Error al obtener la lista de puntos:', response.status_code)
