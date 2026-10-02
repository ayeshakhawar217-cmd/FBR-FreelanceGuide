from typing import Optional, List
from pydantic import BaseModel, Field


class FreelancerProfile(BaseModel):
    profession: Optional[str] = None
    service_category: Optional[str] = None

    client_location: Optional[str] = None
    income_source: Optional[str] = None
    platform: Optional[str] = None

    # Income details
    annual_income: Optional[float] = None
    monthly_income: Optional[float] = None
    currency: Optional[str] = None

    # Freelance-specific facts
    pseb_registered: Optional[bool] = None
    pseb_certification_valid: Optional[bool] = None
    return_filed: Optional[bool] = None

    # Payment details
    payment_channels: List[str] = Field(default_factory=list)
    foreign_currency_received: Optional[bool] = None
    received_in_pakistani_bank: Optional[bool] = None

    # Other income mentioned by the user
    other_income_sources: List[str] = Field(default_factory=list)

    # Facts that require confirmation
    uncertain_facts: List[str] = Field(default_factory=list)

    # Facts needed before calculation
    missing_information: List[str] = Field(default_factory=list)