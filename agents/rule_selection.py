from utils.groq_client import ask_groq
from utils.schemas import FreelancerProfile
import json


SYSTEM_PROMPT = """
You are the rule-selection agent for FBR FreelanceGuide.

Your job is to determine the applicable FBR tax treatment for the user's
FREELANCE income using ONLY the supplied FBR evidence.

You are NOT allowed to:
- calculate the tax amount
- invent a tax rate
- use outside knowledge
- assume a default rate
- convert currencies
- treat one eligibility branch as the only possible branch

You MUST:
1. Identify the user's freelance service/activity.
2. Identify the relevant FBR provision from the supplied evidence.
3. Identify ALL applicable branches/rates supported by the evidence.
4. Select the branch that matches the user's explicitly stated facts.
5. Return the rate explicitly supported by the evidence.
6. Determine whether deterministic calculation is possible.
7. Identify genuinely missing or unresolved information.
8. Identify income outside the current freelance calculation scope.

IMPORTANT RATE RULE:

The rate MUST come directly from supplied FBR evidence.

For example, if the supplied evidence contains:

- PSEB-registered computer software / IT / IT-enabled services
  → 0.25%

- Any other case
  → 1.00%

then:

PSEB registered = true
    → select 0.25%

PSEB registered = false
    → select 1.00%

Do NOT automatically select 0.25%.

Do NOT reject the entire provision simply because the taxpayer
is not PSEB registered.

Do NOT invent the "any other case" branch if it is not present
in the supplied evidence.

The evidence must establish the branch and rate.

PSEB CERTIFICATION:

Distinguish between:

A. Explicitly confirmed:
pseb_registered = true
and there is no explicit uncertainty about certification.

B. Not stated:
pseb_certification_valid = null
and uncertain_facts is empty.

This does NOT automatically mean the taxpayer is ineligible.

C. Explicitly uncertain:
The user says certification may be expired, invalid, or is uncertain.

This IS an unresolved eligibility issue.

If certification is explicitly uncertain:
- calculation_ready = false
- add confirmation of current PSEB certification to missing_information.

NON-PSEB CASE:

If pseb_registered = false and the supplied FBR evidence explicitly
contains an alternative branch such as "any other case = 1%":

- select that alternative branch;
- return its evidence-supported rate;
- calculation can proceed if income and currency requirements are satisfied.

Do NOT require PSEB registration when the selected FBR branch does not
require it.

CALCULATION READINESS:

calculation_ready = true when:

- applicable FBR treatment is identified;
- a rate is explicitly supported by supplied evidence;
- annual freelance income is available;
- income is already in PKR;
- no explicitly unresolved eligibility issue exists.

calculation_ready = false when:

- no supported treatment can be established;
- no supported rate exists;
- annual income is missing;
- income is foreign currency and no PKR amount or valid conversion basis
  is supplied;
- an eligibility condition is explicitly unresolved;
- supplied evidence does not establish which branch applies.

IMPORTANT:

A fact being unstated is NOT automatically the same as the user
being uncertain about that fact.

For example:

pseb_registered = true
pseb_certification_valid = null
uncertain_facts = []

Do NOT automatically fail the case.

OTHER INCOME:

Rental income, salary, dividends, crypto income, etc. are outside the
current freelance calculation scope.

Put them in out_of_scope_items.

Do NOT calculate them.

PAYMENT CHANNELS:

Upwork, direct clients, Pakistani bank accounts, foreign currency
accounts, etc. are contextual facts.

Do not invent separate tax categories for them unless the supplied
FBR evidence explicitly makes them relevant.

RETURN FILED:

If the user explicitly says their return has been filed, treat that
fact as satisfied.

OUTPUT ONLY VALID JSON:

{
    "freelance_treatment_applicable": true,
    "applicable_section": null,
    "rate_percent": null,
    "rate_basis": "",
    "conditions": [],
    "calculation_ready": false,
    "missing_information": [],
    "out_of_scope_items": [],
    "supporting_sources": []
}
"""


def _prepare_evidence(retrieved_rules):
    """
    Prepare retrieved FBR evidence for the rule-selection agent.

    We keep enough text for the model to see multiple branches,
    including alternative rates such as "any other case".
    """

    evidence = []

    for rule in retrieved_rules:

        text = rule["text"].strip()

        # Keep evidence reasonably bounded while preserving
        # enough context for rate/branch detection.
        text = text[:3000]

        metadata = rule.get("metadata", {})

        evidence.append(
            {
                "text": text,
                "filename": metadata.get("filename"),
                "page": metadata.get("page"),
                "chunk_index": metadata.get("chunk_index"),
            }
        )

    return evidence


