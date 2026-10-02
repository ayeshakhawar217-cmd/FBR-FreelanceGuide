import time
import streamlit as st

from ui.styles import inject_styles
from ui.components import (
    render_navbar,
    render_hero,
    render_input_label,
    render_processing_header,
    render_stage,
    render_result_header,
    render_result_card,
    render_metric,
    render_section_title,
    render_rule,
    render_condition,
    render_verification,
    render_caveat,
    render_source,
    render_demo_intro,
    render_demo_card,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="FBR FreelanceGuide",
    page_icon="F",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# GLOBAL STYLES
# =========================================================

inject_styles()


# =========================================================
# SESSION STATE
# =========================================================

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "user_input" not in st.session_state:
    st.session_state.user_input = ""


# =========================================================
# NAVBAR
# =========================================================

render_navbar()


# =========================================================
# RESET / HOMEPAGE
# =========================================================

if st.session_state.analysis_result is None:

    # -----------------------------------------------------
    # HERO
    # -----------------------------------------------------

    render_hero()

    st.markdown(
        "<div style='height:36px;'></div>",
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # INPUT
    # -----------------------------------------------------

    render_input_label()

    user_input = st.text_area(
        label="",
        value=st.session_state.user_input,
        placeholder=(
            "Tell us about your freelance work, clients, "
            "income, platform, PSEB status, and how you receive payments..."
        ),
        height=150,
        label_visibility="collapsed",
    )

    st.session_state.user_input = user_input

    st.markdown(
        "<div style='height:12px;'></div>",
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # DEMO SCENARIOS
    # -----------------------------------------------------

    render_demo_intro()

    demo_col1, demo_col2, demo_col3 = st.columns(
        3,
        gap="medium",
    )

    # =====================================================
    # SCENARIO DATA
    # =====================================================

    # -----------------------------------------------------
    # CASE 01 — CLEAR IT EXPORT
    # -----------------------------------------------------

    demo_1 = """
    Main aik Pakistani software developer hoon aur US clients ke liye
    kaam karta hoon. Meri saalana freelance income taqreeban 48 lakh PKR
    hai. Mujhe payments foreign currency mein milti hain jo mere Pakistani
    bank account mein receive hoti hain. Main PSEB ke saath registered hoon
    aur apna income tax return file kar chuka hoon. Meri estimated tax
    amount kitni banti hai?
    """

    # -----------------------------------------------------
    # CASE 02 — DIFFERENT ELIGIBILITY
    # -----------------------------------------------------

    demo_2 = """
    Main Pakistan mein software development ka freelance kaam karta hoon
    aur meri saalana income 48 lakh PKR hai. Mere clients US mein hain aur
    mujhe payments foreign currency mein milti hain jo mere Pakistani bank
    account mein receive hoti hain. Main PSEB ke saath registered nahi hoon.
    Mere case mein FBR ke mutabiq konsa tax treatment apply ho sakta hai?
    """

    # -----------------------------------------------------
    # CASE 03 — NEEDS CONFIRMATION
    # -----------------------------------------------------

    demo_3 = """
    Main aik Pakistani software developer hoon aur Upwork ke zariye US
    clients se har mahine taqreeban 4,000 dollars kamata hoon. Kuch clients
    mujhe directly pay karte hain aur kuch Upwork ke zariye. Maine pichle
    saal PSEB ke saath registration karwai thi lekin mujhe yaqeen nahi ke
    meri certification abhi valid hai. Is ke ilawa meri aik choti rental
    property bhi hai jis se har mahine 50,000 PKR milte hain. Maine pichla
    tax return file kiya tha lekin is saal abhi file nahi kiya. Calculation
    par rely karne se pehle mujhe konsi information confirm karni hogi?
    """

    # =====================================================
    # SCENARIO 01 CARD
    # =====================================================

    with demo_col1:

        if st.button(
            "CLEAR IT EXPORT",
            use_container_width=True,
            key="demo_1",
        ):
            st.session_state.user_input = demo_1.strip()
            st.rerun()

        st.html(
            render_demo_card(
                "Clear IT export",
                "Straightforward case with enough information for calculation.",
                "CASE 01",
            )
        )

    # =====================================================
    # SCENARIO 02 CARD
    # =====================================================

    with demo_col2:

        if st.button(
            "DIFFERENT ELIGIBILITY",
            use_container_width=True,
            key="demo_2",
        ):
            st.session_state.user_input = demo_2.strip()
            st.rerun()

        st.html(
            render_demo_card(
                "Different eligibility",
                "Tests how eligibility facts affect the selected FBR treatment.",
                "CASE 02",
            )
        )

    # =====================================================
    # SCENARIO 03 CARD
    # =====================================================

    with demo_col3:

        if st.button(
            "NEEDS CONFIRMATION",
            use_container_width=True,
            key="demo_3",
        ):
            st.session_state.user_input = demo_3.strip()
            st.rerun()

        st.html(
            render_demo_card(
                "Needs confirmation",
                "Tests uncertainty, USD income, and income outside freelance scope.",
                "CASE 03",
            )
        )

    st.markdown(
        "<div style='height:28px;'></div>",
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # CHECK BUTTON
    # -----------------------------------------------------

    check = st.button(
        "CHECK MY TAX SITUATION →",
        type="primary",
        use_container_width=True,
    )

    if check:

        if not user_input.strip():

            st.warning(
                "Please describe your freelance situation first."
            )
            st.stop()

        # -------------------------------------------------
        # PROCESSING SCREEN
        # -------------------------------------------------

        render_processing_header()

        stages = [
            (
                "01",
                "Understanding your situation",
                "Extracting your freelance facts.",
            ),
            (
                "02",
                "Searching FBR evidence",
                "Retrieving relevant provisions from the FBR corpus.",
            ),
            (
                "03",
                "Determining applicable treatment",
                "Matching your situation against retrieved evidence.",
            ),
            (
                "04",
                "Checking the result",
                "Independently verifying the analysis.",
            ),
        ]

        stage_placeholder = st.empty()

        for index, (
            number,
            name,
            description,
        ) in enumerate(stages):

            with stage_placeholder.container():

                for stage_index, stage in enumerate(stages):

                    st.html(
                        render_stage(
                            stage[0],
                            stage[1],
                            stage[2],
                            active=(
                                stage_index == index
                            ),
                        )
                    )

            time.sleep(0.45)

        # -------------------------------------------------
        # RUN ACTUAL PIPELINE
        # -------------------------------------------------

        try:

            from agents.orchestrator import (
                run_freelance_tax_analysis,
            )

            result = run_freelance_tax_analysis(
                user_text=user_input,
                retrieval_results=4,
            )

            st.session_state.analysis_result = result

            st.rerun()

        except Exception as exc:

            st.error(
                "The analysis could not be completed."
            )

            st.code(
                str(exc),
                language="text",
            )

            st.stop()


# =========================================================
# RESULT SCREEN
# =========================================================

else:

    result = st.session_state.analysis_result

    # -----------------------------------------------------
    # Scroll to top after rerun
    # -----------------------------------------------------

    st.html(
        """
        <script>
        setTimeout(function() {
            try {
                window.parent.document.documentElement.scrollTo({
                    top: 0,
                    behavior: "instant"
                });

                window.parent.document.body.scrollTo({
                    top: 0,
                    behavior: "instant"
                });

                window.parent.window.scrollTo({
                    top: 0,
                    behavior: "instant"
                });
            } catch (e) {
                console.log("Scroll reset:", e);
            }
        }, 100);
        </script>
        """
    )

    # -----------------------------------------------------
    # RESULT HEADER
    # -----------------------------------------------------

    render_result_header()

    st.markdown(
        "<div style='height:22px;'></div>",
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # GET RESULT DATA
    # -----------------------------------------------------

    calculation = result.get(
        "calculation"
    )

    selected_rule = result.get(
        "selected_rule",
        {},
    )

    verification = result.get(
        "verification",
        {},
    )

    analysis_status = result.get(
        "analysis_status",
        "NEEDS_REVIEW",
    )

    # =====================================================
    # CALCULATED RESULT
    # =====================================================

    if (
        analysis_status == "CALCULATED"
        and calculation
    ):

        tax_amount = calculation.get(
            "tax_amount",
            0,
        )

        verification_status = verification.get(
            "overall_status",
            "VERIFIED",
        )

        # -------------------------------------------------
        # MAIN RESULT
        # -------------------------------------------------

        render_result_card(
            tax_amount,
            verification_status,
        )

        st.markdown(
            "<div style='height:18px;'></div>",
            unsafe_allow_html=True,
        )

        # -------------------------------------------------
        # METRICS
        # -------------------------------------------------

        metric_col1, metric_col2, metric_col3 = st.columns(
            3,
            gap="medium",
        )

        with metric_col1:

            annual_income = calculation.get(
                "annual_income",
                0,
            )

            render_metric(
                "ANNUAL EXPORT PROCEEDS",
                f"PKR {annual_income:,.0f}",
            )

        with metric_col2:

            rate = calculation.get(
                "tax_rate",
                0,
            )

            render_metric(
                "APPLIED RATE",
                f"{rate:g}%",
            )

        with metric_col3:

            effective_rate = calculation.get(
                "effective_rate",
                0,
            )

            render_metric(
                "EFFECTIVE RATE",
                f"{effective_rate:g}%",
            )

    # =====================================================
    # NEEDS CONFIRMATION RESULT
    # =====================================================

    else:

        st.html(
            """
            <div class="result-card">

                <div class="result-label">
                    CALCULATION STATUS
                </div>

                <div
                    class="tax-amount"
                    style="
                        font-size:42px;
                        line-height:1.05;
                    "
                >
                    NEEDS CONFIRMATION
                </div>

                <div class="verification-badge">
                    NO UNSUPPORTED TAX AMOUNT GENERATED
                </div>

            </div>
            """
        )

    st.markdown(
        "<div style='height:30px;'></div>",
        unsafe_allow_html=True,
    )

    # =====================================================
    # RULE / TREATMENT
    # =====================================================

    render_section_title(
        "Applicable FBR treatment"
    )

    if selected_rule:

        render_rule(
            selected_rule
        )

    # =====================================================
    # CONDITIONS
    # =====================================================

    conditions = selected_rule.get(
        "conditions",
        [],
    )

    if conditions:

        st.markdown(
            "<div style='height:18px;'></div>",
            unsafe_allow_html=True,
        )

        render_section_title(
            "Relevant conditions"
        )

        for condition in conditions:

            render_condition(
                condition
            )

    # =====================================================
    # MISSING INFORMATION
    # =====================================================

    missing_information = selected_rule.get(
        "missing_information",
        [],
    )

    if missing_information:

        st.markdown(
            "<div style='height:22px;'></div>",
            unsafe_allow_html=True,
        )

        render_section_title(
            "What needs confirmation"
        )

        for item in missing_information:

            render_caveat(
                item
            )

    # =====================================================
    # OUT OF SCOPE ITEMS
    # =====================================================

    out_of_scope_items = selected_rule.get(
        "out_of_scope_items",
        [],
    )

    if out_of_scope_items:

        st.markdown(
            "<div style='height:22px;'></div>",
            unsafe_allow_html=True,
        )

        render_section_title(
            "Outside the current freelance scope"
        )

        for item in out_of_scope_items:

            render_condition(
                f"{item} was identified, but it was not "
                "included in the freelance tax calculation."
            )

    # =====================================================
    # VERIFICATION
    # =====================================================

    if verification:

        st.markdown(
            "<div style='height:22px;'></div>",
            unsafe_allow_html=True,
        )

        render_section_title(
            "Independent verification"
        )

        render_verification(
            verification
        )

    # =====================================================
    # CAVEATS
    # =====================================================

    caveats = verification.get(
        "caveats",
        [],
    )

    if caveats:

        st.markdown(
            "<div style='height:22px;'></div>",
            unsafe_allow_html=True,
        )

        render_section_title(
            "Important"
        )

        for caveat in caveats:

            render_caveat(
                caveat
            )

    # =====================================================
    # SOURCES
    # =====================================================

    sources = selected_rule.get(
        "supporting_sources",
        [],
    )

    if sources:

        st.markdown(
            "<div style='height:22px;'></div>",
            unsafe_allow_html=True,
        )

        render_section_title(
            "FBR sources"
        )

        for source in sources:

            render_source(
                source
            )

    # =====================================================
    # RETRIEVED EVIDENCE COUNT
    # =====================================================

    retrieved_evidence = result.get(
        "retrieved_evidence",
        [],
    )

    if retrieved_evidence:

        st.markdown(
            "<div style='height:18px;'></div>",
            unsafe_allow_html=True,
        )

        st.html(
            f"""
            <div
                style="
                    font-family:'IBM Plex Mono',monospace;
                    font-size:10px;
                    color:#6B6B72;
                    letter-spacing:.05em;
                    text-transform:uppercase;
                    margin-top:8px;
                "
            >
                Analysis grounded in
                {len(retrieved_evidence)}
                retrieved FBR evidence chunks
            </div>
            """
        )

    # =====================================================
    # ORIGINAL INPUT
    # =====================================================

    st.markdown(
        "<div style='height:26px;'></div>",
        unsafe_allow_html=True,
    )

    render_section_title(
        "Your submitted situation"
    )

    st.html(
        f"""
        <div
            style="
                background:#F2EFE6;
                border:1px solid rgba(20,20,26,.08);
                border-radius:18px;
                padding:18px 20px;
                color:#14141A;
                font-family:'IBM Plex Sans',sans-serif;
                font-size:14px;
                line-height:1.7;
            "
        >
            {result.get("input", "")}
        </div>
        """
    )

    # =====================================================
    # RESET
    # =====================================================

    st.markdown(
        "<div style='height:28px;'></div>",
        unsafe_allow_html=True,
    )

    if st.button(
        "← ANALYZE ANOTHER SITUATION",
        use_container_width=True,
    ):

        st.session_state.analysis_result = None
        st.session_state.user_input = ""

        st.rerun()