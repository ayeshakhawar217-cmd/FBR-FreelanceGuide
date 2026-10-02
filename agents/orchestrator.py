import json

from agents.intake import extract_freelancer_facts
from agents.retrieval import retrieve_rules
from agents.rule_selection import select_tax_rule
from agents.calculation import calculate_freelancer_tax
from agents.verification import verify_calculation


def run_freelance_tax_analysis(
    user_text: str,
    retrieval_results: int = 4,
) -> dict:

    if not user_text or not user_text.strip():
        raise ValueError(
            "User input cannot be empty."
        )

    # ============================================================
    # 1. INTAKE
    # ============================================================

    profile = extract_freelancer_facts(
        user_text
    )

    # ============================================================
    # 2. RETRIEVAL
    # ============================================================

    retrieved_rules = retrieve_rules(
        profile,
        n_results=retrieval_results,
    )

    if not retrieved_rules:
        return {
            "input": user_text,
            "profile": profile.model_dump(),
            "retrieved_evidence": [],
            "selected_rule": {
                "freelance_treatment_applicable": False,
                "calculation_ready": False,
                "rate_percent": None,
                "missing_information": [
                    "No relevant FBR evidence was retrieved."
                ],
                "out_of_scope_items": (
                    profile.other_income_sources
                ),
                "supporting_sources": [],
            },
            "calculation": None,
            "verification": {
                "verified": False,
                "overall_status": "REQUIRES_REVIEW",
                "issues": [
                    "No relevant FBR evidence was retrieved."
                ],
                "caveats": [],
                "verification_summary": (
                    "The freelance tax treatment could not "
                    "be established from the retrieved evidence."
                ),
            },
            "analysis_status": "NEEDS_REVIEW",
        }

    # ============================================================
    # 3. RULE SELECTION
    # ============================================================

    selected_rule = select_tax_rule(
        profile,
        retrieved_rules,
    )

    rate_percent = selected_rule.get(
        "rate_percent"
    )

    calculation_ready = selected_rule.get(
        "calculation_ready",
        False,
    )

    # ============================================================
    # 4. COLLECT MISSING INFORMATION
    #
    # IMPORTANT:
    # The orchestrator should NOT invent additional missing
    # information here.
    #
    # The rule-selection agent is responsible for deciding
    # whether a missing/uncertain fact actually prevents
    # calculation.
    # ============================================================

    missing_information = list(
        selected_rule.get(
            "missing_information",
            [],
        )
    )

    # ------------------------------------------------------------
    # Currency / income requirements
    # ------------------------------------------------------------

    if profile.annual_income is None:

        if profile.monthly_income is not None:

            if profile.currency == "PKR":
                missing_information.append(
                    "Annual freelance export proceeds are "
                    "required for deterministic calculation."
                )

            else:
                missing_information.append(
                    "A PKR value for the freelance export "
                    "proceeds is required for deterministic "
                    "calculation."
                )

        else:

            missing_information.append(
                "Annual freelance export proceeds are required."
            )

    elif profile.currency != "PKR":

        missing_information.append(
            "A PKR value for the freelance export proceeds "
            "is required for deterministic calculation."
        )

    # ------------------------------------------------------------
    # Remove duplicate messages while preserving order
    # ------------------------------------------------------------

    missing_information = list(
        dict.fromkeys(
            missing_information
        )
    )

    selected_rule[
        "missing_information"
    ] = missing_information

    # ============================================================
    # 5. HANDLE NON-READY CALCULATION
    #
    # IMPORTANT:
    #
    # Do NOT use:
    #
    #     or missing_information
    #
    # here.
    #
    # A missing-information list can contain informational
    # caveats while the actual calculation is still valid.
    #
    # The calculation is blocked only when:
    #
    # - rule selection says calculation is not ready
    # - no evidence-supported rate exists
    # - annual income is unavailable
    # - income is not already expressed in PKR
    # ============================================================

    if (
        not calculation_ready
        or rate_percent is None
        or profile.annual_income is None
        or profile.currency != "PKR"
    ):
        return {
            "input": user_text,
            "profile": profile.model_dump(),
            "retrieved_evidence": retrieved_rules,
            "selected_rule": selected_rule,
            "calculation": None,
            "verification": {
                "verified": False,
                "overall_status": "VERIFICATION_PENDING",
                "issues": [],
                "caveats": missing_information,
                "verification_summary": (
                    "The applicable freelance treatment was "
                    "analyzed, but deterministic calculation "
                    "was not performed because required "
                    "information remains unconfirmed."
                ),
            },
            "analysis_status": "NEEDS_CONFIRMATION",
        }

    # ============================================================
    # 6. DETERMINISTIC CALCULATION
    # ============================================================

    calculation = calculate_freelancer_tax(
        profile=profile,
        tax_rate_percent=rate_percent,
    )

    # ============================================================
    # 7. BLIND VERIFICATION
    # ============================================================

    verification = verify_calculation(
        profile=profile,
        selected_rule=selected_rule,
        calculation=calculation,
    )

    # ============================================================
    # 8. FINAL RESULT
    # ============================================================

    return {
        "input": user_text,
        "profile": profile.model_dump(),
        "retrieved_evidence": retrieved_rules,
        "selected_rule": selected_rule,
        "calculation": calculation,
        "verification": verification,
        "analysis_status": "CALCULATED",
    }


# ================================================================
# LOCAL TEST
# ================================================================

if __name__ == "__main__":

    demo_input = """
    I'm a Pakistani software developer. I earn around PKR 4.8 million
    annually from US clients through Upwork. I provide software
    development and IT services. My clients pay me in foreign currency,
    and the money is received in my Pakistani bank account. I am
    registered with the Pakistan Software Export Board (PSEB), and I
    have filed my income tax return for the previous year.
    """

    print("\n" + "=" * 80)
    print("FBR FREELANCEGUIDE")
    print("MASTER ORCHESTRATOR")
    print("=" * 80)

    try:

        result = run_freelance_tax_analysis(
            user_text=demo_input,
            retrieval_results=4,
        )

        print("\nFINAL RESULT")
        print("=" * 80)

        print(
            json.dumps(
                result,
                indent=2,
                ensure_ascii=False,
            )
        )

    except Exception as exc:

        print("\nPIPELINE ERROR")
        print("=" * 80)

        print(str(exc))

        raise