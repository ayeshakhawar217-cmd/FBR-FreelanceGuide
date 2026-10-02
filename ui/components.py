import streamlit as st


# =========================================================
# NAVBAR
# =========================================================

def render_navbar():
    st.html(
        """
        <div class="vf-navbar">

            <div class="vf-brand">
                <span class="vf-brand-mark">F</span>
                FBR FREELANCEGUIDE
            </div>

            <div class="vf-nav-pill">
                FBR-GROUNDED · AI VERIFIED
            </div>

        </div>
        """
    )


# =========================================================
# HERO
# =========================================================

def render_hero():
    st.html(
        """
        <div class="hero-shell">

            <!-- Main content -->
            <div class="hero-content">

                <div class="hero-eyebrow">
                    <span class="hero-eyebrow-dot"></span>
                    BUILT FOR PAKISTANI FREELANCERS
                </div>


                <h1 class="hero-title">
                    Tax clarity
                    <br>
                    <em>without the guesswork.</em>
                </h1>


                <div class="hero-description">
                    Describe your freelance situation and let
                    FreelanceGuide trace it through official FBR
                    evidence, identify the applicable rule, calculate
                    the result, and independently verify it.
                </div>

            </div>


            <!-- Intelligence pipeline -->
            <div class="hero-flow">

                <div class="hero-flow-card">

                    <div class="hero-flow-left">

                        <div class="hero-flow-number">
                            01
                        </div>

                        <div class="hero-flow-name">
                            Your situation
                        </div>

                    </div>

                    <div class="hero-flow-status">
                        INTAKE
                    </div>

                </div>


                <div class="hero-flow-card">

                    <div class="hero-flow-left">

                        <div class="hero-flow-number">
                            02
                        </div>

                        <div class="hero-flow-name">
                            FBR evidence
                        </div>

                    </div>

                    <div class="hero-flow-status">
                        RETRIEVAL
                    </div>

                </div>


                <div class="hero-flow-card">

                    <div class="hero-flow-left">

                        <div class="hero-flow-number">
                            03
                        </div>

                        <div class="hero-flow-name">
                            Applicable rule
                        </div>

                    </div>

                    <div class="hero-flow-status">
                        SELECTION
                    </div>

                </div>


                <div class="hero-flow-card">

                    <div class="hero-flow-left">

                        <div class="hero-flow-number">
                            04
                        </div>

                        <div class="hero-flow-name">
                            Calculation + verification
                        </div>

                    </div>

                    <div class="hero-flow-status">
                        CHECK
                    </div>

                </div>

            </div>

        </div>
        """
    )


# =========================================================
# INPUT LABEL
# =========================================================

def render_input_label():
    st.html(
        """
        <div class="input-label">
            YOUR FREELANCE SITUATION
        </div>
        """
    )


# =========================================================
# PROCESSING HEADER
# =========================================================

def render_processing_header():
    st.html(
        """
        <div class="processing-header">

            <div class="processing-title">
                Checking your situation.
            </div>

            <div class="processing-subtitle">
                Retrieving FBR evidence and independently
                verifying the result.
            </div>

        </div>
        """
    )


# =========================================================
# PROCESSING STAGE
# =========================================================

def render_stage(
    number,
    name,
    description,
    active=False,
):

    active_class = " active" if active else ""

    return f"""
        <div class="stage{active_class}">

            <div class="stage-number">
                {number}
            </div>

            <div>

                <div class="stage-name">
                    {name}
                </div>

                <div class="stage-description">
                    {description}
                </div>

            </div>

        </div>
    """


# =========================================================
# RESULT HEADER
# =========================================================

def render_result_header():
    st.html(
        """
        <div class="result-header">

            <div class="result-eyebrow">
                ANALYSIS COMPLETE
            </div>

            <div class="result-title">
                Your freelance
                <br>
                tax result.
            </div>

            <div class="result-description">
                Your situation was matched against FBR evidence,
                calculated using deterministic arithmetic, and
                independently re-verified.
            </div>

        </div>
        """
    )


# =========================================================
# RESULT CARD
# =========================================================

