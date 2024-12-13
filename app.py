import time
from flask import Flask
from flask_cors import CORS
from src.api.route import scraping_bp  # Asegúrate de importar el blueprint correctamente

# Crear la aplicación Flask
app = Flask(__name__)

# Habilitar CORS para todas las solicitudes
CORS(app, origins='*')

# Registrar el blueprint para las rutas de scraping
app.register_blueprint(scraping_bp, url_prefix='/api/v1')

# Iniciar la aplicación en modo debug
if __name__ == '__main__':
    app.run(debug=True)
