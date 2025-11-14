"""
Tests para utilidades de formateo
"""
import pytest
from app.utils.formatters import (
    safe_int,
    safe_number,
    format_cop,
    normalize_payment_method,
    get_payment_method_label
)


class TestSafeInt:
    def test_safe_int_with_integer(self):
        assert safe_int(42) == 42

    def test_safe_int_with_string(self):
        assert safe_int("42") == 42

    def test_safe_int_with_float_string(self):
        assert safe_int("42.7") == 42

    def test_safe_int_with_invalid(self):
        assert safe_int("invalid") == 0

    def test_safe_int_with_none(self):
        assert safe_int(None) == 0


class TestSafeNumber:
    def test_safe_number_with_integer(self):
        assert safe_number(42) == 42

    def test_safe_number_with_float(self):
        assert safe_number(42.5) == 42.5

    def test_safe_number_with_string_with_commas(self):
        assert safe_number("1,234,567") == 1234567

    def test_safe_number_with_decimal_string(self):
        assert safe_number("123.45") == 123.45

    def test_safe_number_with_none(self):
        assert safe_number(None) == 0


class TestFormatCOP:
    def test_format_cop_basic(self):
        assert format_cop(450000) == "$450.000"

    def test_format_cop_millions(self):
        assert format_cop(1234567) == "$1.234.567"

    def test_format_cop_with_decimals(self):
        assert format_cop(450000.75) == "$450.001"

    def test_format_cop_zero(self):
        assert format_cop(0) == "$0"


class TestNormalizePaymentMethod:
    def test_normalize_credit_card(self):
        assert normalize_payment_method("Tarjeta de crédito") == "credit-card"
        assert normalize_payment_method("credit card") == "credit-card"

    def test_normalize_debit_card(self):
        assert normalize_payment_method("Tarjeta débito") == "debit-card"
        assert normalize_payment_method("debit") == "debit-card"

    def test_normalize_transfer(self):
        assert normalize_payment_method("Transferencia") == "transfer"
        assert normalize_payment_method("transfer") == "transfer"

    def test_normalize_cash(self):
        assert normalize_payment_method("Efectivo") == "cash"
        assert normalize_payment_method("cash") == "cash"

    def test_normalize_unknown(self):
        assert normalize_payment_method("Bitcoin") == "other"

    def test_normalize_empty(self):
        assert normalize_payment_method("") == "other"


class TestGetPaymentMethodLabel:
    def test_get_label_credit_card(self):
        assert get_payment_method_label("credit-card") == "Tarjeta crédito"

    def test_get_label_cash(self):
        assert get_payment_method_label("cash") == "Efectivo"

    def test_get_label_unknown(self):
        assert get_payment_method_label("bitcoin") == "bitcoin"