def render_result_card(
    tax_amount,
    status,
):

    if status == "VERIFIED":

        status_text = (
            "✓ INDEPENDENTLY VERIFIED"
        )

    else:

        status_text = (
            "✓ VERIFIED WITH CAVEAT"
        )


    st.html(
        f"""
        <div class="result-card">

            <div class="result-label">
                ESTIMATED TAX ON EXPORT PROCEEDS
            </div>

            <div class="tax-amount">
                PKR {tax_amount:,.0f}
            </div>

            <div class="verification-badge">
                {status_text}
            </div>

        </div>
        """
    )


# =========================================================
# METRIC
# =========================================================

def render_metric(
    label,
    value,
):

    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                {label}
            </div>

            <div class="metric-value">
                {value}
            </div>

        </div>
        """
    )


# =========================================================
# SECTION TITLE
# =========================================================

def render_section_title(title):

    st.html(
        f"""
        <div class="section-title">
            {title}
        </div>
        """
    )


# =========================================================
# RULE
# =========================================================

def render_rule(rule):

    section = rule.get(
        "applicable_section",
        "154A",
    )

    basis = rule.get(
        "rate_basis",
        "",
    )


    st.html(
        f"""
        <div class="rule-card">

            <div class="metric-label">
                FBR TAX TREATMENT
            </div>

            <div
                style="
                    margin-top:9px;
                    margin-bottom:9px;
                    color:#14141A;
                    font-family:'IBM Plex Sans',sans-serif;
                    font-size:16px;
                    font-weight:650;
                "
            >
                Section {section} — Export of IT Services
            </div>

            <div
                style="
                    color:#6B6B72;
                    font-family:'IBM Plex Sans',sans-serif;
                    font-size:11px;
                    line-height:1.6;
                "
            >
                {basis}
            </div>

        </div>
        """
    )


# =========================================================
# CONDITION
# =========================================================

def render_condition(condition):

    st.html(
        f"""
        <div class="condition-card">

            <span
                style="
                    color:#356B58;
                    font-family:'IBM Plex Mono',monospace;
                    font-weight:700;
                    margin-right:7px;
                "
            >
                ✓
            </span>

            <span>
                {condition}
            </span>

        </div>
        """
    )


# =========================================================
# VERIFICATION
# =========================================================

def render_verification(verification):

    status = verification.get(
        "overall_status",
        "VERIFIED",
    )

    summary = verification.get(
        "verification_summary",
        "",
    )


    display_status = status.replace(
        "_",
        " ",
    )


    st.html(
        f"""
        <div class="verification-card">

            <div class="verification-status">
                {display_status}
            </div>

            <div class="verification-summary">
                {summary}
            </div>

        </div>
        """
    )


# =========================================================
# CAVEAT
# =========================================================

def render_caveat(caveat):

    st.html(
        f"""
        <div class="caveat-card">

            <div class="caveat-label">
                IMPORTANT
            </div>

            <div class="caveat-text">
                {caveat}
            </div>

        </div>
        """
    )


# =========================================================
# SOURCE
# =========================================================

def render_source(source):

    filename = source.get(
        "filename",
        "FBR document",
    )

    page = source.get(
        "page",
        "—",
    )

    reason = source.get(
        "reason",
        "",
    )


    st.html(
        f"""
        <div class="source-card">

            <div>

                <div class="source-file">
                    {filename}
                </div>

                <div class="source-page">
                    PAGE {page}
                </div>

            </div>

            <div class="source-reason">
                {reason}
            </div>

        </div>
        """
    )


# =========================================================
# DEMO INTRO
# =========================================================

def render_demo_intro():

    st.html(
        """
        <div class="demo-intro">

            <div>

                <div class="demo-title">
                    Try a demo scenario
                </div>

                <div class="demo-subtitle">
                    Start with a prepared case or describe
                    your own freelance situation.
                </div>

            </div>

            <div class="demo-label">
                3 PREPARED CASES
            </div>

        </div>
        """
    )


# =========================================================
# DEMO CARD
# =========================================================

def render_demo_card(
    title,
    description,
    tag,
):

    return f"""
        <div class="demo-card">

            <div class="demo-card-tag">
                {tag}
            </div>

            <div class="demo-card-title">
                {title}
            </div>

            <div class="demo-card-description">
                {description}
            </div>

        </div>
    """