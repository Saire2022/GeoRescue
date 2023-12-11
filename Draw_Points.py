import folium
import requests

class Point:
    def __init__(self, date, point, lat, lon):
        self.date = date
        self.point = point
        self.lat = lat
        self.lon = lon

    def __add__(self, other):
        combined_date = f'{self.date} and {other.date}'
        combined_point = f'{self.point} and {other.point}'
        combined_lat = (self.lat + other.lat) / 2
        combined_lon = (self.lon + other.lon) / 2
        return Point(combined_date, combined_point, combined_lat, combined_lon)

def Draw_Points(list_points):
    if not list_points:
        print("The list of points is empty.")
        return
    print(f"Number of points: {len(list_points)}")

    min_lat = min(float(point[2]) for point in list_points)
    max_lat = max(float(point[2]) for point in list_points)
    min_lon = min(float(point[3]) for point in list_points)
    max_lon = max(float(point[3]) for point in list_points)

    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2

    map = folium.Map(location=[center_lat, center_lon], zoom_start=20)
    for point in list_points:
        map.add_child(folium.Marker([point[2], point[3]], popup=(str(point[0]), str(point[1]), f'Lat: {str(point[2])}', f'Lng: {str(point[3])}')))
    map.save("Map_Points.html")

def Draw_Points_Route(list_points):
    if not list_points:
        print("The list of points is empty.")
        return
    print(f"Number of points: {len(list_points)}")

    min_lat = min(point["coords"][0] for point in list_points)
    max_lat = max(point["coords"][0] for point in list_points)
    min_lon = min(point["coords"][1] for point in list_points)
    max_lon = max(point["coords"][1] for point in list_points)

    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2

    map = folium.Map(location=[center_lat, center_lon], zoom_start=20)

    route_coords = [point["coords"] for point in list_points]

    folium.PolyLine(locations=route_coords, color='blue').add_to(map)

    for index, point in enumerate(list_points):
        popup_text = f"{point['label']}\nLat: {point['coords'][0]}, Lng: {point['coords'][1]}"
        marker_color = 'red' if index == 0 else 'green' if index == len(list_points) - 1 else 'blue'
        icon_type = 'arrow-up' if index == 0 else 'arrow-down' if index == len(list_points) - 1 else 'none'

        if index == 0 or index == len(list_points) - 1:
            folium.Marker(location=point["coords"], icon=folium.Icon(color=marker_color, icon=icon_type), popup=popup_text).add_to(map)
        else:
            map.add_child(folium.Marker(point["coords"], popup=popup_text))

    map.save("Map_Points_with_Route.html")

def draw_map_points(api_url, headers):
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        puntos_data = response.json()['puntos']
        puntos_para_mapa = [(f'Date: {p["fecha"]}', f'Point: {p["id"]}', p['latitud'], p['longitud']) for p in puntos_data]

        points = [{"coords": [float(punto['latitud']), float(punto['longitud'])], "label": punto['fecha']} for punto in puntos_data]

        Draw_Points(puntos_para_mapa)
    else:
        print(f'(Error {response.status_code}): {response.text}')

def draw_map_points_route(api_url, headers):
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        puntos_data = response.json()['puntos']
        puntos_para_mapa = [(f'Date: {p["fecha"]}', f'Point: {p["id"]}', p['latitud'], p['longitud']) for p in puntos_data]

        points = [{"coords": [float(punto['latitud']), float(punto['longitud'])], "label": punto['fecha']} for punto in puntos_data]

        Draw_Points_Route(points)
    else:
        print(f'(Error {response.status_code}): {response.text}')

def main():
    # Get user credentials
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Log in and get the token
    token_url = 'http://127.0.0.1:5000/login'
    credentials = {'username': username, 'password': password}

    # Incluye el encabezado Content-Type: application/json en la solicitud POST
    token_response = requests.post(token_url, json=credentials, headers={'Content-Type': 'application/json'})

    if token_response.status_code == 200:
        token = token_response.json()['access_token']
        headers = {"Authorization": f"Bearer {token}"}

        # Menu
        print('Select the mode that you want to plot the point')
        print('1.- By user')
        print('2.- By an interval of time and user')
        print('3.- All points')
        option = input("Please, select one: ")
        Route = input("Draw points with Route? (Y/N):")

        if int(option) == 1:
            url = 'http://127.0.0.1:5000/obtener_puntos_por_usuario/'
            while True:
                try:
                    user_id = input("Please, put the id: ")
                    response = requests.get(url + user_id, headers=headers)
                    response.raise_for_status()
                except requests.exceptions.HTTPError as errh:
                    print("User ID not found in the database. Please try again with another ID.")
                except Exception as err:
                    print("An unexpected error occurred.")
                else:
                    full_url = url + user_id
                    if Route.lower() == 'y' or '':
                        draw_map_points_route(full_url, headers)
                    else:
                        draw_map_points(full_url, headers)
                    break

        elif int(option) == 2:
            url = 'http://127.0.0.1:5000/obtener_puntos_por_rango_de_tiempo/'
            user_id = input("Please, put the id: ")
            url = url + user_id + "?start_time="
            date = input("Please, the start date (yy-mm-dd): ")
            url = url + date + "%20"
            hour_s = input("Please, the start hour (hh:mm:ss): ")
            url = url + hour_s + "&end_time="
            date_end = input("Please, the end date (yy:mm:dd): ")
            url = url + date_end + "%20"
            hour_end = input("Please, the end hour (hh:mm:ss): ")
            full_url = url + hour_end
            if Route.lower() == 'y' or '':
                draw_map_points_route(full_url, headers)
            else:
                draw_map_points(full_url, headers)

        elif int(option) == 3:
            url = 'http://127.0.0.1:5000/obtener_puntos'
            if Route.lower() == 'y':
                draw_map_points_route(url, headers)
            else:
                draw_map_points(url, headers)

    else:
        print(f'(Error {token_response.status_code}): {token_response.text}')

if __name__ == "__main__":
    main()
