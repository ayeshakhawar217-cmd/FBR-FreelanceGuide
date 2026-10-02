from decimal import Decimal, ROUND_HALF_UP


def calculate_export_tax(
    annual_income: float,
    tax_rate: float,
) -> dict:
    """
    Deterministic tax calculation.

    annual_income: gross annual export proceeds in PKR
    tax_rate: percentage rate, e.g. 0.25 for 0.25%
    """

    income = Decimal(str(annual_income))
    rate = Decimal(str(tax_rate)) / Decimal("100")

    tax = (income * rate).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    effective_rate = (
        (tax / income) * Decimal("100")
        if income > 0
        else Decimal("0")
    )

    return {
        "annual_income": float(income),
        "tax_rate": float(tax_rate),
        "tax_amount": float(tax),
        "effective_rate": float(effective_rate),
    }