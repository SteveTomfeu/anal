import streamlit as st
import pandas as pd
from pathlib import Path
import os

st.set_page_config(
    layout="wide",
    page_title="Analyse Données Marchandises",
    page_icon="📊"
)

#1. chargement des données
@st.cache_data
def load_data():
    #données sur l'acompte.
    df_acompte = pd.read_excel("acomptes_ms.xlsx")
    df_facture = pd.read_excel("final_ms.xlsx")
    df_fusion = pd.read_excel("Marchandises_enrichi.xlsx")
    return df_acompte, df_facture, df_fusion

df1, df2, df3 = load_data()

#1 ---Barre latérales (Filtres Globaux)---
st.sidebar.title("📌 Filtres")
#sap = st.sidebar.multiselect("SAP", options=df3['Secteur facturation '].unique(), default=df3['Secteur facturation '].unique())

df3["Délai acompte"] = (
    df3["Délai acompte"]
    .astype(str)
    .str.replace(",", ".")
    .str.strip()
)

df3["Délai final"] = (
    df3["Délai final"]
    .astype(str)
    .str.replace(",", ".")
    .str.strip()
)

df3["Délai acompte"] = pd.to_numeric(df3["Délai acompte"], errors="coerce")
df3["Délai final"] = pd.to_numeric(df3["Délai final"], errors="coerce")

# Calcul le délai moyen acompte par secteur de facturation
delai_par_secteur = (
    df3.dropna(subset=["Délai acompte", "Secteur facturation "])
    .groupby("Secteur facturation ")["Délai acompte"]
    .mean()
    .round(2)
)

# Calcul le délai moyen facture définitive par secteur de facturation
definal_par_secteur = (
    df3.dropna(subset=["Délai final", "Secteur facturation "])
    .groupby("Secteur facturation ")["Délai final"]
    .mean()
    .round(2)
)

st.subheader("⏱️ Délai moyen facturation acompte par secteur d'activités portuaires.")
#Création dynamique des colonnes selon le nombre de secteurs trouvés
cols = st.columns(len(delai_par_secteur))

for col, (secteur, delai) in zip(cols, delai_par_secteur.items()):
    with col:
        st.metric(
            label = f"Secteur {secteur}",
            value=f"{delai} jours",
            help=f"Délai moyen acompte pour le {secteur}"
        )

st.subheader("⏱️ Délai moyen facturation définitive par secteur d'activités portuaires.")
#Création dynamique des colonnes selon le nombre de secteurs trouvés
cols = st.columns(len(definal_par_secteur))

for col, (secteur, delai) in zip(cols, definal_par_secteur.items()):
    with col:
        st.metric(
            label = f"Secteur {secteur}",
            value=f"{delai} jours",
            help=f"Délai moyen facturation définitive pour le {secteur}"
        )

#Affichage des données détaillées
st.subheader("📋 Datasets")
st.dataframe(
    df3,
    use_container_width=True,
    hide_index=True
             )