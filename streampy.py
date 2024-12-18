import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import urllib.parse
import random
import time

# Titre de l'application
st.title("✨ Projet IRIS avec Streamlit 🚀")

# Chargement des données avec barre de progression
st.header("Chargement des données...")
progress_bar = st.progress(0)
for i in range(100):
    time.sleep(0.02)
    progress_bar.progress(i + 1)

try:
    # Charger le fichier IRIS.csv
    data = pd.read_csv("IRIS.csv")
    st.success("Base de données chargée avec succès 🎉")
    
    # Affichage de l'aperçu des données
    st.write("Aperçu des données :")
    st.dataframe(data.head())
    
    # Section 1 : Statistiques descriptives
    st.header("📊 Statistiques Descriptives")
    if st.button("Afficher les statistiques descriptives"):
        st.write(data.describe())
    
    # Section 2 : Visualisations interactives
    st.header("📈 Visualisation des Données")
    
    # Histogramme interactif
    numeric_column = st.selectbox(
        "Sélectionnez une colonne numérique pour un histogramme",
        data.select_dtypes(include=['number']).columns
    )
    if numeric_column:
        st.write(f"Histogramme pour **{numeric_column}**")
        fig, ax = plt.subplots()
        ax.hist(data[numeric_column], bins=15, color='skyblue', edgecolor='black')
        ax.set_title(f"Histogramme de {numeric_column}")
        st.pyplot(fig)
    
    # Scatter plot interactif avec Plotly
    st.subheader("📊 Corrélation : Graphique interactif")
    x_col = st.selectbox("Axe X", data.select_dtypes(include=['number']).columns, key="scatter_x")
    y_col = st.selectbox("Axe Y", data.select_dtypes(include=['number']).columns, key="scatter_y")
    if x_col and y_col:
        scatter_fig = px.scatter(data, x=x_col, y=y_col, color=data.columns[-1], title="Corrélation entre deux colonnes")
        st.plotly_chart(scatter_fig)
    
    # Boxplot interactif
    st.subheader("📦 Box Plot : Distribution par catégorie")
    categorical_col = st.selectbox("Sélectionnez une colonne catégorique", data.select_dtypes(include=['object']).columns)
    if categorical_col and numeric_column:
        fig, ax = plt.subplots()
        sns.boxplot(x=categorical_col, y=numeric_column, data=data, ax=ax, palette="coolwarm")
        ax.set_title(f"Distribution de {numeric_column} par {categorical_col}")
        st.pyplot(fig)

    # Section 3 : Challenge SQL Injection
    st.header("🎯 Mini CTF : Challenge SQL Injection 💻")
    st.write(
        "Votre mission : trouvez un moyen de contourner notre filtre pour obtenir le **flag**.\n"
        "⚠️ Attention, si votre payload est détecté comme une attaque, vous serez bloqué ! 😈"
    )

    # Input utilisateur pour tester le payload SQLi
    payload = st.text_input("Loggez-vous !")

    # Liste des mots-clés SQLi classiques
    sqli_keywords = [
        "select", "insert", "update", "delete", "union",
        "--", "#", "/*", "*/", "'", '"', "or 1=1", "or 'a'='a'",
        "sleep", "benchmark", "ascii", "char", "unhex", "select+from", "union+select", "group+by"
    ]

    # Fonction pour vérifier les caractères SQLi
    def contains_sqli_characters(payload):
        sqli_chars = ["'", '"', "--", "#", "/*", "*/", "or 1=1", "or 'a'='a'"]
        return any(char in payload for char in sqli_chars)

    # Fonction pour valider un payload SQLi
    def validate_payload(payload):
        decoded_payload = urllib.parse.unquote(payload.lower())
        if any(keyword in decoded_payload for keyword in sqli_keywords):
            return decoded_payload
        return None

    # Payloads SQLi valides pour le flag
    valid_sqli_payloads = [
        "admin'--",
        "admin' #",
        "' OR 1=1 --",
        "' OR 'a'='a' --"
    ]

    if payload:
        if contains_sqli_characters(payload):
            st.error("❌ Bad Hacker ! Filters catch you. Retry.")
        else:
            decoded_payload = validate_payload(payload)
            if decoded_payload:
                if decoded_payload in valid_sqli_payloads:
                    flag = "FLAG{SQL1_Inj3c7ion_5ucc3ss}"
                    st.success(f"🎉 Félicitations, vous avez réussi ! Voici votre flag : {flag}")
                else:
                    st.write("Pas encore le bon payload ! Essayez encore.")
            else:
                st.write("Payload non valide. Réessayez.")

except FileNotFoundError:
    st.error("Erreur : Le fichier 'IRIS.csv' est introuvable dans le dossier. Assurez-vous qu'il est bien au bon endroit.")
