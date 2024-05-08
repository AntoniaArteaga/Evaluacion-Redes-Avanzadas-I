import requests

route = "https://graphhopper.com/api/1/route"
clave = "a25cfe59-6dbd-47fe-83a1-05269283fd7b"

# Mapear las opciones de transporte en español a inglés
opciones_transportes = {
    "auto": "car",
    "bicicleta": "bike",
    "a pie": "foot"
}

def obtener_geolocalizacion(location):
    url = f"https://graphhopper.com/api/1/geocode?q={location}&limit=1&key={clave}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["hits"][0]["name"], data["hits"][0].get("state", ""), data["hits"][0].get("city", ""), data["hits"][0]["point"]["lat"], data["hits"][0]["point"]["lng"]
    return None, None, None, None, None

def calcular_ruta(partida, destino, vehicle):
    partida_nombre, _, _, partida_lat, partida_lng = obtener_geolocalizacion(partida)
    destino_nombre, _, _, destino_lat, destino_lng = obtener_geolocalizacion(destino)
    if not partida_nombre or not destino_nombre:
        print("Error al obtener las ubicaciones.")
        return

    url = f"https://graphhopper.com/api/1/route?point={partida_lat},{partida_lng}&point={destino_lat},{destino_lng}&vehicle={vehicle}&key={clave}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        distancia_km = data['paths'][0]['distance'] / 1000
        distancia_millas = distancia_km * 0.621371
        tiempo_segundos = data['paths'][0]['time'] / 1000
        horas = int(tiempo_segundos // 3600)
        minutos = int((tiempo_segundos % 3600) // 60)
        segundos = int(tiempo_segundos % 60)
        print(f"Distancia: {distancia_km:.2f} Km ({distancia_millas:.2f} Millas)")
        print(f"Tiempo aproximado estimado: {horas:02d}:{minutos:02d}:{segundos:02d} (h:m:s)")
    else:
        print("Error al calcular la ruta.")

def main():
    while True:
        print("\nMenu principal:")
        print("1. Obtener geolocalizacion")
        print("2. Calcular ruta")
        print("3. Salir")
        choice = input("Ingrese una opcion: ")

        if choice == "1":
            location = input("Ingrese una ubicacion: ")
            nombre, region, ciudad, lat, lng = obtener_geolocalizacion(location)
            if nombre:
                print("Informacion de la ubicacion:")
                print(f"Ciudad: {nombre}")
                print(f"Region: {region}")
                print(f"Pais: {ciudad}")
                print(f"Latitud: {lat}")
                print(f"Longitud: {lng}")
            else:
                print("Error al obtener la ubicacion.")

        elif choice == "2":
            partida = input("Ubicacion de partida: ")
            destino = input("Ubicacion destino: ")
            # Pedir al usuario que seleccione un medio de transporte en español
            transporte = input("Seleccione el medio de transporte (auto, bicicleta, a pie): ").lower()
            # Convertir la opción del usuario al equivalente en inglés utilizando el diccionario
            vehicle = opciones_transportes.get(transporte)
            if vehicle:
                calcular_ruta(partida, destino, vehicle)
            else:
                print("Por favor seleccione un medio de transporte válido.")

        elif choice == "3":
            print("Salir del programa")
            break

        else:
            print("Opcion invalida. Intente nuevamente")

if __name__ == "__main__":
    main()