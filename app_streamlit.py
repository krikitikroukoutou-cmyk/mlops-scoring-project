import streamlit as st
import requests

st.set_page_config(page_title="Scoring Crédit", page_icon="💳")
st.title("💳 Simulateur de score de crédit")

API_URL = "http://localhost:8000/predict"  # sera remplacé par l'URL Cloud Run à l'Étape 8

with st.form("formulaire"):
    revolving = st.number_input("Taux d'utilisation du crédit renouvelable", 0.0, 2.0, 0.3)
    age = st.number_input("Âge", 18, 100, 35)
    late_30_59 = st.number_input("Nb retards 30-59 jours", 0, 20, 0)
    debt_ratio = st.number_input("Ratio d'endettement", 0.0, 5.0, 0.4)
    income = st.number_input("Revenu mensuel", 0, 50000, 3000)
    open_credit = st.number_input("Nb lignes de crédit ouvertes", 0, 50, 5)
    late_90 = st.number_input("Nb retards 90+ jours", 0, 20, 0)
    real_estate = st.number_input("Nb prêts immobiliers", 0, 10, 1)
    late_60_89 = st.number_input("Nb retards 60-89 jours", 0, 20, 0)
    dependents = st.number_input("Nb personnes à charge", 0, 10, 0)

    submit = st.form_submit_button("Calculer le score")

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
    response = requests.post(API_URL, json=payload)
    result = response.json()

    st.metric("Probabilité de défaut", f"{result['probabilite_defaut']*100:.1f}%")
    if result["prediction"] == 1:
        st.error("⚠️ Client à risque : crédit déconseillé")
    else:
        st.success("✅ Client fiable : crédit accordé")