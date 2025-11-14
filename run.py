"""
Entry point para la aplicación Flask
"""
import os
from app import create_app
from app.config import get_config

# Determinar ambiente
config_name = os.getenv('FLASK_ENV', 'production')
config = get_config(config_name)

# Crear aplicación
app = create_app(config)

if __name__ == "__main__":
    # Configuración para desarrollo local
    port = int(os.getenv('PORT', 5000))
    debug = config.DEBUG

    app.logger.info(f"Iniciando servidor en puerto {port}")
    app.logger.info(f"Modo debug: {debug}")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug
    )
