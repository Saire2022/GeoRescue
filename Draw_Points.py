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

###############################################################
#################""" Function to draw points"""################
###############################################################
def Draw_Points(list_points):
    """Draws points on a map."""
    if not list_points:
        print("The list of points is empty.")
        return
    print(f"Number of points: {len(list_points)}")
    # Calculate the maximum and minimum latitude and longitude coordinates
    min_lat = min(float(point[2]) for point in list_points)
    max_lat = max(float(point[2]) for point in list_points)
    min_lon = min(float(point[3]) for point in list_points)
    max_lon = max(float(point[3]) for point in list_points)

    # Calculate the center of the coordinates
    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2

    # Create the map centered at the calculated coordinates
    map = folium.Map(location=[center_lat, center_lon], zoom_start=20)
    for point in list_points:
        map.add_child(folium.Marker([point[2], point[3]], popup=(str(point[0]),str(point[1]),f'Lat: {str(point[2])}',f'Lng: {str(point[3])}')))
    map.save("Map_Points.html")

###############################################################################
#################""" Function to draw points and route """#####################
###############################################################################

def Draw_Points_Route(list_points):
    """Draws points and route on a map."""
    if not list_points:
        print("The list of points is empty.")
        return
    print(f"Number of points: {len(list_points)}")

    # Calculate the maximum and minimum latitude and longitude coordinates
    min_lat = min(point["coords"][0] for point in list_points)
    max_lat = max(point["coords"][0] for point in list_points)
    min_lon = min(point["coords"][1] for point in list_points)
    max_lon = max(point["coords"][1] for point in list_points)

    # Calculate the center of the coordinates
    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2

    # Create the map centered at the calculated coordinates
    map = folium.Map(location=[center_lat, center_lon], zoom_start=20)

    # Create a list of coordinates for the route
    route_coords = [point["coords"] for point in list_points]

    # Add a polyline for the route
    folium.PolyLine(locations=route_coords, color='blue').add_to(map)

    for index, point in enumerate(list_points):
        popup_text = f"{point['label']}\nLat: {point['coords'][0]}, Lng: {point['coords'][1]}"
        marker_color = 'red' if index == 0 else 'green' if index == len(list_points) - 1 else 'blue'
        icon_type = 'arrow-up' if index == 0 else 'arrow-down' if index == len(list_points) - 1 else 'none'

        # Add arrows for start and end points, regular markers for others
        if index == 0 or index == len(list_points) - 1:
            folium.Marker(location=point["coords"], icon=folium.Icon(color=marker_color, icon=icon_type), popup=popup_text).add_to(map)
        else:
            map.add_child(folium.Marker(point["coords"], popup=popup_text))

    map.save("Map_Points_with_Route.html")

############################################################################
############# Function to draw points according to request #################
############################################################################
def draw_map_points(api_url):
    # Get points data from the API
    response = requests.get(api_url)

    if response.status_code == 200:
        puntos_data = response.json()['puntos']
        # Prepare points data for mapping
        puntos_para_mapa = [(f'Date: {p["fecha"]}', f'Point: {p["id"]}', p['latitud'], p['longitud']) for p in puntos_data]
        
        # Prepare points in the required format for mapping
        points = []
        for punto in puntos_data:
            latitud = float(punto['latitud'])
            longitud = float(punto['longitud'])
            fecha = punto['fecha']
            punto_formato = {
                "coords": [latitud, longitud],
                "label": fecha
            }
            points.append(punto_formato)
        
        Draw_Points(puntos_para_mapa)
    else:
        print(f'(Error {response.status_code}): {response.text}')


############################################################################
########## Function to draw points and route according to request ##########
############################################################################

def draw_map_points_route(api_url):
    # Get points data from the API
    response = requests.get(api_url)

    if response.status_code == 200:
        # Extract points data from the JSON response
        puntos_data = response.json()['puntos']
        
        # Prepare points data for mapping
        puntos_para_mapa = [(f'Date: {p["fecha"]}', f'Point: {p["id"]}', p['latitud'], p['longitud']) for p in puntos_data]
        
        # Prepare points in the required format for mapping
        points = []
        for punto in puntos_data:
            latitud = float(punto['latitud'])
            longitud = float(punto['longitud'])
            fecha = punto['fecha']
            punto_formato = {
                "coords": [latitud, longitud],
                "label": fecha
            }
            points.append(punto_formato)

        # Call the function to draw points with a route on the map
        Draw_Points_Route(points)
    else:
        print(f'(Error {response.status_code}): {response.text}')


#Menu
print('Select the mode that you want to plot the point')
print('1.- By user')
print('2.- By an interval of time and user')
print('3.- All points')
option = input("Please, select one: ")
Route = input("Draw points with Route? (Y/N):")
#API Santiago:
#URL = 'https://apirest-qywgms5y2q-ue.a.run.app'

#API Saire:
URL = 'https://apirest-gwcceccumq-ue.a.run.app'

if int(option) == 1:
    url = URL + '/obtener_puntos_por_usuario/'
    while True:
        try:
            user_id = input("Please, put the id: ")
            # Validate if the user ID exists in the database
            response = requests.get(url + user_id)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            #print(f"Error: {errh}")
            print("User ID not found in the database. Please try again with another ID.")
        except Exception as err:
            print(f"Error: {err}")
            print("An unexpected error occurred.")
        else:
            full_url = url + user_id
            if Route.lower() == 'y' or '':
                draw_map_points_route(full_url)
            else:
                draw_map_points(full_url)
            break

elif int(option)==2:
    url = URL + '/obtener_puntos_por_rango_de_tiempo/'
    user_id=input("Please, put the id: ")
    url = url+user_id+"?start_time="
    date=input("Please, the start date (yy-mm-dd): ")
    url=url+date+"%20"
    hour_s=input("Please, the start hour (hh:mm:ss): ")
    url=url+hour_s+"&end_time="
    date_end=input("Please, the end date (yy:mm:dd): ")
    url=url+date_end+"%20"
    hour_end=input("Please, the end hour (hh:mm:ss): ")
    full_url=url+hour_end
    if Route.lower() == 'y' or '':
        draw_map_points_route(full_url)
    else:
        draw_map_points(full_url)
elif int(option)==3:
    url = URL + '/obtener_puntos'
    if(Route=='Y'):
        draw_map_points_route(url)
    else:
        draw_map_points(url)




###########################
point1 = Point('Date1', 'Point1', 12.345, 67.890)
point2 = Point('Date2', 'Point2', 23.456, 78.901)

combined_point = point1 + point2
print(f'Combined Point: Date: {combined_point.date}, Point: {combined_point.point}, Lat: {combined_point.lat}, Lon: {combined_point.lon}')

