import streamlit as st


def inject_styles():
    st.html(
        """
        <style>

        /* =========================================================
           ROOT
        ========================================================= */

        :root {
            --ink: #14141A;
            --cream: #F2EFE6;
            --white: #FFFFFF;
            --teal: #1B435E;
            --teal-dark: #143449;
            --muted: #6B6B72;
            --line: #DDD9CF;
            --soft: #E9E5DA;
            --green: #356B58;
            --green-soft: #E8F0EC;
        }

        * {
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            margin: 0 !important;
            background: var(--cream) !important;
        }


        /* =========================================================
           REMOVE STREAMLIT CHROME
           ========================================================= */

        header[data-testid="stHeader"] {
            display: none !important;
        }

        [data-testid="stToolbar"] {
            display: none !important;
        }

        div[data-testid="stDecoration"] {
            display: none !important;
        }

        #MainMenu {
            display: none !important;
        }

        footer {
            display: none !important;
        }

        .stApp {
            margin-top: 0 !important;
            background: var(--cream) !important;
        }

        section.main {
            margin-top: 0 !important;
        }

        section.main > div {
            padding-top: 0 !important;
        }

        .block-container {
            max-width: 1180px !important;
            padding-top: 0.6rem !important;
            padding-bottom: 4rem !important;
        }


        /* =========================================================
           NAVBAR
           ========================================================= */

        .vf-navbar {
            width: 100%;
            height: 68px;

            display: flex;
            align-items: center;
            justify-content: space-between;

            padding: 0 4px;

            position: relative;
            z-index: 20;
        }

        .vf-brand {
            display: flex;
            align-items: center;
            gap: 11px;

            color: var(--ink);

            font-family: "IBM Plex Sans", sans-serif;
            font-size: 15px;
            font-weight: 700;
            letter-spacing: -0.01em;
        }

        .vf-brand-mark {
            width: 31px;
            height: 31px;

            border-radius: 50%;

            display: flex;
            align-items: center;
            justify-content: center;

            background: var(--ink);
            color: var(--cream);

            font-family: "IBM Plex Mono", monospace;
            font-size: 12px;
            font-weight: 600;
        }

        .vf-nav-pill {
            padding: 8px 13px;

            border: 1px solid var(--line);
            border-radius: 999px;

            color: var(--muted);

            background: rgba(255,255,255,0.45);

            font-family: "IBM Plex Mono", monospace;
            font-size: 10px;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }


        /* =========================================================
           HERO
           ========================================================= */

        .hero-shell {
            position: relative;
            overflow: hidden;

            width: 100%;
            min-height: 510px;

            margin-top: 8px;

            padding: 64px 58px 58px;

            border-radius: 28px;

            background:
                radial-gradient(
                    circle at 82% 22%,
                    rgba(48, 96, 121, 0.24),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 10% 90%,
                    rgba(255,255,255,0.08),
                    transparent 25%
                ),
                var(--ink);

            color: var(--white);

            box-shadow:
                0 22px 60px rgba(20,20,26,0.13);

            display: grid;

            grid-template-columns:
                minmax(0, 1.15fr)
                minmax(340px, 0.85fr);

            column-gap: 70px;

            align-items: center;
        }


        /* =========================================================
           HERO BACKGROUND
           ========================================================= */

        .hero-shell::before {
            content: "";

            position: absolute;
            inset: 0;

            opacity: 0.18;

            background-image:
                linear-gradient(
                    rgba(255,255,255,0.08) 1px,
                    transparent 1px
                ),
                linear-gradient(
                    90deg,
                    rgba(255,255,255,0.08) 1px,
                    transparent 1px
                );

            background-size: 46px 46px;

            mask-image:
                radial-gradient(
                    circle at 75% 45%,
                    black,
                    transparent 68%
                );

            pointer-events: none;
        }


        .hero-shell::after {
            content: "";

            position: absolute;

            width: 280px;
            height: 280px;

            right: 85px;
            top: 105px;

            border-radius: 50%;

            border: 1px solid rgba(255,255,255,0.12);

            box-shadow:
                0 0 0 32px rgba(255,255,255,0.025),
                0 0 0 64px rgba(255,255,255,0.018),
                0 0 0 96px rgba(255,255,255,0.012);

            pointer-events: none;
        }


        /* =========================================================
           HERO CONTENT
           ========================================================= */

        .hero-content {
            position: relative;

            z-index: 3;

            min-width: 0;

            max-width: 650px;
        }


        .hero-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 8px;

            margin-bottom: 20px;
            padding: 7px 11px;

            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 999px;

            background: rgba(255,255,255,0.055);

            color: rgba(255,255,255,0.68);

            font-family: "IBM Plex Mono", monospace;
            font-size: 10px;
            letter-spacing: 0.07em;
            text-transform: uppercase;
        }

        .hero-eyebrow-dot {
            width: 6px;
            height: 6px;

            border-radius: 50%;

            background: #9CC5D8;

            box-shadow:
                0 0 12px rgba(156,197,216,0.8);
        }


        .hero-title {
            margin: 0;

            max-width: 720px;

            color: white;

            font-family: "Lora", Georgia, serif;

            font-size: clamp(
                44px,
                5.2vw,
                72px
            );

            line-height: 0.98;

            font-weight: 500;

            letter-spacing: -0.055em;
        }

        .hero-title em {
            color: #A8C6D4;
            font-style: italic;
        }


        .hero-description {
            max-width: 560px;

            margin-top: 25px;

            color: rgba(255,255,255,0.66);

            font-family: "IBM Plex Sans", sans-serif;

            font-size: 16px;

            line-height: 1.65;
        }


        /* =========================================================
           HERO PIPELINE
           ========================================================= */

        .hero-flow {
            position: relative;

            z-index: 4;

            width: 100%;

            display: flex;
            flex-direction: column;

            gap: 10px;

            align-self: center;

            justify-self: stretch;
        }


        .hero-flow-card {
            display: flex;

            align-items: center;
            justify-content: space-between;

            width: 100%;

            padding: 15px 17px;

            border: 1px solid rgba(255,255,255,0.13);

            border-radius: 13px;

            background: rgba(255,255,255,0.065);

            backdrop-filter: blur(12px);

            transition:
                transform 0.2s ease,
                background 0.2s ease,
                border-color 0.2s ease;
        }


        .hero-flow-card:hover {
            transform: translateX(-4px);

            background: rgba(255,255,255,0.10);

            border-color:
                rgba(168,198,212,0.3);
        }


        .hero-flow-left {
            display: flex;

            align-items: center;

            gap: 11px;

            min-width: 0;
        }


        .hero-flow-number {
            width: 27px;
            height: 27px;

            display: flex;

            align-items: center;
            justify-content: center;

            flex: 0 0 27px;

            border-radius: 7px;

            background:
                rgba(168,198,212,0.12);

            color: #A8C6D4;

            font-family:
                "IBM Plex Mono", monospace;

            font-size: 9px;
        }


        .hero-flow-name {
            color:
                rgba(255,255,255,0.86);

            font-family:
                "IBM Plex Sans", sans-serif;

            font-size: 12px;

            font-weight: 600;
        }


        .hero-flow-status {
            color:
                rgba(255,255,255,0.4);

            font-family:
                "IBM Plex Mono", monospace;

            font-size: 9px;

            flex-shrink: 0;
        }


        /* =========================================================
           IMPORTANT:
           Floating hero chips removed completely.
           ========================================================= */


        /* =========================================================
           INPUT LABEL
           ========================================================= */

        .input-label {
            margin-top: 42px;
            margin-bottom: 10px;

            color: var(--ink);

            font-family:
                "IBM Plex Mono", monospace;

            font-size: 10px;

            font-weight: 600;

            letter-spacing: 0.08em;

            text-transform: uppercase;
        }


        /* =========================================================
           TEXTAREA
           ========================================================= */

        div[data-testid="stTextArea"] textarea {
            min-height: 155px !important;

            padding: 18px 20px !important;

            border:
                1px solid var(--line) !important;

            border-radius:
                17px !important;

            background:
                rgba(255,255,255,0.75) !important;

            color:
                var(--ink) !important;

            font-family:
                "IBM Plex Sans", sans-serif !important;

            font-size:
                15px !important;

            line-height:
                1.65 !important;

            box-shadow:
                none !important;

            transition:
                border-color 0.18s ease,
                box-shadow 0.18s ease !important;
        }


        div[data-testid="stTextArea"] textarea:focus {
            border-color:
                var(--teal) !important;

            box-shadow:
                0 0 0 3px
                rgba(27,67,94,0.08) !important;
        }


        div[data-testid="stTextArea"] textarea::placeholder {
            color: #99979A !important;
        }


        /* =========================================================
           BUTTONS
           ========================================================= */

        .stButton > button {
            min-height: 46px !important;

            padding: 0 20px !important;

            border:
                1px solid var(--ink) !important;

            border-radius:
                12px !important;

            background:
                var(--ink) !important;

            color:
                white !important;

            font-family:
                "IBM Plex Sans", sans-serif !important;

            font-size:
                13px !important;

            font-weight:
                600 !important;

            box-shadow:
                none !important;

            transition:
                transform 0.18s ease,
                box-shadow 0.18s ease,
                background-color 0.18s ease !important;
        }


        .stButton > button:hover {
            transform:
                translateY(-1px) !important;

            background:
                var(--teal-dark) !important;

            box-shadow:
                0 8px 22px
                rgba(20,20,26,0.13) !important;
        }


        .stButton > button:active {
            transform:
                translateY(0) !important;
        }


        .stButton > button:focus {
            box-shadow:
                0 0 0 3px
                rgba(27,67,94,0.12) !important;
        }


        /* =========================================================
           DEMO SECTION
           ========================================================= */

        .demo-intro {
            display: flex;

            align-items: flex-end;

            justify-content: space-between;

            margin-top: 35px;

            margin-bottom: 16px;
        }


        .demo-title {
            color: var(--ink);

            font-family:
                "Lora", Georgia, serif;

            font-size: 22px;

            font-weight: 500;

            letter-spacing: -0.025em;
        }


        .demo-subtitle {
            margin-top: 5px;

            color: var(--muted);

            font-family:
                "IBM Plex Sans", sans-serif;

            font-size: 12px;
        }


        .demo-label {
            color: var(--muted);

            font-family:
                "IBM Plex Mono", monospace;

            font-size: 9px;

            letter-spacing: 0.08em;

            text-transform: uppercase;
        }


        .demo-card {
            min-height: 150px;

            padding: 19px;

            border:
                1px solid var(--line);

            border-radius: 17px;

            background:
                rgba(255,255,255,0.68);

            transition:
                transform 0.18s ease,
                box-shadow 0.18s ease,
                border-color 0.18s ease;
        }


        .demo-card:hover {
            transform:
                translateY(-2px);

            border-color:
                #C9C4B8;

            box-shadow:
                0 12px 30px
                rgba(20,20,26,0.07);
        }


        .demo-card-tag {
            display: inline-block;

            margin-bottom: 18px;

            padding: 5px 7px;

            border-radius: 6px;

            background:
                var(--soft);

            color:
                var(--teal);

            font-family:
                "IBM Plex Mono", monospace;

            font-size: 8px;

            font-weight: 600;

            letter-spacing: 0.06em;
        }


        .demo-card-title {
            margin-bottom: 7px;

            color:
                var(--ink);

            font-family:
                "IBM Plex Sans", sans-serif;

            font-size: 14px;

            font-weight: 650;
        }


        .demo-card-description {
            color:
                var(--muted);

            font-family:
                "IBM Plex Sans", sans-serif;

            font-size: 11px;

            line-height: 1.5;
        }


        .demo-card + div .stButton > button {
            margin-top: 8px !important;

            min-height: 38px !important;

            border-color:
                var(--line) !important;

            background:
                transparent !important;

            color:
                var(--ink) !important;

            font-size:
                11px !important;
        }


        .demo-card + div .stButton > button:hover {
            background:
                white !important;

            border-color:
                #BBB6AA !important;
        }


        /* =========================================================
           PROCESSING
           ========================================================= */

        .processing-header {
            margin-top: 42px;
            margin-bottom: 20px;
        }


        .processing-title {
            color:
                var(--ink);

            font-family:
                "Lora", Georgia, serif;

            font-size:
                30px;

            font-weight:
                500;

            letter-spacing:
                -0.03em;
        }


        .processing-subtitle {
            margin-top: 5px;

            color:
                var(--muted);

            font-family:
                "IBM Plex Sans", sans-serif;

            font-size:
                12px;
        }


        .stage {
            display:
                flex;

            align-items:
                center;

            gap:
                14px;

            margin-bottom:
                9px;

            padding:
                13px 15px;

            border:
                1px solid var(--line);

            border-radius:
                13px;

            background:
                rgba(255,255,255,0.56);
        }


        .stage.active {
            border-color:
                #AABCC7;

            background:
                rgba(255,255,255,0.85);
        }


        .stage-number {
            width:
                28px;

            height:
                28px;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            flex:
                0 0 28px;

            border-radius:
                8px;

            background:
                var(--soft);

            color:
                var(--muted);

            font-family:
                "IBM Plex Mono", monospace;

            font-size:
                9px;
        }


        .stage.active .stage-number {
            background:
                var(--teal);

            color:
                white;
        }


        .stage-name {
            color:
                var(--ink);

            font-family:
                "IBM Plex Sans", sans-serif;

            font-size:
                12px;

            font-weight:
                600;
        }


        .stage-description {
            margin-top:
                2px;

            color:
                var(--muted);

            font-family:
                "IBM Plex Sans", sans-serif;

            font-size:
                10px;
        }


        /* =========================================================
           RESULT HEADER
           ========================================================= */

        .result-header {
            padding-top:
                24px;

            margin-bottom:
                22px;
        }


        .result-eyebrow {
            margin-bottom:
                9px;

            color:
                var(--teal);

            font-family:
                "IBM Plex Mono", monospace;

            font-size:
                9px;

            font-weight:
                600;

            letter-spacing:
                0.1em;

            text-transform:
                uppercase;
        }


        .result-title {
            color:
                var(--ink);

            font-family:
                "Lora", Georgia, serif;

            font-size:
                clamp(34px, 4vw, 52px);

            line-height:
                1.05;

            font-weight:
                500;

            letter-spacing:
                -0.045em;
        }


        .result-description {
            max-width:
                620px;

            margin-top:
                10px;

            color:
                var(--muted);

            font-family:
                "IBM Plex Sans", sans-serif;

            font-size:
                13px;

            line-height:
                1.6;
        }


        /* =========================================================
           RESULT CARD
           ========================================================= */

        .result-card {
            position:
                relative;

            overflow:
                hidden;

            padding:
                34px 38px;

            border-radius:
                22px;

            background:
                var(--ink);

            color:
                white;

            box-shadow:
                0 18px 48px
                rgba(20,20,26,0.14);
        }


        .result-card::after {
            content:
                "";

            position:
                absolute;

            width:
                230px;

            height:
                230px;

            right:
                -80px;

            top:
                -90px;

            border-radius:
                50%;

            border:
                1px solid
                rgba(255,255,255,0.08);

            box-shadow:
                0 0 0 28px
                rgba(255,255,255,0.025),
                0 0 0 56px
                rgba(255,255,255,0.015);
        }


        .result-label {
            position:
                relative;

            z-index:
                2;

            color:
                rgba(255,255,255,0.48);

            font-family:
                "IBM Plex Mono", monospace;

            font-size:
                9px;

            letter-spacing:
                0.08em;

            text-transform:
                uppercase;
        }


        .tax-amount {
            position:
                relative;

            z-index:
                2;

            margin-top:
                8px;

            color:
                white;

            font-family:
                "IBM Plex Mono", monospace;

            font-size:
                clamp(38px, 5vw, 62px);

            font-weight:
                500;

            letter-spacing:
                -0.06em;
        }


        .verification-badge {
            position:
                relative;

            z-index:
                2;

            display:
                inline-flex;

            align-items:
                center;

            margin-top:
                18px;

            padding:
                7px 10px;

            border-radius:
                999px;

            background:
                rgba(120,170,145,0.13);

            color:
                #B9D8C8;

            font-family:
                "IBM Plex Mono", monospace;

            font-size:
                9px;

            letter-spacing:
                0.04em;
        }


        /* =========================================================
           METRICS
           ========================================================= */

        .metric-card {
            padding:
                17px 18px;

            border:
                1px solid var(--line);

            border-radius:
                15px;

            background:
                rgba(255,255,255,0.58);
        }


        .metric-label {
            color:
                var(--muted);

            font-family:
                "IBM Plex Mono", monospace;

            font-size:
                8px;

            letter-spacing:
                0.06em;

            text-transform:
                uppercase;
        }


        .metric-value {
            margin-top:
                7px;

            color:
                var(--ink);

            font-family:
                "IBM Plex Mono", monospace;

            font-size:
                16px;

            font-weight:
                600;
        }


        /* =========================================================
           SECTION TITLES
           ========================================================= */

        .section-title {
            margin-top:
                34px;

            margin-bottom:
                12px;

            color:
                var(--ink);

            font-family:
                "Lora", Georgia, serif;

            font-size:
                21px;

            font-weight:
                500;

            letter-spacing:
                -0.025em;
        }


        /* =========================================================
           RULE CARD
           ========================================================= */

        .rule-card {
            padding:
                22px;

            border:
                1px solid var(--line);

            border-radius:
                17px;

            background:
                rgba(255,255,255,0.63);
        }


        .rule-row {
            display:
                flex;

            justify-content:
                space-between;

            gap:
                25px;

            padding:
                10px 0;

            border-bottom:
                1px solid #E6E2D9;
        }


        .rule-row:last-child {
            border-bottom:
                none;
        }


        .rule-label {
            color:
                var(--muted);

            font-family:
                "IBM Plex Mono", monospace;

            font-size:
                9px;

            text-transform:
                uppercase;
        }


        .rule-value {
            max-width:
                68%;

            color:
                var(--ink);

            font-family:
                "IBM Plex Sans", sans-serif;

            font-size:
                12px;

            line-height:
                1.5;

            text-align:
                right;
        }


        /* =========================================================
           CONDITIONS
           ========================================================= */

        .condition-card {
            margin-bottom:
                8px;

            padding:
                12px 14px;

            border-left:
                3px solid var(--teal);

            border-radius:
                0 10px 10px 0;

            background:
                rgba(255,255,255,0.58);

            color:
                var(--ink);

            font-family:
                "IBM Plex Sans", sans-serif;

            font-size:
                11px;

            line-height:
                1.55;
        }


        /* =========================================================
           VERIFICATION
           ========================================================= */

        .verification-card {
            padding:
                20px;

            border:
                1px solid #D6E2DC;

            border-radius:
                17px;

            background:
                var(--green-soft);
        }


        .verification-status {
            color:
                var(--green);

            font-family:
                "IBM Plex Mono", monospace;

            font-size:
                10px;

            font-weight:
                700;

            letter-spacing:
                0.06em;
        }


        .verification-summary {
            margin-top:
                8px;

            color:
                #42544B;

            font-family:
                "IBM Plex Sans", sans-serif;

            font-size:
                12px;

            line-height:
                1.6;
        }


        /* =========================================================
           CAVEAT
           ========================================================= */

        .caveat-card {
            margin-top:
                10px;

            padding:
                14px 16px;

            border:
                1px solid #DDD8C8;

            border-radius:
                13px;

            background:
                #F7F3E8;
        }


        .caveat-label {
            margin-bottom:
                5px;

            color:
                #85775C;

            font-family:
                "IBM Plex Mono", monospace;

            font-size:
                8px;

            font-weight:
                600;

            letter-spacing:
                0.08em;

            text-transform:
                uppercase;
        }


        .caveat-text {
            color:
                #5F5749;

            font-family:
                "IBM Plex Sans", sans-serif;

            font-size:
                11px;

            line-height:
                1.55;
        }


        /* =========================================================
           SOURCES
           ========================================================= */

        .source-card {
            display:
                flex;

            justify-content:
                space-between;

            gap:
                18px;

            margin-bottom:
                8px;

            padding:
                14px 16px;

            border:
                1px solid var(--line);

            border-radius:
                13px;

            background:
                rgba(255,255,255,0.58);
        }


        .source-file {
            color:
                var(--ink);

            font-family:
                "IBM Plex Mono", monospace;

            font-size:
                10px;

            font-weight:
                600;
        }


        .source-page {
            margin-top:
                4px;

            color:
                var(--muted);

            font-family:
                "IBM Plex Mono", monospace;

            font-size:
                8px;
        }


        .source-reason {
            max-width:
                55%;

            color:
                var(--muted);

            font-family:
                "IBM Plex Sans", sans-serif;

            font-size:
                10px;

            line-height:
                1.5;

            text-align:
                right;
        }


        /* =========================================================
           MOBILE
           ========================================================= */

        @media (max-width: 850px) {

            .block-container {
                padding-left:
                    15px !important;

                padding-right:
                    15px !important;
            }


            .hero-shell {
                min-height:
                    620px;

                padding:
                    42px 25px 35px;

                border-radius:
                    22px;

                display:
                    flex;

                flex-direction:
                    column;

                align-items:
                    stretch;

                gap:
                    38px;
            }


            .hero-content {
                max-width:
                    100%;
            }


            .hero-title {
                font-size:
                    44px;
            }


            .hero-description {
                font-size:
                    14px;
            }


            .hero-flow {
                position:
                    relative;

                left:
                    auto;

                right:
                    auto;

                bottom:
                    auto;

                width:
                    100%;
            }


            .hero-shell::after {
                right:
                    -100px;

                top:
                    60px;
            }


            .demo-intro {
                display:
                    block;
            }


            .demo-label {
                margin-top:
                    8px;
            }


            .result-card {
                padding:
                    27px 24px;
            }


            .rule-row {
                display:
                    block;
            }


            .rule-value {
                max-width:
                    100%;

                margin-top:
                    5px;

                text-align:
                    left;
            }


            .source-card {
                display:
                    block;
            }


            .source-reason {
                max-width:
                    100%;

                margin-top:
                    8px;

                text-align:
                    left;
            }
        }

        </style>
        """
    )