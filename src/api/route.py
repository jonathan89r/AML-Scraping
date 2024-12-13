from flask import Blueprint, request, jsonify
from src.api.service.Scraping_service import scrape_and_store

scraping_bp = Blueprint('scraping', __name__)

@scraping_bp.route('/scrape', methods=['POST'])
def scrape_information():
    # Obtener el JSON de la solicitud
    data = request.get_json()

    # Verificar si 'uri' está presente en el JSON
    if not data or 'uri' not in data:
        return jsonify({"error": "Se requiere el campo 'uri' en el JSON"}), 400

    # Obtener la URL del campo 'uri'
    uri = data['uri']

    # Llamar al método de scraping en el servicio y pasar la URL
    try:
        # Llamamos al servicio, el cual hace todo el scraping y el guardado en la base de datos
        result = scrape_and_store(uri)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500