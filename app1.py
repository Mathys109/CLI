# app.py
import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="Gestion Financière", layout="wide")

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
        volatilite = rendements.std() * np.sqrt(252)
        var = np.percentile(rendements, 5)
        return volatilite, var
    except:
        return "N/A", "N/A"

# Suggestions d'actifs populaires
suggestions = ["AAPL", "MSFT", "TSLA", "GOOGL", "AMZN", "VTI", "SPY", "XIC.TO", "QQQ"]

# Onglets principaux
onglets = st.tabs(["👤 Profil Financier", "💰 Intérêts Composés", "📊 Portefeuille", "👀 Watchlist", "ℹ️ Infos Financières"])

# Onglet 1 : Profil Financier
with onglets[0]:
    st.header("👤 Créez votre Profil Financier")
    with st.form("profil_form"):
        nom = st.text_input("Votre nom")
        age = st.number_input("Âge", min_value=18, value=30)
        revenu = st.number_input("Revenu annuel ($)", min_value=0.0, step=1000.0)
        objectif = st.selectbox("Objectif d'investissement", ["Retraite", "Croissance du capital", "Revenu stable", "Projet à court terme"])
        horizon = st.slider("Horizon de placement (années)", 1, 50, 10)
        risque = st.radio("Tolérance au risque", ["Faible", "Moyenne", "Élevée"])
        soumettre = st.form_submit_button("Analyser mon profil")

    if soumettre:
        st.success(f"Merci {nom}, voici quelques recommandations :")
        if risque == "Faible":
            st.write("\n🔹 Portefeuille défensif suggéré : FNB obligataires (ZAG), actions stables (BCE, ENB), FNB de dividendes (VDY)")
        elif risque == "Moyenne":
            st.write("\n🔹 Portefeuille équilibré suggéré : FNB diversifiés (VGRO), actions solides (AAPL, MSFT), obligations")
        else:
            st.write("\n🔹 Portefeuille dynamique suggéré : Tech (TSLA, NVDA), croissance (ARKK), crypto ou émergents")

        st.info("Ces suggestions sont basées sur votre horizon et tolérance au risque. Consultez un conseiller pour des conseils personnalisés.")

# Onglet 2 : Calculateur d'intérêts composés
with onglets[1]:
    st.header("💰 Calculateur d'Intérêts Composés")
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
        st.line_chart(df.set_index("Année")[["Capital accumulé"]])
        total = df["Capital accumulé"].iloc[-1]
        st.success(f"Capital final après {annees} ans : ${total:,.2f}")
        csv = df.to_csv(index=False)
        st.download_button("Télécharger les données", csv, "evolution_capital.csv", "text/csv")

# Onglet 3 : Portefeuille
with onglets[2]:
    st.header("📊 Mon Portefeuille")
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

        df = st.session_state.portefeuille
        df["Valeur Totale"] = df["Quantité"] * df["Valeur Actuelle"]
        df["Profit/Perte"] = (df["Valeur Actuelle"] - df["Prix Achat"]) * df["Quantité"]
        st.dataframe(df.style.format({"Prix Achat": "${:.2f}", "Valeur Actuelle": "${:.2f}", "Valeur Totale": "${:,.2f}", "Profit/Perte": "${:,.2f}"}))

# Onglet 4 : Watchlist
with onglets[3]:
    st.header("👀 Ma Watchlist")
    if "watchlist" not in st.session_state:
        st.session_state.watchlist = []

    symbole = st.text_input("Ajouter un symbole à la watchlist")
    if st.button("Ajouter") and symbole:
        st.session_state.watchlist.append(symbole.upper())
        st.success(f"{symbole.upper()} ajouté à la watchlist !")

    if st.session_state.watchlist:
        st.subheader("Liste de surveillance")
        data = {}
        risques = []
        for symbole in st.session_state.watchlist:
            try:
                actif = yf.Ticker(symbole)
                hist = actif.history(period="1y")
                if hist.empty:
                    raise ValueError("Aucune donnée disponible")
                data[symbole] = hist["Close"].iloc[-1]
                volatilite, var = calculer_risque(hist["Close"])
                risques.append({"Volatilité (annuelle)": volatilite, "VaR (95%)": var})
            except:
                data[symbole] = "N/A"
                risques.append({"Volatilité (annuelle)": "N/A", "VaR (95%)": "N/A"})

        watch_df = pd.DataFrame(list(data.items()), columns=["Symbole", "Prix Actuel"])
        risque_df = pd.DataFrame(risques)
        st.dataframe(pd.concat([watch_df, risque_df], axis=1))

# Onglet 5 : Infos Financières
with onglets[4]:
    st.header("ℹ️ Informations Financières")
    symbole = st.text_input("Entrez un symbole pour voir les infos")
    if symbole:
        try:
            actif = yf.Ticker(symbole.upper())
            info = actif.info
            st.subheader(f"{info.get('longName', symbole.upper())} ({symbole.upper()})")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Secteur** : {info.get('sector', 'N/A')}")
                st.write(f"**Prix actuel** : ${info.get('currentPrice', 0):.2f}")
                st.write(f"**Capitalisation** : ${info.get('marketCap', 0):,.0f}")
            with col2:
                st.write(f"**PER** : {info.get('trailingPE', 'N/A')}")
                st.write(f"**Dividende** : {info.get('dividendYield', 0) * 100:.2f}%")
                st.write(f"**52 semaines** : ${info.get('fiftyTwoWeekLow', 0):.2f} - ${info.get('fiftyTwoWeekHigh', 0):.2f}")

            hist = actif.history(period="1y")
            if not hist.empty:
                volatilite, var = calculer_risque(hist["Close"])
                st.write(f"**Volatilité (annuelle)** : {'N/A' if volatilite == 'N/A' else f'{volatilite:.2%}'}")
                st.write(f"**VaR (95%)** : {'N/A' if var == 'N/A' else f'{var:.2%}'}")

                periode = st.selectbox("Période du graphique", ["1mo", "6mo", "1y", "5y"])
                hist = actif.history(period=periode)
                st.line_chart(hist["Close"].rename(f"Historique {symbole.upper()} ({periode})"))
        except Exception as e:
            st.error(f"Erreur : {str(e)}")

# Footer
date_str = datetime.now().strftime('%Y-%m-%d')
st.markdown(f"---\n<sub>Dernière mise à jour : {date_str}</sub>", unsafe_allow_html=True)
