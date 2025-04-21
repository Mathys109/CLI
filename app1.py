import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

st.set_page_config(page_title="Conseiller Financier Virtuel", layout="wide")

st.title("💼 Conseiller Financier Virtuel")

# Onglets pour organiser l'application
tabs = st.tabs([
    "Profil Financier",
    "Suggestions de Portefeuille",
    "Simulateur de Rendement",
    "Comparateur de Fonds",
    "Recherche d'Actions",
    "FAQ",
    "Analyse Technique",
    "Glossaire"
])

# ------------------------
# 1. PROFIL FINANCIER
# ------------------------
with tabs[0]:
    st.header("📋 Profil Financier")
    with st.form("profil_form"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Âge", min_value=18, max_value=100, value=30)
            objectif = st.selectbox("Objectif d'investissement", ["Épargne retraite", "Achat maison", "Voyage", "Revenus passifs", "Autre"])
            montant_initial = st.number_input("Montant disponible à investir maintenant ($)", min_value=0)
            investissement_mensuel = st.number_input("Montant investi chaque mois ($)", min_value=0)
            duree = st.slider("Durée de l'investissement (en années)", 1, 50, 10)
            connaissance = st.select_slider("Connaissances en finance", options=["Débutant", "Intermédiaire", "Avancé"])
        with col2:
            risque = st.select_slider("Tolérance au risque", options=["Faible", "Modérée", "Élevée"])
            situation_familiale = st.selectbox("Situation familiale", ["Célibataire", "Marié(e)", "Avec enfants", "Sans enfants"])
            epargne_urgence = st.radio("Avez-vous une épargne d'urgence?", ["Oui", "Non"])
            preference_esg = st.checkbox("Je préfère des investissements responsables (ESG)")
            horizon_liquidite = st.radio("Avez-vous besoin de liquidité à court terme?", ["Oui", "Non"])

        submitted = st.form_submit_button("Analyser mon profil")

    if submitted:
        st.success("✅ Profil analysé avec succès!")
        st.write("### Résumé de votre profil :")
        st.json({
            "Âge": age,
            "Objectif": objectif,
            "Montant initial": montant_initial,
            "Investissement mensuel": investissement_mensuel,
            "Durée": duree,
            "Tolérance au risque": risque,
            "Situation familiale": situation_familiale,
            "Épargne d'urgence": epargne_urgence,
            "Préférence ESG": preference_esg,
            "Connaissances financières": connaissance,
            "Besoin de liquidité court terme": horizon_liquidite
        })

# ------------------------
# 2. SUGGESTIONS DE PORTEFEUILLE
# ------------------------
with tabs[1]:
    st.header("📊 Suggestions de Portefeuille")
    st.markdown("Voici un exemple de répartition suggérée :")

    labels = ["Actions canadiennes", "Actions internationales", "Obligations", "Fonds ESG"]
    if risque == "Faible":
        sizes = [20, 20, 50, 10]
    elif risque == "Modérée":
        sizes = [35, 35, 20, 10]
    else:
        sizes = [50, 35, 5, 10]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

# ------------------------
# 3. SIMULATEUR DE RENDEMENT
# ------------------------
with tabs[2]:
    st.header("📈 Simulateur de Rendement")
    taux = st.slider("Taux de rendement annuel (%)", 1, 15, 5)
    capital = montant_initial
    historique = []
    for annee in range(duree):
        capital = capital * (1 + taux / 100) + 12 * investissement_mensuel
        historique.append(capital)

    st.line_chart(historique)
    st.metric("Montant estimé à terme", f"{capital:,.2f} $")

# ------------------------
# 4. COMPARATEUR DE FONDS
# ------------------------
with tabs[3]:
    st.header("🔍 Comparateur de Fonds")
    fond1 = st.selectbox("Choisir un premier fonds", ["VEQT", "XEQT", "VCNS", "VGRO"])
    fond2 = st.selectbox("Choisir un deuxième fonds", ["VEQT", "XEQT", "VCNS", "VGRO"], index=1)

    donnees_fonds = {
        "VEQT": {"Rendement moyen": "8%", "Risque": "Élevé", "Frais": "0.25%"},
        "XEQT": {"Rendement moyen": "7.8%", "Risque": "Élevé", "Frais": "0.20%"},
        "VCNS": {"Rendement moyen": "5%", "Risque": "Faible", "Frais": "0.25%"},
        "VGRO": {"Rendement moyen": "6.5%", "Risque": "Modéré", "Frais": "0.25%"},
    }

    st.write(f"### 📌 {fond1}")
    st.json(donnees_fonds[fond1])
    st.write(f"### 📌 {fond2}")
    st.json(donnees_fonds[fond2])

# ------------------------
# 5. RECHERCHE D'ACTIONS
# ------------------------
with tabs[4]:
    st.header("📊 Recherche d'Actions")
    ticker = st.text_input("Entrez le symbole boursier (ex: AAPL, TSLA, MSFT)")
    if ticker:
        try:
            data = yf.Ticker(ticker)
            info = data.info
            st.subheader(info.get("longName", ticker))
            st.write(f"📈 Prix actuel: ${info.get('currentPrice', 'N/A')}")
            st.write(f"🏢 Secteur: {info.get('sector', 'N/A')}")
            st.write(f"📊 Capitalisation boursière: {info.get('marketCap', 'N/A')}")
            st.write(f"📅 Date de création: {info.get('fundFamily', 'N/A')}")
            st.write(f"💰 Dividende: {info.get('dividendYield', 'N/A')}")
            st.write(f"🔍 Description: {info.get('longBusinessSummary', 'N/A')}")
        except Exception as e:
            st.error("Erreur lors de la récupération des données. Vérifiez le symbole.")

# ------------------------
# 6. FAQ
# ------------------------
with tabs[5]:
    st.header("❓ Questions fréquentes")
    with st.expander("C'est quoi un ETF?"):
        st.write("Un ETF (Exchange Traded Fund) est un fonds qui regroupe plusieurs actifs, comme des actions ou des obligations, et qui se transige en bourse comme une action.")

    with st.expander("Comment fonctionne le risque?"):
        st.write("Plus le rendement espéré est élevé, plus le risque de pertes est grand. C’est pourquoi il faut bien connaître son profil d’investisseur.")

    with st.expander("À quelle fréquence investir?"):
        st.write("Investir de manière périodique (ex: chaque mois) permet de réduire le risque en lissant les fluctuations du marché.")

    with st.expander("Faut-il avoir une épargne d’urgence?"):
        st.write("Oui, avant d’investir à long terme, il est important d’avoir un coussin d’épargne équivalent à 3 à 6 mois de dépenses.")

# ------------------------
# 7. ANALYSE TECHNIQUE
# ------------------------
with tabs[6]:
    st.header("📉 Analyse Technique (à venir)")
    st.info("Cette section permettra d'ajouter vos propres analyses à partir de données boursières historiques.")

# ------------------------
# 8. GLOSSAIRE
# ------------------------
with tabs[7]:
    st.header("📘 Glossaire Financier")
    st.markdown("Voici quelques termes importants pour mieux comprendre la finance :")
    st.write("**ETF** : Fonds négocié en bourse, panier d'actifs transigé comme une action.")
    st.write("**Fonds indiciel** : Fonds qui réplique la performance d'un indice (ex : S&P 500).")
    st.write("**Diversification** : Répartition des investissements pour limiter les risques.")
    st.write("**Rendement** : Gain ou perte générée par un investissement sur une période donnée.")
    st.write("**Frais de gestion** : Coûts annuels prélevés par un fonds, exprimés en pourcentage.")
