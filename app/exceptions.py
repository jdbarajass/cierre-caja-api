"""
Excepciones custom para la aplicación
"""
from flask import jsonify
from werkzeug.exceptions import HTTPException
import logging

logger = logging.getLogger(__name__)


class CierreCajaException(Exception):
    """Excepción base para errores del sistema de cierre de caja"""

    def __init__(self, message, status_code=500, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        rv['status_code'] = self.status_code
        return rv


class AlegraConnectionError(CierreCajaException):
    """Error al conectar con la API de Alegra"""

    def __init__(self, message="Error al conectar con Alegra", details=None):
        payload = {'service': 'alegra'}
        if details:
            payload['details'] = details
        super().__init__(message, status_code=502, payload=payload)


class AlegraAuthError(CierreCajaException):
    """Error de autenticación con Alegra"""

    def __init__(self, message="Credenciales de Alegra inválidas"):
        super().__init__(
            message,
            status_code=500,
            payload={'service': 'alegra', 'type': 'authentication'}
        )


class AlegraTimeoutError(CierreCajaException):
    """Timeout al conectar con Alegra"""

    def __init__(self, message="Timeout al conectar con Alegra"):
        super().__init__(
            message,
            status_code=504,
            payload={'service': 'alegra', 'type': 'timeout'}
        )


class ValidationError(CierreCajaException):
    """Error de validación de datos"""

    def __init__(self, message, field=None):
        payload = {'type': 'validation'}
        if field:
            payload['field'] = field
        super().__init__(message, status_code=400, payload=payload)


class ConfigurationError(CierreCajaException):
    """Error de configuración del sistema"""

    def __init__(self, message):
        super().__init__(
            message,
            status_code=500,
            payload={'type': 'configuration'}
        )


class CalculationError(CierreCajaException):
    """Error en cálculos de cierre de caja"""

    def __init__(self, message, calculation_type=None):
        payload = {'type': 'calculation'}
        if calculation_type:
            payload['calculation_type'] = calculation_type
        super().__init__(message, status_code=500, payload=payload)


def setup_error_handlers(app):
    """
    Configura los manejadores de errores para la aplicación

    Args:
        app: Instancia de Flask
    """

    @app.errorhandler(CierreCajaException)
    def handle_cierre_caja_exception(error):
        """Maneja excepciones custom de cierre de caja"""
        logger.error(f"CierreCajaException: {error.message}", extra={
            'status_code': error.status_code,
            'payload': error.payload
        })
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Maneja excepciones HTTP de Werkzeug"""
        logger.warning(f"HTTPException: {error.description}", extra={
            'status_code': error.code
        })
        response = jsonify({
            'error': error.description,
            'status_code': error.code
        })
        response.status_code = error.code
        return response

    @app.errorhandler(404)
    def handle_not_found(error):
        """Maneja errores 404"""
        return jsonify({
            'error': 'Endpoint no encontrado',
            'status_code': 404
        }), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Maneja errores 405"""
        return jsonify({
            'error': 'Método HTTP no permitido',
            'status_code': 405
        }), 405

    @app.errorhandler(500)
    def handle_internal_error(error):
        """Maneja errores internos 500"""
        logger.error(f"Error interno del servidor: {str(error)}", exc_info=True)
        return jsonify({
            'error': 'Error interno del servidor',
            'status_code': 500
        }), 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Maneja errores inesperados"""
        logger.error(f"Error inesperado: {str(error)}", exc_info=True)
        return jsonify({
            'error': 'Error inesperado en el servidor',
            'status_code': 500,
            'type': type(error).__name__
        }), 500
