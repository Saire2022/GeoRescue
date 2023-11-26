import folium
import requests
from geopy.geocoders import Nominatim
#Custom Class 'Point' and overload the + operator to combine two Point objects, resulting in a new Point object.

class Point:
    def __init__(self, date, point, lat, lon):
        self.date = date
        self.point = point
        self.lat = lat
        self.lon = lon

    def __add__(self, other):
        # Overload the '+' operator to create a new Point with combined information
        combined_date = f'{self.date} and {other.date}'
        combined_point = f'{self.point} and {other.point}'
        combined_lat = (self.lat + other.lat) / 2
        combined_lon = (self.lon + other.lon) / 2
        return Point(combined_date, combined_point, combined_lat, combined_lon)


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

# Function to draw points according to reques 
def get_points_and_draw_map(api_url):
    response = requests.get(api_url)

    if response.status_code == 200:
        puntos_data = response.json()['puntos']
        puntos_para_mapa = [(f'Date: {p["fecha"]}', f'Point: {p["id"]}', p['latitud'], p['longitud']) for p in puntos_data]
        print(puntos_para_mapa)
        Draw_Points(puntos_para_mapa)
    else:
        print(f'(Error {response.status_code}): {response.text}')

# Then you can call this function in your main code with the desired URL
#url = 'http://192.168.0.36:8080/obtener_puntos_por_usuario/1003818497'
#get_points_and_draw_map(url)



################# Idea de como graficar#######################33
print('Select the mode that you want to plot the point')
print('1.- By user')
print('2.- By an interval of time and user')
print('3.- All points')
option = input("Please, select one: ")
if int(option)==1:
    url = 'http://192.168.0.36:8080/obtener_puntos_por_usuario/'
    user_id=input("Please, put the id: ")
    full_url = url+user_id
    get_points_and_draw_map(full_url)
    #print(full_url)
elif int(option)==2:
    url = 'http://192.168.0.36:8080/obtener_puntos_por_rango_de_tiempo/'
    user_id=input("Please, put the id: ")
    url = url+user_id+"?start_time="
    date=input("Please, the start date (yy-mm-dd): ")
    url=url+date+"%20"
    hour_s=input("Please, the start hour (hh-mm-ss): ")
    url=url+hour_s+"&end_time="
    date_end=input("Please, the end date (yy-mm-dd): ")
    url=url+date_end+"%20"
    hour_end=input("Please, the end hour (hh-mm-ss): ")
    full_url=url+hour_end
    get_points_and_draw_map(full_url)
elif int(option)==3:
    url = 'http://192.168.0.36:8080/obtener_puntos'
    get_points_and_draw_map(url)





###########################
point1 = Point('Date1', 'Point1', 12.345, 67.890)
point2 = Point('Date2', 'Point2', 23.456, 78.901)

combined_point = point1 + point2
print(f'Combined Point: Date: {combined_point.date}, Point: {combined_point.point}, Lat: {combined_point.lat}, Lon: {combined_point.lon}')

