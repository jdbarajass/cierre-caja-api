"""
Cliente para la API de Alegra
"""
import requests
from requests.auth import HTTPBasicAuth
from typing import Dict, List
import logging

from app.exceptions import (
    AlegraConnectionError,
    AlegraAuthError,
    AlegraTimeoutError
)
from app.utils.formatters import (
    safe_number,
    normalize_payment_method,
    get_payment_method_label,
    format_cop
)

logger = logging.getLogger(__name__)


class AlegraClient:
    """Cliente para interactuar con la API de Alegra"""

    def __init__(self, username: str, password: str, base_url: str, timeout: int = 30):
        """
        Inicializa el cliente de Alegra

        Args:
            username: Usuario de Alegra
            password: Token/Password de Alegra
            base_url: URL base de la API
            timeout: Timeout en segundos para las peticiones
        """
        self.username = username
        self.password = password
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(username, password)

        # Headers comunes
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

        logger.info(f"Cliente Alegra inicializado para usuario: {username}")

    def get_invoices_by_date(self, date: str) -> List[Dict]:
        """
        Obtiene las facturas de Alegra para una fecha específica

        Args:
            date: Fecha en formato YYYY-MM-DD

        Returns:
            Lista de facturas

        Raises:
            AlegraTimeoutError: Si la petición excede el timeout
            AlegraAuthError: Si las credenciales son inválidas
            AlegraConnectionError: Para otros errores de conexión
        """
        url = f"{self.base_url}/invoices"
        params = {
            "date": date
        }

        logger.info(f"Consultando facturas de Alegra para fecha: {date}")

        try:
            response = self.session.get(
                url,
                params=params,
                timeout=self.timeout
            )

            # Log del status
            logger.debug(f"Alegra response status: {response.status_code}")

            # Manejar diferentes status codes
            if response.status_code == 401:
                logger.error("Credenciales de Alegra inválidas (401)")
                raise AlegraAuthError("Credenciales de Alegra inválidas")

            if response.status_code == 403:
                logger.error("Acceso prohibido a Alegra (403)")
                raise AlegraAuthError("Acceso prohibido. Verifique permisos de la cuenta")

            if response.status_code == 404:
                logger.warning(f"Endpoint no encontrado en Alegra (404): {url}")
                raise AlegraConnectionError(
                    "Endpoint no encontrado en Alegra",
                    details={'url': url}
                )

            if response.status_code >= 500:
                logger.error(f"Error del servidor de Alegra ({response.status_code})")
                raise AlegraConnectionError(
                    f"Error del servidor de Alegra (HTTP {response.status_code})",
                    details={'status_code': response.status_code}
                )

            # Intentar parsear JSON
            response.raise_for_status()
            data = response.json()

            # Validar que sea una lista
            if not isinstance(data, list):
                logger.warning(f"Respuesta de Alegra no es una lista: {type(data)}")
                data = []

            logger.info(f"✓ {len(data)} facturas obtenidas de Alegra para {date}")
            return data

        except requests.exceptions.Timeout:
            logger.error(f"Timeout al conectar con Alegra (>{self.timeout}s)")
            raise AlegraTimeoutError(
                f"Timeout al conectar con Alegra (>{self.timeout}s)"
            )

        except requests.exceptions.ConnectionError as e:
            logger.error(f"Error de conexión con Alegra: {str(e)}")
            raise AlegraConnectionError(
                "No se pudo conectar con Alegra. Verifique la conexión a internet",
                details={'error': str(e)}
            )

        except requests.exceptions.HTTPError as e:
            logger.error(f"Error HTTP de Alegra: {str(e)}")
            raise AlegraConnectionError(
                f"Error HTTP de Alegra: {e.response.status_code}",
                details={'error': str(e)}
            )

        except ValueError as e:
            logger.error(f"Error al parsear JSON de Alegra: {str(e)}")
            raise AlegraConnectionError(
                "Respuesta inválida de Alegra (JSON mal formado)",
                details={'error': str(e)}
            )

        except Exception as e:
            logger.error(f"Error inesperado con Alegra: {str(e)}", exc_info=True)
            raise AlegraConnectionError(
                f"Error inesperado al conectar con Alegra: {str(e)}",
                details={'error': str(e)}
            )

    def process_invoices(self, invoices: List[Dict]) -> Dict[str, float]:
        """
        Procesa facturas y suma totales por método de pago

        Args:
            invoices: Lista de facturas de Alegra

        Returns:
            Dict con totales por método: {"credit-card": X, "debit-card": Y, ...}
        """
        totals = {
            "credit-card": 0,
            "debit-card": 0,
            "transfer": 0,
            "cash": 0
        }

        for inv in invoices:
            payments = inv.get("payments", []) or []

            for p in payments:
                amount = safe_number(p.get("amount", 0))
                pm_raw = p.get("paymentMethod", "")
                method = normalize_payment_method(pm_raw)

                if method in totals:
                    totals[method] += amount
                else:
                    # Métodos desconocidos van a 'cash' por defecto
                    logger.debug(f"Método de pago desconocido '{pm_raw}' mapeado a 'cash'")
                    totals["cash"] += amount

        logger.debug(f"Totales procesados: {totals}")
        return totals

    def build_alegra_response(
        self,
        totals: Dict[str, float],
        date: str,
        username: str
    ) -> Dict:
        """
        Construye la estructura de respuesta de Alegra

        Args:
            totals: Diccionario con totales por método de pago
            date: Fecha consultada
            username: Usuario utilizado

        Returns:
            Dict con estructura completa de respuesta
        """
        result = {}

        for method, total in totals.items():
            result[method] = {
                "label": get_payment_method_label(method),
                "total": int(total),
                "formatted": format_cop(total)
            }

        total_sum = sum(totals.values())
        result_total = {
            "label": "TOTAL VENTA DEL DÍA",
            "total": int(total_sum),
            "formatted": format_cop(total_sum)
        }

        return {
            "date_requested": date,
            "username_used": username,
            "results": result,
            "total_sale": result_total
        }

    def get_sales_summary(self, date: str) -> Dict:
        """
        Obtiene el resumen completo de ventas para una fecha

        Args:
            date: Fecha en formato YYYY-MM-DD

        Returns:
            Diccionario con resumen completo de ventas
        """
        invoices = self.get_invoices_by_date(date)
        totals = self.process_invoices(invoices)
        return self.build_alegra_response(totals, date, self.username)

    def health_check(self) -> bool:
        """
        Verifica si el servicio de Alegra está disponible

        Returns:
            True si está disponible, False en caso contrario
        """
        try:
            url = f"{self.base_url}/categories"  # Endpoint ligero para health check
            response = self.session.get(url, timeout=5)
            return response.status_code in [200, 401]  # 401 significa que API responde
        except Exception:
            return False
