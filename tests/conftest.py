"""
Configuración de pytest
"""
import pytest
import sys
import os

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def app():
    """Fixture para la aplicación Flask"""
    from app import create_app
    from app.config import TestingConfig

    app = create_app(TestingConfig)
    return app


@pytest.fixture
def client(app):
    """Fixture para el cliente de pruebas"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Fixture para el runner CLI"""
    return app.test_cli_runner()
