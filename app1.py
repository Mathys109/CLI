# app.py
import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="Gestion Financière", layout="wide")

# Menu latéral
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Choisir une section", 
                           ["Calculateur d'Intérêts", "Portefeuille", "Watchlist", "Informations Financières", "Profil Financier"])

# Fonction pour calculer les intérêts composés
def calculer_capital(montant, taux, duree, type_invest="Actions"):
    capital = 0
    evolution = []
    for annee in range(1, duree + 1):
        taux_ajuste = taux / 100 * (1.2 if type_invest == "Actions" else 0.8)
        capital = (capital + montant) * (1 + taux_ajuste)
        evolution.append((annee, round(capital, 2)))
    return pd.DataFrame(evolution, columns=["Année", "Capital accumulé"])

# Fonction pour calculer la volatilité et la VaR
def calculer_risque(historique):
    try:
        rendements = historique.pct_change().dropna()
        if len(rendements) < 2:
            return "N/A", "N/A"
        volatilite = rendements.std() * np.sqrt(252)  # Annualisée
        var = np.percentile(rendements, 5)  # VaR à 95%
        return volatilite, var
    except:
        return "N/A", "N/A"

# Fonction pour rechercher un symbole depuis un nom
@st.cache_data
def trouver_symbole(nom_ou_symbole):
    nom_ou_symbole = nom_ou_symbole.strip().upper()
    if len(nom_ou_symbole) <= 5:
        return nom_ou_symbole  # Probablement un symbole
    try:
        recherche = yf.Ticker(nom_ou_symbole)
        if recherche:
            return nom_ou_symbole
    except:
        pass
    return nom_ou_symbole

# Suggestions d'actifs populaires
suggestions = ["AAPL", "MSFT", "TSLA", "GOOGL", "AMZN", "VTI", "SPY", "XIC.TO", "QQQ"]

# Création du Profil Financier
def creer_profil():
    st.title("📝 Profil Financier")

    age = st.number_input("Quel est votre âge ?", min_value=18, max_value=100, value=30, step=1)
    but = st.selectbox("Quel est votre objectif d'investissement ?", ["Retraite", "Achat immobilier", "Éducation", "Autre"])
    horizon_temps = st.selectbox("Quel est votre horizon d'investissement ?", ["Moins de 1 an", "1 à 5 ans", "5 ans et plus"])
    risque = st.selectbox("Quelle est votre tolérance au risque ?", ["Faible", "Modéré", "Élevé"])
    montant = st.number_input("Combien souhaitez-vous investir en $ ?", min_value=100, value=1000, step=100)

    # Calculer le profil en fonction des réponses
    if st.button("Obtenir des suggestions"):
        # Exemple de logique de suggestion
        suggestions = []
        if risque == "Faible":
            suggestions.append("ETF Obligations")
            if horizon_temps == "5 ans et plus":
                suggestions.append("ETF Actions de dividendes")
        elif risque == "Modéré":
            suggestions.append("ETF large marché")
            if horizon_temps == "5 ans et plus":
                suggestions.append("Actions de grandes entreprises")
        else:
            suggestions.append("Actions de croissance")
            if horizon_temps == "5 ans et plus":
                suggestions.append("Technologie")
        
        # Affichage des suggestions
        st.subheader("💡 Suggestions d'investissement basées sur votre profil :")
        for suggestion in suggestions:
            st.write(f"- {suggestion}")

# Section 1 : Calculateur d'Intérêts Composés
if page == "Calculateur d'Intérêts":
    st.title("💰 Calculateur de Placement et Intérêts Composés")

    col1, col2 = st.columns(2)
    with col1:
        montant_annuel = st.number_input("Montant investi par an ($)", min_value=0.0, value=1000.0, step=100.0)
        taux_interet = st.number_input("Taux d'intérêt annuel (%)", min_value=0.0, value=5.0, step=0.1)
    with col2:
        annees = st.number_input("Nombre d'années", min_value=1, value=10, step=1)
        type_invest = st.selectbox("Type d'investissement", ["Actions", "Obligations"])

    if st.button("Calculer"):
        df = calculer_capital(montant_annuel, taux_interet, annees, type_invest)

        st.subheader("📈 Évolution du capital")
        st.dataframe(df.style.format({"Capital accumulé": "${:,.2f}"}))

        st.line_chart(df.set_index("Année")["Capital accumulé"].rename(type_invest))

        total = df["Capital accumulé"].iloc[-1]
        st.success(f"Capital final après {annees} ans : ${total:,.2f}")

        csv = df.to_csv(index=False)
        st.download_button("Télécharger les données", csv, "evolution_capital.csv", "text/csv")

