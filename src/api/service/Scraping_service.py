import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from bson import ObjectId

def scrape_and_store(url):
    """
    Realiza el scraping de la URL proporcionada, extrae los nombres y lugares,
    y guarda los datos en MongoDB.

    :param url: URL de la página web a procesar
    :return: Inserted ID (como string), nombres y lugares extraídos
    """
    try:
        # Realizar la solicitud HTTP
        result = requests.get(url)
        result.raise_for_status()  # Lanza una excepción si la respuesta HTTP no es exitosa
        conte = result.text

        # Usar BeautifulSoup para analizar el contenido
        soup = BeautifulSoup(conte, "lxml")

        # Buscar los párrafos que contienen los nombres y lugares
        parrafos = soup.find_all("p")

        # Extraer los nombres capturados
        parrafo_nombres = None
        for p in parrafos:
            if "Durante el operativo se capturó" in p.get_text():
                parrafo_nombres = p
                break

        nombres = []
        if parrafo_nombres:
            texto = parrafo_nombres.get_text(separator=" ", strip=True)
            texto_nombres = texto.split("En la diligencia")[0].replace("Durante el operativo se capturó a:", "").strip()
            nombres = [nombre.strip() for nombre in texto_nombres.split(",")]

        # Extraer los lugares del operativo
        parrafo_lugares = None
        for p in parrafos:
            if "El procedimiento se realizó en" in p.get_text():
                parrafo_lugares = p
                break

        lugares = []
        if parrafo_lugares:
            texto = parrafo_lugares.get_text(separator=" ", strip=True)
            texto_lugares = texto.split("De acuerdo con")[0].replace("El procedimiento se realizó en", "").strip()
            lugares = [lugar.strip() for lugar in texto_lugares.split(",")]

        # Preparar la información para guardar en MongoDB
        scraping_data = {
            "url": url,
            "nombres_capturados": nombres,
            "lugares_operativo": lugares
        }

        # Conectar a MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client["ListasNegras"]
        collection = db["listas-internas"]

        # Insertar los datos en MongoDB
        insert_result = collection.insert_one(scraping_data)

        # Retornar el ID insertado como string, los nombres y lugares extraídos
        return str(insert_result.inserted_id), nombres, lugares

    except requests.exceptions.RequestException as e:
        # Manejo de errores en la solicitud HTTP
        print(f"Error al hacer la solicitud HTTP: {e}")
        return None, [], []

    except Exception as e:
        # Manejo de errores generales
        print(f"Error al procesar los datos: {e}")
        return None, [], []
