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
# ========== 🔧 Fonctions utilitaires ==========

def evaluer_profil(age, risque, connaissance):
    score = 0
    if age < 35:
        score += 1
    if risque == "Élevée":
        score += 2
    elif risque == "Modérée":
        score += 1
    if connaissance == "Avancé":
        score += 2
    elif connaissance == "Intermédiaire":
        score += 1
    return score

# ========== 🔄 Mise à jour du Simulateur de Rendement avec Altair ==========
import altair as alt

if "📈 Simulateur de Rendement" in [tab.label for tab in tabs]:
    with tabs[2]:
        st.subheader("📊 Graphique interactif")
        df = pd.DataFrame({
            "Année": list(range(1, duree+1)),
            "Capital estimé ($)": historique
        })
        chart = alt.Chart(df).mark_line(point=True).encode(
            x='Année:O',
            y='Capital estimé ($):Q',
            tooltip=['Année', 'Capital estimé ($)']
        ).interactive()
        st.altair_chart(chart, use_container_width=True)

# ========== 🧮 Calculateur Retraite ==========

tabs.append(st.tab("🧓 Planification Retraite"))
with tabs[-1]:
    st.header("🧓 Planification Retraite")
    age_retraite = st.slider("À quel âge voulez-vous prendre votre retraite ?", 55, 70, 65)
    revenus_voulus = st.number_input("Revenu annuel désiré à la retraite ($)", value=40000)
    duree_retraite = 90 - age_retraite
    inflation = st.slider("Inflation estimée (%)", 1, 5, 2)

    besoin_total = 0
    for i in range(duree_retraite):
        besoin_total += revenus_voulus * ((1 + inflation/100) ** i)

    st.success(f"📊 Vous aurez besoin d’environ **{besoin_total:,.0f} $** pour {duree_retraite} ans de retraite.")

# ========== 🧠 Quiz amélioré aléatoire ==========
if "🧠 Quiz Financier" in [tab.label for tab in tabs]:
    with tabs[10]:
        st.header("🧠 Quiz Financier Amélioré")
        import random
        questions = [
            {"q": "Quel est l'objectif principal de la diversification ?", "r": "Minimiser les risques", "opts": ["Maximiser les rendements", "Minimiser les risques", "Augmenter les frais"]},
            {"q": "Que signifie ETF ?", "r": "Fonds négocié en bourse", "opts": ["Frais de trading", "Fonds négocié en bourse", "Épargne temporaire fixe"]},
            {"q": "C'est quoi un dividende ?", "r": "Une part des bénéfices reversée aux actionnaires", "opts": ["Une taxe", "Un prêt", "Une part des bénéfices reversée aux actionnaires"]}
        ]
        q = random.choice(questions)
        st.subheader(f"❓ {q['q']}")
        rep = st.radio("Votre réponse :", q["opts"])
        if rep:
            if rep == q["r"]:
                st.success("Bonne réponse ✅")
            else:
                st.error(f"Mauvaise réponse ❌. Bonne réponse : **{q['r']}**")

# ========== 🎯 Score Profil Investisseur ==========

if "📋 Profil Financier" in [tab.label for tab in tabs]:
    with tabs[0]:
        if submitted:
            score = evaluer_profil(age, risque, connaissance)
            st.markdown(f"### 🎯 **Score investisseur : {score}/5**")
            if score <= 2:
                st.warning("Profil prudent : idéal pour obligations ou fonds équilibrés.")
            elif score <= 4:
                st.info("Profil modéré : bon équilibre entre actions et obligations.")
            else:
                st.success("Profil dynamique : vous pouvez viser des rendements plus élevés.")
# ========== 📅 Planificateur d'Objectifs ==========
tabs.append(st.tab("🎯 Objectifs Financiers"))
with tabs[-1]:
    st.header("🎯 Planificateur d’Objectifs")
    objectifs = st.text_area("Listez vos objectifs (un par ligne)", "Acheter une maison\nFinancer les études\nVoyager")
    if objectifs:
        objectifs_list = objectifs.split("\n")
        delais = []
        for obj in objectifs_list:
            delais.append(st.slider(f"Combien d'années pour : {obj} ?", 1, 30, 5))
        st.write("### 🗓️ Résumé :")
        for o, d in zip(objectifs_list, delais):
            st.write(f"🔹 **{o}** dans **{d} ans**.")

