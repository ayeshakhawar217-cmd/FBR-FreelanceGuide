from utils.groq_client import ask_groq
from utils.schemas import FreelancerProfile
import json


SYSTEM_PROMPT = """
You are the independent verification agent for FBR FreelanceGuide.

You are a BLIND verifier.

You receive only:
1. The freelancer's structured profile.
2. The selected FBR rule and supporting evidence.
3. The deterministic calculation.

You must independently verify the result.

Do NOT assume the previous agent is correct.
Do NOT rely on hidden reasoning from another agent.

VERIFY THESE FOUR THINGS:

1. ELIGIBILITY

Check the taxpayer eligibility conditions supported by the supplied
FBR evidence.

IMPORTANT DISTINCTION:

There are three different states for an eligibility fact:

A. EXPLICITLY CONFIRMED
Example:
pseb_registered = true
and the user explicitly confirms valid/current certification.

This can be treated as confirmed.

B. NOT EXPLICITLY CONFIRMED
Example:
pseb_registered = true
but pseb_certification_valid = null
and the user did NOT say that the certification is expired,
invalid, or uncertain.

This does NOT mean the taxpayer is ineligible.

In this situation:
- core eligibility is not disproven;
- return the core verification as verified;
- add a caveat saying the certification was not explicitly confirmed.

C. EXPLICITLY UNCERTAIN / INVALID
Example:
The user says:
"My PSEB certification may have expired."
"My certification is not valid."
"I'm not sure whether my PSEB certification is current."

This is an unresolved eligibility issue.

In this situation:
- verified = false
- overall_status = "REQUIRES_REVIEW"
- explain that current PSEB certification must be confirmed.

Do NOT turn missing information into an automatic eligibility failure.

PROCEDURAL WITHHOLDING INFORMATION:

If evidence says something such as:

"Every authorized dealer in foreign exchange shall deduct tax
at the time of realization of foreign exchange proceeds."

This describes HOW tax is collected.

Absence of information about the authorized dealer in the profile
does NOT mean the freelancer is ineligible.

Treat missing procedural information as a caveat, not an eligibility failure.

2. SECTION

Check whether the selected tax section/provision is supported by
the supplied FBR evidence.

Do NOT use outside knowledge.

3. RATE

Check whether the selected tax rate is explicitly supported by
the supplied FBR evidence.

Do NOT invent or infer a rate.

rate_percent represents percentage:
0.25 means 0.25%
1.0 means 1%
4.0 means 4%

The rate must match the selected rule and evidence.

4. ARITHMETIC

Verify:

tax_amount = annual_income × rate_percent / 100

Use the exact selected rate from the calculation.

Do not independently choose another rate.

OUTPUT ONLY VALID JSON.

If everything important is confirmed:

{
    "verified": true,
    "eligibility_check": "PASS",
    "rate_check": "PASS",
    "arithmetic_check": "PASS",
    "overall_status": "VERIFIED",
    "issues": [],
    "caveats": [],
    "verification_summary": "The selected treatment, supported rate, eligibility conditions, and arithmetic were independently verified."
}

If the core treatment, rate, and arithmetic are supported but an
important fact is not explicitly confirmed:

{
    "verified": true,
    "eligibility_check": "PASS",
    "rate_check": "PASS",
    "arithmetic_check": "PASS",
    "overall_status": "VERIFIED_WITH_CAVEAT",
    "issues": [],
    "caveats": [
        "..."
    ],
    "verification_summary": "The core tax treatment, supported rate, and arithmetic were independently verified, with an eligibility confirmation caveat."
}

If an actual eligibility condition is explicitly unresolved,
the selected section is unsupported, the rate is unsupported,
or the arithmetic is incorrect:

{
    "verified": false,
    "eligibility_check": "FAIL",
    "rate_check": "PASS",
    "arithmetic_check": "PASS",
    "overall_status": "REQUIRES_REVIEW",
    "issues": [
        "..."
    ],
    "caveats": [],
    "verification_summary": "..."
}

IMPORTANT RULES:

- Do not invent facts.
- Do not invent FBR provisions.
- Do not use knowledge outside supplied evidence.
- Do not fail eligibility merely because a fact is not explicitly mentioned.
- Do not treat null pseb_certification_valid as proof that certification is invalid.
- If pseb_registered=true and certification is not explicitly described
  as invalid or uncertain, do NOT fail the result solely because
  pseb_certification_valid is null.
- If the user explicitly expresses uncertainty about PSEB certification,
  treat it as an unresolved eligibility issue.
- Do not assume a default tax rate.
- Do not assume 0.25% or any other rate.
- Verify the rate against supplied evidence.
- Verify arithmetic against the supplied calculation.
- Do not provide legal advice.
- Keep the verification summary concise.
"""


def verify_calculation(
    profile: FreelancerProfile,
    selected_rule: dict,
    calculation: dict,
) -> dict:

    verification_input = {
        "freelancer_profile": profile.model_dump(),
        "selected_rule": selected_rule,
        "calculation": calculation,
    }

    response = ask_groq(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=json.dumps(
            verification_input,
            indent=2,
            ensure_ascii=False,
        ),
        temperature=0.0,
    )

    try:
        result = json.loads(response)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Verification agent returned invalid JSON."
        ) from exc

    if not isinstance(result, dict):
        raise ValueError(
            "Verification agent returned an invalid object."
        )

    # ---------------------------------------------------------
    # Normalize required fields so the UI always gets
    # a predictable verification object.
    # ---------------------------------------------------------

    result.setdefault("verified", False)
    result.setdefault("eligibility_check", "FAIL")
    result.setdefault("rate_check", "FAIL")
    result.setdefault("arithmetic_check", "FAIL")
    result.setdefault("overall_status", "REQUIRES_REVIEW")
    result.setdefault("issues", [])
    result.setdefault("caveats", [])
    result.setdefault(
        "verification_summary",
        "Independent verification could not be completed."
    )

    # ---------------------------------------------------------
    # Safety normalization:
    #
    # If the user explicitly stated uncertainty about PSEB
    # certification, the result cannot be treated as fully
    # verified.
    # ---------------------------------------------------------

    explicit_certification_uncertainty = any(
        keyword in " ".join(
            profile.uncertain_facts
        ).lower()
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

        result["verified"] = False
        result["eligibility_check"] = "FAIL"
        result["overall_status"] = "REQUIRES_REVIEW"

        issue = (
            "The current validity of the freelancer's "
            "PSEB certification is explicitly uncertain "
            "and must be confirmed before relying on the "
            "selected treatment."
        )

        if issue not in result["issues"]:
            result["issues"].append(issue)

        result["verification_summary"] = (
            "The selected treatment cannot be fully verified "
            "because PSEB certification validity is explicitly "
            "uncertain."
        )

    return result