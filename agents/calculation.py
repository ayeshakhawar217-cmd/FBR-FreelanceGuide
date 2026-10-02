from utils.calculator import calculate_export_tax
from utils.schemas import FreelancerProfile


def calculate_freelancer_tax(
    profile: FreelancerProfile,
    tax_rate_percent: float,
) -> dict:
    """
    Calculate tax deterministically using the tax rate selected
    from FBR source evidence.

    tax_rate_percent is expressed as a percentage.
    Example:
        0.25 means 0.25%
        1.0 means 1%
    """

    if profile.annual_income is None:
        raise ValueError("Annual income is required for calculation.")

    if profile.currency != "PKR":
        raise ValueError("Currently only PKR income is supported.")

    if tax_rate_percent <= 0:
        raise ValueError("Tax rate must be greater than zero.")

    return calculate_export_tax(
        annual_income=profile.annual_income,
        tax_rate=tax_rate_percent,
    )