# ========== 💸 Suivi du Budget Mensuel ==========
tabs.append(st.tab("💸 Suivi Budget"))
with tabs[-1]:
    st.header("💸 Suivi du Budget")
    revenus = st.number_input("💰 Revenus mensuels ($)", min_value=0)
    depenses = {
        "Logement": st.number_input("🏠 Logement", min_value=0),
        "Nourriture": st.number_input("🍽️ Nourriture", min_value=0),
        "Transport": st.number_input("🚗 Transport", min_value=0),
        "Divertissement": st.number_input("🎉 Divertissement", min_value=0),
        "Autres": st.number_input("🧾 Autres", min_value=0),
    }
    total_depenses = sum(depenses.values())
    reste = revenus - total_depenses
    st.metric("💼 Épargne potentielle", f"{reste:,.2f} $")
    fig2, ax2 = plt.subplots()
    ax2.pie(depenses.values(), labels=depenses.keys(), autopct='%1.1f%%')
    ax2.axis('equal')
    st.pyplot(fig2)

# ========== 🔔 Alertes de Portefeuille ==========
tabs.append(st.tab("🔔 Alertes"))
with tabs[-1]:
    st.header("🔔 Alertes personnalisées")
    valeur_seuil = st.number_input("Déclencher une alerte si la valeur d’un actif descend sous ($)", value=100)
    actif = st.text_input("Entrez le symbole boursier", value="AAPL")
    if st.button("Vérifier le seuil"):
        try:
            prix_actuel = yf.Ticker(actif).info["currentPrice"]
            st.write(f"📈 Prix actuel de {actif}: {prix_actuel} $")
            if prix_actuel < valeur_seuil:
                st.warning(f"⚠️ {actif} est sous le seuil de {valeur_seuil} $")
            else:
                st.success(f"✅ {actif} est au-dessus du seuil.")
        except:
            st.error("Erreur lors de la récupération du prix.")

# ========== 🧾 Générateur de Rapport PDF ==========
from fpdf import FPDF
import datetime

tabs.append(st.tab("📄 Rapport PDF"))
with tabs[-1]:
    st.header("📄 Générateur de Rapport Financier")
    if st.button("📥 Télécharger mon rapport"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Rapport Financier Personnel", ln=True, align="C")
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Date : {datetime.datetime.now().strftime('%d/%m/%Y')}", ln=True)
        pdf.cell(200, 10, txt=f"Âge : {age}", ln=True)
        pdf.cell(200, 10, txt=f"Objectif : {objectif}", ln=True)
        pdf.cell(200, 10, txt=f"Investissement mensuel : {investissement_mensuel} $", ln=True)
        pdf.cell(200, 10, txt=f"Durée : {duree} ans", ln=True)
        pdf.output("/tmp/rapport_financier.pdf")
        with open("/tmp/rapport_financier.pdf", "rb") as f:
            st.download_button("📤 Télécharger le PDF", f, file_name="rapport_financier.pdf")

# ========== 🌐 Convertisseur de Devises ==========
import requests

tabs.append(st.tab("💱 Convertisseur de Devises"))
with tabs[-1]:
    st.header("💱 Convertisseur")
    montant = st.number_input("Montant à convertir", value=100.0)
    from_devise = st.selectbox("De", ["USD", "CAD", "EUR", "GBP"])
    to_devise = st.selectbox("Vers", ["USD", "CAD", "EUR", "GBP"], index=1)
    if st.button("Convertir"):
        try:
            url = f"https://api.exchangerate.host/convert?from={from_devise}&to={to_devise}&amount={montant}"
            response = requests.get(url).json()
            st.success(f"{montant} {from_devise} = {response['result']:.2f} {to_devise}")
        except:
            st.error("Erreur lors de la conversion.")
