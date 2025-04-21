import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np

# Configuration de la page Streamlit
st.set_page_config(page_title="Conseiller Financier Virtuel", layout="wide")
st.title("💼 Conseiller Financier Virtuel")

# Variables par défaut pour éviter les erreurs si le formulaire n'est pas soumis
age = 30
objectif = "Épargne retraite"
montant_initial = 1000
investissement_mensuel = 100
duree = 10
connaissance = "Débutant"
risque = "Modérée"
situation_familiale = "Célibataire"
epargne_urgence = "Oui"
preference_esg = False
horizon_liquidite = "Non"

# Onglets
tabs = st.tabs([
    "Profil Financier",
    "Suggestions de Portefeuille",
    "Simulateur de Rendement",
    "Comparateur de Fonds",
    "Recherche d'Actions",
    "FAQ",
    "Analyse Technique",
    "Glossaire",
    "Watchlist",
    "Simulation Monte Carlo",
    "Quiz Financier",
    "Cryptomonnaie"
])

# 1. Profil Financier
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

# 2. Suggestions de Portefeuille
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

# 3. Simulateur de Rendement
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

# 4. Comparateur de Fonds
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

# 5. Recherche d'Actions
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

# 6. FAQ
with tabs[5]:
    st.header("❓ Questions fréquentes")
    with st.expander("C'est quoi un ETF?"):
        st.write("Un ETF (Exchange Traded Fund) est un fonds qui regroupe plusieurs actifs, comme des actions ou des obligations, et qui se transige en bourse comme une action.")
    with st.expander("Comment fonctionne le risque?"):
        st.write("Plus le rendement espéré est élevé, plus le risque de pertes est grand.")
    with st.expander("À quelle fréquence investir?"):
        st.write("Investir de manière périodique (ex: chaque mois) permet de réduire le risque.")
    with st.expander("Faut-il avoir une épargne d’urgence?"):
        st.write("Oui, avant d’investir à long terme, il est important d’avoir un coussin de sécurité.")

# 7. Analyse Technique
with tabs[6]:
    st.header("📉 Analyse Technique (à venir)")
    st.info("Cette section permettra d'ajouter vos propres analyses à partir de données boursières historiques.")

# 8. Glossaire
with tabs[7]:
    st.header("📘 Glossaire Financier")
    st.markdown("**ETF** : Fonds négocié en bourse, panier d'actifs transigé comme une action.")
    st.markdown("**Fonds indiciel** : Réplique la performance d'un indice (ex : S&P 500).")
    st.markdown("**Diversification** : Répartir ses placements pour limiter les risques.")
    st.markdown("**Rendement** : Gain ou perte sur un investissement.")
    st.markdown("**Frais de gestion** : Coûts annuels d'un fonds, en pourcentage.")

# 9. Watchlist
with tabs[8]:
    st.header("📝 Ma Watchlist")
    watchlist = st.text_area("Ajouter des actions à suivre (séparées par des virgules)", "")
    if watchlist:
        actions = [action.strip() for action in watchlist.split(",")]
        st.write("### Liste de suivi :")
        st.write(", ".join(actions))

# 10. Simulation Monte Carlo
with tabs[9]:
    st.header("🔮 Simulation Monte Carlo")
    st.markdown("Simulez des rendements futurs pour vos investissements.")

    num_simulations = st.number_input("Nombre de simulations", min_value=100, max_value=10000, value=1000)
    volatilite = st.slider("Volatilité (%)", min_value=1, max_value=50, value=20)
    rendement_moyen = st.slider("Rendement moyen annuel (%)", min_value=1, max_value=20, value=8)

    simulation_results = []
    for _ in range(num_simulations):
        capital_final = montant_initial
        historique_simulation = [capital_final]
        for _ in range(duree):
            rendement = np.random.normal(rendement_moyen / 100, volatilite / 100)
            capital_final *= (1 + rendement)
            historique_simulation.append(capital_final)
        simulation_results.append(historique_simulation)

    fig, ax = plt.subplots()
    for simulation in simulation_results[:50]:
        ax.plot(simulation, alpha=0.3)
    st.pyplot(fig)

# 11. Quiz Financier
with tabs[10]:
    st.header("🧠 Quiz Financier")
    question = "Quel est l'objectif principal de la diversification ?"
    options = ["Maximiser les rendements", "Minimiser les risques", "Augmenter les frais"]
    response = st.radio(question, options)

    if response:
        if response == "Minimiser les risques":
            st.success("Bonne réponse! La diversification réduit les risques.")
        else:
            st.error("Mauvaise réponse. L'objectif est de **minimiser les risques**.")

# 12. Cryptomonnaie
with tabs[11]:
    st.header("💰 Cryptomonnaie")
    st.write("""
    La cryptomonnaie est une monnaie numérique sécurisée par cryptographie. 
    Exemples populaires : Bitcoin (BTC), Ethereum (ETH), Litecoin (LTC).
    """)
    st.write("**Bitcoin (BTC)** : La première et la plus célèbre des cryptomonnaies.")
    st.write("**Ethereum (ETH)** : Utilisé pour des applications décentralisées.")
    st.write("**Litecoin (LTC)** : Une alternative plus rapide au Bitcoin.")