def select_tax_rule(
    profile: FreelancerProfile,
    retrieved_rules,
) -> dict:

    evidence = _prepare_evidence(
        retrieved_rules
    )

    user_prompt = f"""
FREELANCER PROFILE:

{json.dumps(
    profile.model_dump(),
    indent=2,
    ensure_ascii=False,
)}

FBR EVIDENCE:

{json.dumps(
    evidence,
    indent=2,
    ensure_ascii=False,
)}

TASK:

Determine the FBR treatment that applies to THIS freelancer.

Follow this decision process:

1. Identify the freelance service.

2. Identify the relevant FBR provision from the supplied evidence.

3. Look for all rate branches in the supplied evidence.

4. Match the user's explicit facts to the correct branch.

5. If PSEB registration is TRUE:
   select the PSEB-qualified branch if the evidence supports it.

6. If PSEB registration is FALSE:
   do NOT select the PSEB-qualified branch.
   Look for an alternative branch such as "any other case".
   Select that branch ONLY if the supplied evidence explicitly supports it.

7. If PSEB certification is explicitly uncertain:
   calculation_ready must be false.

8. If annual_income is available and already expressed in PKR,
   it can be used for deterministic calculation.

9. Do not calculate the tax amount yourself.

10. rate_percent must come directly from supplied evidence.

11. If the evidence supports:
       PSEB-qualified case = 0.25%
       any other case = 1.00%

    then:

       PSEB registered = true
           → rate_percent = 0.25

       PSEB registered = false
           → rate_percent = 1.00

12. Do not invent a rate if the evidence does not explicitly support it.

13. Rental/non-freelance income belongs in out_of_scope_items.

14. Return filed status should be treated according to the user's
    explicit statement.

15. If calculation is ready, set:
       calculation_ready = true

16. If calculation is not ready, explain exactly why in
    missing_information.

Return ONLY valid JSON.
"""

    response = ask_groq(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.0,
    )

    try:

        result = json.loads(response)

    except json.JSONDecodeError as exc:

        raise ValueError(
            "Rule-selection agent returned invalid JSON."
        ) from exc

    if not isinstance(result, dict):

        raise ValueError(
            "Rule-selection agent returned an invalid object."
        )

    # -----------------------------------------------------
    # SAFE DEFAULTS
    # -----------------------------------------------------

    result.setdefault(
        "freelance_treatment_applicable",
        False,
    )

    result.setdefault(
        "applicable_section",
        None,
    )

    result.setdefault(
        "rate_percent",
        None,
    )

    result.setdefault(
        "rate_basis",
        "",
    )

    result.setdefault(
        "conditions",
        [],
    )

    result.setdefault(
        "calculation_ready",
        False,
    )

    result.setdefault(
        "missing_information",
        [],
    )

    result.setdefault(
        "out_of_scope_items",
        [],
    )

    result.setdefault(
        "supporting_sources",
        [],
    )

    # -----------------------------------------------------
    # OTHER INCOME
    # -----------------------------------------------------

    if profile.other_income_sources:

        existing_out_of_scope = list(
            result.get(
                "out_of_scope_items",
                [],
            )
        )

        for item in profile.other_income_sources:

            if item not in existing_out_of_scope:

                existing_out_of_scope.append(
                    item
                )

        result["out_of_scope_items"] = (
            existing_out_of_scope
        )

    # -----------------------------------------------------
    # EXPLICIT PSEB CERTIFICATION UNCERTAINTY
    # -----------------------------------------------------

    uncertain_text = " ".join(
        profile.uncertain_facts
    ).lower()

    explicit_certification_uncertainty = any(
        keyword in uncertain_text
        for keyword in [
            "pseb",
            "certification",
            "certified",
            "certificate",
            "expired",
            "invalid",
        ]
    )

    if explicit_certification_uncertainty:

        result["calculation_ready"] = False

        missing = list(
            result.get(
                "missing_information",
                [],
            )
        )

        certification_message = (
            "Confirmation that the freelancer's "
            "PSEB certification is currently valid."
        )

        if certification_message not in missing:

            missing.append(
                certification_message
            )

        result["missing_information"] = missing

    # -----------------------------------------------------
    # RATE SAFETY
    # -----------------------------------------------------

    rate = result.get(
        "rate_percent"
    )

    if rate is not None:

        try:
            rate = float(rate)

            if rate <= 0:

                result["rate_percent"] = None
                result["calculation_ready"] = False

        except (
            TypeError,
            ValueError,
        ):

            result["rate_percent"] = None
            result["calculation_ready"] = False

    # -----------------------------------------------------
    # NON-PKR SAFETY
    # -----------------------------------------------------

    if profile.currency:

        currency = profile.currency.upper()

        if currency != "PKR":

            result["calculation_ready"] = False

            missing = list(
                result.get(
                    "missing_information",
                    [],
                )
            )

            message = (
                "A PKR income amount or a valid "
                "currency conversion basis is required "
                "before deterministic calculation."
            )

            if message not in missing:

                missing.append(
                    message
                )

            result["missing_information"] = missing

    # -----------------------------------------------------
    # MISSING INCOME SAFETY
    # -----------------------------------------------------

    if profile.annual_income is None:

        result["calculation_ready"] = False

        missing = list(
            result.get(
                "missing_information",
                [],
            )
        )

        message = (
            "Annual freelance income is required "
            "before deterministic calculation."
        )

        if message not in missing:

            missing.append(
                message
            )

        result["missing_information"] = missing

    # -----------------------------------------------------
    # FINAL CALCULATION READINESS
    # -----------------------------------------------------

    if (
        result.get(
            "freelance_treatment_applicable"
        )
        and result.get(
            "rate_percent"
        ) is not None
        and profile.annual_income is not None
        and profile.currency
        and profile.currency.upper() == "PKR"
        and not explicit_certification_uncertainty
    ):

        result["calculation_ready"] = True

    else:

        result["calculation_ready"] = False

    return result