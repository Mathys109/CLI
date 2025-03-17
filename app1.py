import streamlit as st

# Titre de l'application
st.title("Bienvenue dans mon application Streamlit")

# Affichage d'un texte
st.write("Ceci nnnnnnest une page fonctionnelle de Streamlit")

# Demande d'entrée à l'utilisateur
nom = st.text_input("Quel est votre nom ?")

# Affichage du résultat
if nom:
    st.write(f"Bonjour, {nom} !")
