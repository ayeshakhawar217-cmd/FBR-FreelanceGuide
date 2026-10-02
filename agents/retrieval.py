from rag.retriever import retrieve_fbr_rules
from utils.schemas import FreelancerProfile


def retrieve_rules(
    profile: FreelancerProfile,
    n_results: int = 8,
):
    """
    Retrieve FBR evidence relevant to the freelancer's situation.

    The retrieval strategy is deliberately centered on Section 154A
    export-of-services treatment so unrelated provisions such as
    Section 152 software-development withholding do not dominate
    the top results.
    """

    query_parts = []

    # ---------------------------------------------------------
    # USER-SPECIFIC FACTS
    # ---------------------------------------------------------

    if profile.profession:
        query_parts.append(
            f"profession: {profile.profession}"
        )

    if profile.service_category:
        query_parts.append(
            f"service category: {profile.service_category}"
        )

    if profile.client_location:
        query_parts.append(
            f"client location: {profile.client_location}"
        )

    if profile.income_source:
        query_parts.append(
            f"income source: {profile.income_source}"
        )

    if profile.platform:
        query_parts.append(
            f"platform: {profile.platform}"
        )

    if profile.pseb_registered is not None:
        query_parts.append(
            f"PSEB registered: {profile.pseb_registered}"
        )

    if profile.pseb_certification_valid is not None:
        query_parts.append(
            "PSEB certification valid: "
            f"{profile.pseb_certification_valid}"
        )

    if profile.return_filed is not None:
        query_parts.append(
            f"return filed: {profile.return_filed}"
        )

    if profile.foreign_currency_received is not None:
        query_parts.append(
            "foreign currency received: "
            f"{profile.foreign_currency_received}"
        )

    if profile.received_in_pakistani_bank is not None:
        query_parts.append(
            "foreign proceeds received in Pakistani bank: "
            f"{profile.received_in_pakistani_bank}"
        )

    if profile.payment_channels:
        query_parts.append(
            "payment channels: "
            + ", ".join(profile.payment_channels)
        )

    # ---------------------------------------------------------
    # CORE SECTION 154A QUERY
    # ---------------------------------------------------------

    query_parts.append(
        """
        Section 154A
        Export of Services
        Division IVA
        Part III First Schedule
        export proceeds
        computer software
        IT services
        IT enabled services
        PSEB
        Pakistan Software Export Board
        registered with PSEB
        any other case
        rate of tax
        0.25%
        1%
        authorized dealer
        foreign exchange proceeds
        realization of foreign exchange proceeds
        final tax
        return filed
        """
    )

    query = " ".join(query_parts)

    # ---------------------------------------------------------
    # PRIMARY RAG RETRIEVAL
    # ---------------------------------------------------------

    results = retrieve_fbr_rules(
        query,
        n_results=n_results,
    )

    # ---------------------------------------------------------
    # DEDUPLICATION
    # ---------------------------------------------------------

    unique_results = {}

    for result in results:

        metadata = result.get(
            "metadata",
            {},
        )

        key = (
            metadata.get("filename"),
            metadata.get("page"),
            metadata.get("chunk_index"),
        )

        if key not in unique_results:
            unique_results[key] = result

    results = list(
        unique_results.values()
    )

    # ---------------------------------------------------------
    # RELEVANCE FILTERING / PRIORITIZATION
    # ---------------------------------------------------------

    def relevance_score(result):

        metadata = result.get(
            "metadata",
            {},
        )

        text = result.get(
            "text",
            "",
        ).lower()

        filename = str(
            metadata.get(
                "filename",
                ""
            )
        ).lower()

        score = 0

        # Strongest signal: Section 154A
        if "154a" in text:
            score += 100

        # Export of services
        if "export of services" in text:
            score += 40

        if "export proceeds" in text:
            score += 30

        # IT/service terminology
        if "computer software" in text:
            score += 20

        if "it services" in text:
            score += 20

        if "it enabled services" in text:
            score += 20

        # PSEB branch
        if "pseb" in text:
            score += 25

        if "pakistan software export board" in text:
            score += 25

        # Alternative branch
        if "any other case" in text:
            score += 35

        # Rates
        if "0.25%" in text:
            score += 15

        if "1%" in text:
            score += 15

        if "1.00%" in text:
            score += 15

        # Relevant procedural language
        if "foreign exchange proceeds" in text:
            score += 15

        if "authorized dealer" in text:
            score += 10

        if "return has been filed" in text:
            score += 10

        # -----------------------------------------------------
        # PENALIZE KNOWN WRONG BRANCH
        # -----------------------------------------------------

        # Section 152 software-development withholding is not
        # the primary rule we want for this export-proceeds flow.
        if "section 152" in text:
            score -= 80

        if "152(2a)" in text:
            score -= 80

        if "152 (2a)" in text:
            score -= 80

        # The exact 8% software-development branch should not
        # outrank Section 154A for this workflow.
        if "8%" in text and "154a" not in text:
            score -= 60

        # Filename signal
        if "incometaxordinanace2001" in filename:
            score += 5

        if "withholdingtaxratescard" in filename:
            score += 10

        return score

    # ---------------------------------------------------------
    # SORT BY RELEVANCE
    # ---------------------------------------------------------

    results.sort(
        key=relevance_score,
        reverse=True,
    )

    # ---------------------------------------------------------
    # RETURN BEST EVIDENCE
    # ---------------------------------------------------------

    return results[:n_results]