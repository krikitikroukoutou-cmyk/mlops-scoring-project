import streamlit as st
import requests

# ============================================================
#  CONFIG PAGE
# ============================================================
st.set_page_config(
    page_title="Nexus Credit | AI Scoring Engine",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_URL = "https://scoring-api-lvnj.onrender.com/predict"  # sera remplacé par l'URL Cloud Run à l'Étape 8

# ============================================================
#  STYLE — Dark FinTech / Glassmorphism / Futuriste
# ============================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css');

    /* ============================================================
       DESIGN TOKENS
    ============================================================ */
    :root{
        --nx-bg-0: #05060f;
        --nx-bg-1: #0a0d1e;
        --nx-bg-2: #0d1128;
        --nx-surface: rgba(18, 22, 46, 0.55);
        --nx-surface-strong: rgba(20, 24, 52, 0.72);
        --nx-border: rgba(140, 150, 255, 0.16);
        --nx-border-strong: rgba(140, 150, 255, 0.32);
        --nx-text: #eef0ff;
        --nx-text-soft: #9aa0c7;
        --nx-text-faint: #6a7099;

        --nx-blue: #3d6bff;
        --nx-violet: #8b5cf6;
        --nx-cyan: #22d3ee;
        --nx-turquoise: #14e6c8;

        --nx-success: #1fe0a0;
        --nx-success-bg: rgba(31, 224, 160, 0.10);
        --nx-danger: #ff4d6d;
        --nx-danger-bg: rgba(255, 77, 109, 0.10);
        --nx-warning: #ffb84d;

        --nx-radius-xl: 28px;
        --nx-radius-lg: 20px;
        --nx-radius-md: 14px;
        --nx-radius-sm: 10px;

        --nx-shadow-soft: 0 8px 32px -8px rgba(0,0,0,0.55);
        --nx-shadow-glow-blue: 0 0 40px -8px rgba(61,107,255,0.45);
        --nx-shadow-glow-violet: 0 0 40px -8px rgba(139,92,246,0.40);
    }

    html, body, [class*="css"]{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    #MainMenu, header, footer {visibility: hidden;}
    div[data-testid="stToolbar"] {display: none;}
    div[data-testid="stDecoration"] {display: none;}

    /* ============================================================
       BACKGROUND — deep space fintech scene
    ============================================================ */
    .stApp{
        background:
            radial-gradient(circle 900px at 12% 8%, rgba(61,107,255,0.22), transparent 60%),
            radial-gradient(circle 900px at 90% 15%, rgba(139,92,246,0.20), transparent 55%),
            radial-gradient(circle 800px at 50% 100%, rgba(20,230,200,0.14), transparent 55%),
            repeating-linear-gradient(0deg, rgba(140,150,255,0.035) 0px, rgba(140,150,255,0.035) 1px, transparent 1px, transparent 42px),
            repeating-linear-gradient(90deg, rgba(140,150,255,0.035) 0px, rgba(140,150,255,0.035) 1px, transparent 1px, transparent 42px),
            linear-gradient(180deg, var(--nx-bg-0) 0%, var(--nx-bg-1) 45%, var(--nx-bg-2) 100%);
    }

    .block-container{ padding-top: 2rem; }

    /* ============================================================
       HERO
    ============================================================ */
    .nx-hero{
        text-align:center;
        padding: 20px 20px 26px 20px;
        margin-bottom: 6px;
        animation: nx-fade-up .7s ease both;
    }
    .nx-hero-badge{
        display:inline-flex;
        align-items:center;
        gap:8px;
        padding: 7px 18px;
        border-radius: 999px;
        background: var(--nx-surface);
        border: 1px solid var(--nx-border-strong);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        color: var(--nx-cyan);
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 22px;
        box-shadow: var(--nx-shadow-glow-blue);
    }
    .nx-hero-badge .nx-dot{
        width: 7px; height: 7px; border-radius: 50%;
        background: var(--nx-turquoise);
        box-shadow: 0 0 10px var(--nx-turquoise);
        animation: nx-pulse 1.8s ease-in-out infinite;
    }
    .nx-hero h1{
        font-family: 'Sora', sans-serif;
        font-size: 3.1rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.1;
        margin-bottom: 14px;
        background: linear-gradient(120deg, #ffffff 10%, var(--nx-cyan) 45%, var(--nx-violet) 75%, var(--nx-blue) 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: nx-shine 6s linear infinite;
    }
    .nx-hero p{
        color: var(--nx-text-soft);
        font-size: 1.12rem;
        font-weight: 500;
        max-width: 620px;
        margin: 0 auto 26px auto;
    }

    .nx-hero-stats{
        display:flex;
        justify-content:center;
        gap: 14px;
        flex-wrap: wrap;
    }
    .nx-stat-pill{
        display:flex;
        align-items:center;
        gap:10px;
        padding: 12px 20px;
        border-radius: var(--nx-radius-md);
        background: var(--nx-surface);
        border: 1px solid var(--nx-border);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        transition: transform .25s ease, border-color .25s ease;
    }
    .nx-stat-pill:hover{ transform: translateY(-3px); border-color: var(--nx-border-strong); }
    .nx-stat-pill i{ color: var(--nx-cyan); font-size: 1.1rem; }
    .nx-stat-pill .nx-stat-label{ color: var(--nx-text-soft); font-size: 0.82rem; font-weight: 500; }
    .nx-stat-pill .nx-stat-value{ color: var(--nx-text); font-size: 0.92rem; font-weight: 700; }

    @keyframes nx-shine{
        to{ background-position: 200% center; }
    }
    @keyframes nx-pulse{
        0%,100%{ opacity:1; transform: scale(1); }
        50%{ opacity:0.4; transform: scale(0.75); }
    }
    @keyframes nx-fade-up{
        from{ opacity:0; transform: translateY(18px); }
        to{ opacity:1; transform: translateY(0); }
    }

    /* ============================================================
       SECTION TITLES INSIDE FORM
    ============================================================ */
    .nx-section-title{
        display:flex;
        align-items:center;
        gap:12px;
        font-family: 'Sora', sans-serif;
        font-weight:700;
        font-size:1.02rem;
        color: var(--nx-text);
        margin: 4px 0 18px 0;
        padding-bottom: 14px;
        border-bottom: 1px solid var(--nx-border);
    }
    .nx-section-title .nx-icon-badge{
        display:flex; align-items:center; justify-content:center;
        width: 38px; height: 38px;
        border-radius: 12px;
        background: linear-gradient(135deg, rgba(61,107,255,0.25), rgba(139,92,246,0.25));
        border: 1px solid var(--nx-border-strong);
        color: var(--nx-cyan);
        font-size: 1rem;
        flex-shrink: 0;
    }
    .nx-section-title .nx-section-sub{
        display:block;
        font-weight: 400;
        font-size: 0.8rem;
        color: var(--nx-text-faint);
        margin-top: 2px;
        text-transform: none;
        letter-spacing: 0;
    }

    /* ============================================================
       FORM CARD (glass)
    ============================================================ */
    div[data-testid="stForm"]{
        background: var(--nx-surface);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--nx-border);
        border-radius: var(--nx-radius-xl);
        box-shadow: var(--nx-shadow-soft);
        padding: 34px 38px 22px 38px;
        position: relative;
        overflow: hidden;
        animation: nx-fade-up .8s ease both;
        animation-delay: .1s;
    }
    div[data-testid="stForm"]::before{
        content:"";
        position:absolute; top:0; left:0; right:0; height:3px;
        background: linear-gradient(90deg, var(--nx-blue), var(--nx-violet), var(--nx-cyan));
        background-size: 200% auto;
        animation: nx-shine 5s linear infinite;
    }
    div[data-testid="stForm"]::after{
        content:"";
        position:absolute; inset:0;
        border-radius: var(--nx-radius-xl);
        padding: 1px;
        pointer-events:none;
        background: linear-gradient(135deg, rgba(255,255,255,0.08), transparent 40%);
    }

    /* ---------- Inputs ---------- */
    div[data-testid="stNumberInput"] label{
        font-weight:600 !important;
        color: var(--nx-text-soft) !important;
        font-size:0.84rem !important;
        letter-spacing: 0.01em;
    }
    div[data-testid="stNumberInput"] input{
        border-radius: var(--nx-radius-sm) !important;
        border: 1px solid var(--nx-border) !important;
        background: rgba(8, 10, 26, 0.55) !important;
        color: var(--nx-text) !important;
        transition: all .2s ease !important;
    }
    div[data-testid="stNumberInput"] input:hover{
        border-color: var(--nx-border-strong) !important;
    }
    div[data-testid="stNumberInput"] input:focus{
        border-color: var(--nx-cyan) !important;
        box-shadow: 0 0 0 3px rgba(34,211,238,0.18) !important;
    }
    div[data-testid="stNumberInput"] button{
        background: rgba(255,255,255,0.04) !important;
        border-color: var(--nx-border) !important;
        color: var(--nx-text-soft) !important;
    }

    /* ---------- Submit button ---------- */
    button[kind="formSubmit"]{
        width: 100%;
        border: none !important;
        border-radius: var(--nx-radius-md) !important;
        padding: 0.85rem 1rem !important;
        font-weight: 700 !important;
        font-size: 1.02rem !important;
        letter-spacing: 0.02em;
        color: #ffffff !important;
        background: linear-gradient(120deg, var(--nx-blue), var(--nx-violet), var(--nx-cyan)) !important;
        background-size: 200% auto !important;
        box-shadow: 0 10px 30px -8px rgba(61,107,255,0.55) !important;
        transition: transform .2s ease, box-shadow .2s ease, background-position .5s ease !important;
        margin-top: 14px;
    }
    button[kind="formSubmit"]:hover{
        transform: translateY(-3px);
        background-position: 100% center !important;
        box-shadow: 0 16px 38px -8px rgba(139,92,246,0.65) !important;
    }
    button[kind="formSubmit"]:active{
        transform: translateY(-1px) scale(0.99);
    }

    /* ============================================================
       RESULT CARD
    ============================================================ */
    .nx-result-card{
        background: var(--nx-surface-strong);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--nx-border);
        border-radius: var(--nx-radius-xl);
        box-shadow: var(--nx-shadow-soft);
        padding: 34px 38px;
        margin-top: 26px;
        position: relative;
        overflow: hidden;
        animation: nx-fade-up .5s ease both;
    }
    .nx-result-card.nx-danger::before{ background: linear-gradient(90deg, var(--nx-danger), #ff8a65, var(--nx-danger)); }
    .nx-result-card.nx-success::before{ background: linear-gradient(90deg, var(--nx-success), var(--nx-turquoise), var(--nx-success)); }
    .nx-result-card::before{
        content:"";
        position:absolute; top:0; left:0; right:0; height:3px;
        background-size: 200% auto;
        animation: nx-shine 5s linear infinite;
    }

    .nx-result-header{
        display:flex;
        align-items:center;
        gap: 12px;
        margin-bottom: 26px;
        color: var(--nx-text-faint);
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .nx-gauge-wrap{
        display:flex;
        flex-direction: column;
        align-items:center;
        justify-content:center;
        gap: 6px;
    }
    .nx-gauge-value{
        font-family: 'Sora', sans-serif;
        font-size: 2.6rem;
        font-weight: 800;
    }
    .nx-gauge-label{
        color: var(--nx-text-faint);
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .nx-verdict-title{
        font-family: 'Sora', sans-serif;
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 8px;
        display:flex; align-items:center; gap:10px;
    }
    .nx-verdict-desc{
        color: var(--nx-text-soft);
        font-size: 0.95rem;
        line-height: 1.5;
        margin-bottom: 18px;
    }

    .nx-badge{
        display:inline-flex;
        align-items:center;
        gap:8px;
        padding: 9px 18px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.88rem;
    }
    .nx-badge-success{ background: var(--nx-success-bg); color: var(--nx-success); border: 1px solid rgba(31,224,160,0.35); }
    .nx-badge-error{ background: var(--nx-danger-bg); color: var(--nx-danger); border: 1px solid rgba(255,77,109,0.35); }

    .nx-mini-stats{
        display:flex;
        gap: 12px;
        margin-top: 22px;
        flex-wrap: wrap;
    }
    .nx-mini-stat{
        flex: 1;
        min-width: 140px;
        padding: 14px 16px;
        border-radius: var(--nx-radius-sm);
        background: rgba(255,255,255,0.03);
        border: 1px solid var(--nx-border);
    }
    .nx-mini-stat .nx-mini-label{
        color: var(--nx-text-faint);
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }
    .nx-mini-stat .nx-mini-value{
        color: var(--nx-text);
        font-size: 1.05rem;
        font-weight: 700;
        font-family: 'Sora', sans-serif;
    }

    /* ---------- Error card ---------- */
    div[data-testid="stAlert"]{
        background: var(--nx-danger-bg) !important;
        border: 1px solid rgba(255,77,109,0.35) !important;
        border-radius: var(--nx-radius-md) !important;
        color: var(--nx-text) !important;
    }

    /* ---------- Responsive ---------- */
    @media (max-width: 768px){
        .nx-hero h1{ font-size: 2.1rem; }
        div[data-testid="stForm"]{ padding: 24px 20px 16px 20px; }
        .nx-result-card{ padding: 24px 20px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
#  HERO
# ============================================================
st.markdown(
    """
    <div class="nx-hero">
        <div class="nx-hero-badge"><span class="nx-dot"></span> Moteur d'IA de scoring en temps réel</div>
        <h1>Nexus Credit Intelligence</h1>
        <p>Estimez instantanément la probabilité de défaut d'un client grâce à un modèle
        de scoring alimenté par l'intelligence artificielle.</p>
        <div class="nx-hero-stats">
            <div class="nx-stat-pill"><i class="fa-solid fa-bolt"></i>
                <div><div class="nx-stat-value">Temps réel</div><div class="nx-stat-label">Réponse instantanée</div></div>
            </div>
            <div class="nx-stat-pill"><i class="fa-solid fa-shield-halved"></i>
                <div><div class="nx-stat-value">Sécurisé</div><div class="nx-stat-label">Données chiffrées</div></div>
            </div>
            <div class="nx-stat-pill"><i class="fa-solid fa-brain"></i>
                <div><div class="nx-stat-value">IA Scoring</div><div class="nx-stat-label">Modèle prédictif</div></div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
#  FORMULAIRE
# ============================================================
with st.form("formulaire"):

    st.markdown(
        """
        <div class="nx-section-title">
            <div class="nx-icon-badge"><i class="fa-solid fa-user"></i></div>
            <div>Profil du client<span class="nx-section-sub">Informations personnelles de base</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input("Âge", 18, 100, 35)
    with c2:
        dependents = st.number_input("Nb personnes à charge", 0, 10, 0)
    with c3:
        income = st.number_input("Revenu mensuel", 0, 50000, 3000)

    st.markdown(
        """
        <div class="nx-section-title">
            <div class="nx-icon-badge"><i class="fa-solid fa-sack-dollar"></i></div>
            <div>Situation financière<span class="nx-section-sub">Endettement et lignes de crédit</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c4, c5, c6 = st.columns(3)
    with c4:
        revolving = st.number_input("Taux d'utilisation du crédit renouvelable", 0.0, 2.0, 0.3)
    with c5:
        debt_ratio = st.number_input("Ratio d'endettement", 0.0, 5.0, 0.4)
    with c6:
        open_credit = st.number_input("Nb lignes de crédit ouvertes", 0, 50, 5)

    st.markdown(
        """
        <div class="nx-section-title">
            <div class="nx-icon-badge"><i class="fa-solid fa-clock-rotate-left"></i></div>
            <div>Historique de paiement<span class="nx-section-sub">Retards et prêts en cours</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c7, c8, c9, c10 = st.columns(4)
    with c7:
        late_30_59 = st.number_input("Nb retards 30-59 jours", 0, 20, 0)
    with c8:
        late_60_89 = st.number_input("Nb retards 60-89 jours", 0, 20, 0)
    with c9:
        late_90 = st.number_input("Nb retards 90+ jours", 0, 20, 0)
    with c10:
        real_estate = st.number_input("Nb prêts immobiliers", 0, 10, 1)

    submit = st.form_submit_button("✨ Calculer le score de crédit")

# ============================================================
#  APPEL API + RÉSULTAT
# ============================================================
if submit:
    payload = {
        "RevolvingUtilizationOfUnsecuredLines": revolving,
        "age": age,
        "NumberOfTime30_59DaysPastDueNotWorse": late_30_59,
        "DebtRatio": debt_ratio,
        "MonthlyIncome": income,
        "NumberOfOpenCreditLinesAndLoans": open_credit,
        "NumberOfTimes90DaysLate": late_90,
        "NumberRealEstateLoansOrLines": real_estate,
        "NumberOfTime60_89DaysPastDueNotWorse": late_60_89,
        "NumberOfDependents": dependents,
        "DebtToIncome": debt_ratio * income,
    }

    try:
        response = requests.post(API_URL, json=payload)
        result = response.json()

        proba = result["probabilite_defaut"]
        prediction = result["prediction"]
        proba_pct = max(0.0, min(1.0, proba)) * 100

        is_risk = prediction == 1
        card_class = "nx-danger" if is_risk else "nx-success"
        accent_color = "var(--nx-danger)" if is_risk else "var(--nx-success)"

        # --- gauge geometry (SVG circle) ---
        radius = 70
        circumference = 2 * 3.14159265 * radius
        offset = circumference * (1 - proba_pct / 100)

        gauge_svg = (
            f'<svg width="180" height="180" viewBox="0 0 180 180">'
            f'<circle cx="90" cy="90" r="{radius}" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="14"/>'
            f'<circle cx="90" cy="90" r="{radius}" fill="none" stroke="{accent_color}" stroke-width="14" '
            f'stroke-linecap="round" stroke-dasharray="{circumference:.2f}" stroke-dashoffset="{offset:.2f}" '
            f'transform="rotate(-90 90 90)" '
            f'style="transition: stroke-dashoffset 1s ease; filter: drop-shadow(0 0 8px {accent_color});"/>'
            f'</svg>'
        )

        st.markdown(f'<div class="nx-result-card {card_class}">', unsafe_allow_html=True)

        st.markdown(
            """
            <div class="nx-result-header">
                <i class="fa-solid fa-chart-pie"></i> Résultat de l'analyse IA
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_gauge, col_verdict = st.columns([1, 2])

        with col_gauge:
            gauge_html = (
                f'<div class="nx-gauge-wrap">'
                f'<div style="position:relative; display:flex; align-items:center; justify-content:center;">'
                f'{gauge_svg}'
                f'<div style="position:absolute; text-align:center;">'
                f'<div class="nx-gauge-value" style="color:{accent_color};">{proba_pct:.1f}%</div>'
                f'</div>'
                f'</div>'
                f'<div class="nx-gauge-label">Probabilité de défaut</div>'
                f'</div>'
            )
            st.markdown(gauge_html, unsafe_allow_html=True)

        with col_verdict:
            if is_risk:
                st.markdown(
                    f"""
                    <div class="nx-verdict-title" style="color:{accent_color};">
                        <i class="fa-solid fa-triangle-exclamation"></i> Client à risque
                    </div>
                    <div class="nx-verdict-desc">
                        Le modèle estime un risque de défaut élevé pour ce profil. Une analyse
                        complémentaire ou des garanties additionnelles sont recommandées avant
                        toute décision d'octroi de crédit.
                    </div>
                    <span class="nx-badge nx-badge-error"><i class="fa-solid fa-xmark"></i> Crédit déconseillé</span>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="nx-verdict-title" style="color:{accent_color};">
                        <i class="fa-solid fa-circle-check"></i> Client fiable
                    </div>
                    <div class="nx-verdict-desc">
                        Le modèle estime un risque de défaut faible pour ce profil. Les indicateurs
                        financiers et l'historique de paiement sont favorables à l'octroi du crédit.
                    </div>
                    <span class="nx-badge nx-badge-success"><i class="fa-solid fa-check"></i> Crédit accordé</span>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown(
                f"""
                <div class="nx-mini-stats">
                    <div class="nx-mini-stat">
                        <div class="nx-mini-label">Revenu mensuel</div>
                        <div class="nx-mini-value">{income:,} €</div>
                    </div>
                    <div class="nx-mini-stat">
                        <div class="nx-mini-label">Ratio d'endettement</div>
                        <div class="nx-mini-value">{debt_ratio:.2f}</div>
                    </div>
                    <div class="nx-mini-stat">
                        <div class="nx-mini-label">Lignes de crédit</div>
                        <div class="nx-mini-value">{open_credit}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    except requests.exceptions.RequestException as e:
        st.markdown('<div class="nx-result-card nx-danger">', unsafe_allow_html=True)
        st.error(f"❌ Impossible de contacter l'API de scoring : {e}")
        st.markdown("</div>", unsafe_allow_html=True)