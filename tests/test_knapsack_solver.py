"""
Tests para el solver de knapsack
"""
import pytest
from app.services.knapsack_solver import KnapsackSolver, construir_base_exacta


class TestKnapsackSolver:
    def test_descomponer_binario_simple(self):
        """Test descomposición binaria básica"""
        partes = KnapsackSolver.descomponer_binario(100, 7)
        assert sum(partes) == 7
        assert 1 in partes
        assert 2 in partes
        assert 4 in partes

    def test_descomponer_binario_power_of_2(self):
        """Test con potencia de 2"""
        partes = KnapsackSolver.descomponer_binario(50, 8)
        assert sum(partes) == 8
        assert partes == [1, 2, 4, 1]

    def test_resolver_base_exacta(self):
        """Test resolver knapsack con solución exacta"""
        solver = KnapsackSolver(objetivo=450000, umbral_menudo=10000)

        todas_denoms = {
            2000: 50,
            5000: 20,
            10000: 30,
            20000: 15,
            50000: 10,
            100000: 5
        }

        conteo_base, conteo_consignar, restante, exacto = solver.resolver(todas_denoms)

        # Verificar que se alcanzó el objetivo
        total_base = sum(d * c for d, c in conteo_base.items())
        assert total_base <= 450000
        assert restante >= 0

        # Verificar que base + consignar = todas_denoms
        for denom in todas_denoms:
            assert conteo_base[denom] + conteo_consignar[denom] == todas_denoms[denom]

    def test_resolver_sin_suficiente_efectivo(self):
        """Test cuando no hay suficiente efectivo para la base"""
        solver = KnapsackSolver(objetivo=450000, umbral_menudo=10000)

        todas_denoms = {
            2000: 10,
            5000: 5,
            10000: 2
        }

        conteo_base, conteo_consignar, restante, exacto = solver.resolver(todas_denoms)

        total_base = sum(d * c for d, c in conteo_base.items())
        assert total_base < 450000
        assert exacto is False
        assert restante > 0


class TestConstruirBaseExacta:
    """Tests de la función helper"""

    def test_construir_base_exacta_function(self):
        """Test de la función wrapper"""
        todas_denoms = {
            2000: 100,
            5000: 50,
            10000: 40,
            20000: 20,
            50000: 10,
            100000: 5
        }

        conteo_base, conteo_consignar, restante, exacto = construir_base_exacta(
            todas_denoms,
            monto_objetivo=450000,
            umbral_menudo=10000
        )

        total_base = sum(d * c for d, c in conteo_base.items())
        assert total_base <= 450000

        # Verificar conservación de cantidades
        for denom in todas_denoms:
            assert conteo_base[denom] + conteo_consignar[denom] == todas_denoms[denom]
