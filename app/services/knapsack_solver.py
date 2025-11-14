"""
Servicio de resolución de problemas Knapsack
Algoritmo de programación dinámica para calcular la base exacta de caja
"""
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class KnapsackSolver:
    """
    Resolvedor de problemas Knapsack usando programación dinámica
    con descomposición binaria para optimizar la búsqueda
    """

    def __init__(self, objetivo: int, umbral_menudo: int):
        """
        Inicializa el solver

        Args:
            objetivo: Monto objetivo a alcanzar (ej: 450000)
            umbral_menudo: Umbral para considerar denominación como menudo (ej: 10000)
        """
        self.objetivo = objetivo
        self.umbral_menudo = umbral_menudo
        self.NEG = -10**18  # Valor negativo para indicar estado imposible

    @staticmethod
    def descomponer_binario(valor: int, cantidad: int) -> list:
        """
        Descompone una cantidad en potencias de 2 para optimizar el knapsack

        Args:
            valor: Valor de la denominación
            cantidad: Cantidad de unidades disponibles

        Returns:
            Lista de potencias de 2 que suman la cantidad

        Ejemplo:
            >>> KnapsackSolver.descomponer_binario(100, 7)
            [1, 2, 4]  # 1+2+4 = 7
        """
        partes = []
        k = 1
        restante = cantidad

        while k <= restante:
            partes.append(k)
            restante -= k
            k *= 2

        if restante > 0:
            partes.append(restante)

        return partes

    def resolver(
        self,
        todas_denoms: Dict[int, int]
    ) -> Tuple[Dict[int, int], Dict[int, int], int, bool]:
        """
        Resuelve el problema de knapsack para encontrar la combinación exacta

        Args:
            todas_denoms: Diccionario {denominación: cantidad_disponible}

        Returns:
            Tupla con:
                - conteo_base: Dict {denominación: cantidad_usada_en_base}
                - conteo_consignar: Dict {denominación: cantidad_restante}
                - restante: Diferencia con el objetivo (0 si se alcanzó exacto)
                - exacto: True si se alcanzó el monto exacto

        Algoritmo:
            Bounded Knapsack con Dynamic Programming
            - Descomposición binaria para reducir complejidad
            - Maximiza denominaciones pequeñas (menudo) en la base
            - Busca combinación exacta del objetivo
        """
        MAX = self.objetivo
        NEG = self.NEG

        # Tabla DP: dp[s] = máximo aporte de menudo al llegar a suma s
        dp = [NEG] * (MAX + 1)
        dp[0] = 0

        # prev[s] guarda el estado previo para reconstruir la solución
        prev = [None] * (MAX + 1)

        # Preparar items con descomposición binaria
        items = []
        for denom, cnt in todas_denoms.items():
            if cnt <= 0:
                continue

            partes = self.descomponer_binario(denom, cnt)
            for k in partes:
                valor_total = denom * k
                # Aporte de menudo: si la denominación es <= umbral, cuenta
                aporte_menudo = valor_total if denom <= self.umbral_menudo else 0
                items.append((valor_total, aporte_menudo, denom, k))

        logger.debug(f"Items preparados: {len(items)} después de descomposición binaria")

        # DP: Procesar cada item
        for valor_total, aporte_menudo, denom, k in items:
            # Recorrer de atrás hacia adelante para evitar usar el mismo item múltiples veces
            for s in range(MAX, valor_total - 1, -1):
                if dp[s - valor_total] != NEG:
                    cand = dp[s - valor_total] + aporte_menudo
                    if cand > dp[s]:
                        dp[s] = cand
                        prev[s] = (s - valor_total, denom, k)

        # Caso 1: Se alcanzó el objetivo exacto
        if dp[MAX] != NEG:
            logger.info(f"✓ Base exacta alcanzada: ${MAX:,}")
            usado = self._reconstruir_solucion(prev, MAX)
            conteo_base = {d: usado.get(d, 0) for d in todas_denoms}
            conteo_consignar = {d: todas_denoms[d] - conteo_base[d] for d in todas_denoms}
            return conteo_base, conteo_consignar, 0, True

        # Caso 2: No se alcanzó exacto, buscar el más cercano
        mejor_s = -1
        for s in range(MAX, -1, -1):
            if dp[s] != NEG:
                mejor_s = s
                break

        if mejor_s == -1:
            # No se pudo formar ninguna combinación
            logger.warning("⚠ No se pudo formar ninguna base")
            conteo_base = {d: 0 for d in todas_denoms}
            conteo_consignar = dict(todas_denoms)
            restante = self.objetivo
            return conteo_base, conteo_consignar, restante, False

        # Reconstruir la mejor solución parcial
        logger.warning(f"⚠ Base inexacta: ${mejor_s:,} de ${MAX:,} (falta ${MAX - mejor_s:,})")
        usado = self._reconstruir_solucion(prev, mejor_s)
        conteo_base = {d: usado.get(d, 0) for d in todas_denoms}
        conteo_consignar = {d: todas_denoms[d] - conteo_base[d] for d in todas_denoms}
        restante = self.objetivo - mejor_s

        return conteo_base, conteo_consignar, restante, False

    def _reconstruir_solucion(self, prev: list, suma_final: int) -> Dict[int, int]:
        """
        Reconstruye la solución desde la tabla de backtracking

        Args:
            prev: Tabla de backtracking
            suma_final: Suma final alcanzada

        Returns:
            Dict {denominación: cantidad_usada}
        """
        usado = {}
        s = suma_final

        while s > 0:
            entry = prev[s]
            if entry is None:
                break

            s_prev, denom, k = entry
            usado[denom] = usado.get(denom, 0) + k
            s = s_prev

        return usado


def construir_base_exacta(
    todas_denoms: Dict[int, int],
    monto_objetivo: int,
    umbral_menudo: int
) -> Tuple[Dict[int, int], Dict[int, int], int, bool]:
    """
    Función helper para mantener compatibilidad con código legacy

    Args:
        todas_denoms: Diccionario {denominación: cantidad}
        monto_objetivo: Monto objetivo de la base
        umbral_menudo: Umbral para considerar menudo

    Returns:
        Tupla (conteo_base, conteo_consignar, restante, exacto)
    """
    solver = KnapsackSolver(monto_objetivo, umbral_menudo)
    return solver.resolver(todas_denoms)