# Section 2 : Portefeuille
elif page == "Portefeuille":
    st.title("📊 Mon Portefeuille")

    if "portefeuille" not in st.session_state:
        st.session_state.portefeuille = pd.DataFrame(columns=["Actif", "Type", "Quantité", "Prix Achat", "Valeur Actuelle"])

    with st.form(key="ajout_actif"):
        recherche = st.text_input("Nom ou symbole du placement")
        quantite = st.number_input("Quantité", min_value=0.0, step=1.0)
        bouton_ajouter = st.form_submit_button("Ajouter")

        if bouton_ajouter and recherche:
            try:
                symbole_final = recherche.strip().upper()
                actif = yf.Ticker(symbole_final)
                info = actif.info
                hist = actif.history(period="1d")
                if hist.empty:
                    raise ValueError("Aucune donnée disponible")
                prix_actuel = hist["Close"].iloc[-1]
                prix_achat = prix_actuel
                secteur = info.get("sector", "")
                if "ETF" in info.get("quoteType", "").upper() or "ETF" in info.get("longName", "").upper():
                    type_actif = "FNB"
                elif secteur == "Financial Services" or "BOND" in info.get("longName", "").upper():
                    type_actif = "Obligations"
                else:
                    type_actif = "Actions"
                new_row = {"Actif": symbole_final, "Type": type_actif, "Quantité": quantite, "Prix Achat": prix_achat, "Valeur Actuelle": prix_actuel}
                st.session_state.portefeuille = pd.concat([st.session_state.portefeuille, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"{symbole_final} ajouté au portefeuille !")
            except Exception as e:
                st.error(f"Erreur : {str(e)}")

    if not st.session_state.portefeuille.empty:
        st.subheader("📈 Composition du portefeuille")

        if st.button("🔄 Mettre à jour les données"):
            for i, row in st.session_state.portefeuille.iterrows():
                try:
                    hist = yf.Ticker(row["Actif"]).history(period="1d")
                    if not hist.empty:
                        st.session_state.portefeuille.at[i, "Valeur Actuelle"] = hist["Close"].iloc[-1]
                except:
                    pass

        st.session_state.portefeuille["Valeur Totale"] = st.session_state.portefeuille["Quantité"] * st.session_state.portefeuille["Valeur Actuelle"]
        st.session_state.portefeuille["Profit/Perte"] = (st.session_state.portefeuille["Valeur Actuelle"] - st.session_state.portefeuille["Prix Achat"]) * st.session_state.portefeuille["Quantité"]

        st.dataframe(st.session_state.portefeuille.style.format({
            "Prix Achat": "${:.2f}", "Valeur Actuelle": "${:.2f}",
            "Valeur Totale": "${:,.2f}", "Profit/Perte": "${:,.2f}"
        }))

# Section 3 : Watchlist
elif page == "Watchlist":
    st.title("👀 Ma Watchlist")

    if "watchlist" not in st.session_state:
        st.session_state.watchlist = []

    symbole = st.text_input("Ajouter un symbole à la watchlist (ex: AAPL)")
    if st.button("Ajouter") and symbole:
        st.session_state.watchlist.append(symbole.upper())
        st.success(f"{symbole.upper()} ajouté à la watchlist !")

    if st.session_state.watchlist:
        st.subheader("Ma Watchlist")
        data = {}
        risques = []
        for sym in st.session_state.watchlist:
            try:
                actif = yf.Ticker(sym)
                info = actif.info
                hist = actif.history(period="1d")
                if not hist.empty:
                    data[sym] = hist["Close"].iloc[-1]
                    volatilite, var = calculer_risque(hist)
                    risques.append((sym, volatilite, var))
            except:
                pass
        st.write(data)
        if risques:
            st.write("Volatilité et VaR des actifs:")
            for risk in risques:
                st.write(f"{risk[0]} : Volatilité = {risk[1]}, VaR = {risk[2]}")

# Section 4 : Informations Financières
elif page == "Informations Financières":
    st.title("📚 Informations Financières")
    st.write("### Qu'est-ce qu'un ETF ?")
    st.write("""
        Un ETF (Exchange Traded Fund) est un fonds d'investissement coté en bourse qui suit un indice, une matière première, un secteur, ou un groupe d'actifs. 
        Il permet aux investisseurs d'obtenir une exposition diversifiée tout en ayant une liquidité élevée, étant donné qu'il peut être acheté et vendu comme une action.
    """)
    st.write("### Quelle est la différence entre une action et une obligation ?")
    st.write("""
        Une action représente une part de propriété dans une entreprise, tandis qu'une obligation est un instrument de dette où l'investisseur prête de l'argent à une entreprise ou un gouvernement en échange de paiements d'intérêts.
    """)

# Section 5 : Profil Financier
elif page == "Profil Financier":
    creer_profil()
