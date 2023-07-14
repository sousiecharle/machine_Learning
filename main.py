import streamlit as st
import pandas as pd
from flask import Flask, jsonify
import requests
import plotly.express as px
import plotly.graph_objects as go

st.title("Bienvenue sur l'application SIE CHARLES SOU")

impressions_df = pd.read_csv('impressions.csv')
clics_df = pd.read_csv('clics.csv')
achats_df = pd.read_csv('achats.csv')

### Fusion des données

donnees_fusionnees = pd.merge(impressions_df, clics_df, on='cookie_id')
donnees = pd.merge(donnees_fusionnees, achats_df, on='cookie_id')



#Route API pour avoir les données
app = Flask(__name__)
@app.route('/api/donnees', methods=['GET'])
def get_donnees():
    return jsonify(donnees)

### Tableau pour le Dashboard
st.title('Bienvenue')
st.subheader('Tableau')
st.dataframe(donnees)

df = pd.DataFrame(donnees)
### Chiffre d'affaire
chiffre_affaires = df['price'].sum()
st.write(f"<span style='color:red; font-size:40px;'>Chiffre d'affaires : {chiffre_affaires} € </span>", unsafe_allow_html=True)

## Box plot
fig = px.box(df, x='product_id', y='age')
fig.update_layout(
    xaxis_title='Produits',
    yaxis_title="Âge",
    title="Relation entre l'âge et les produits")
st.plotly_chart(fig)

fig1 = px.histogram(df, x='campaign_id' , y='price')
fig1.update_layout(
    xaxis_title='campaigne',
    yaxis_title="price",
    title="Les ventes en fonctions des campagnes")
st.plotly_chart(fig1)

# Entonnoir
nb_impressions = df['timestamp'].sum()
nb_clics = df['timestamp_x'].sum()
nb_achats = df['timestamp_y'].sum()

fig2 = go.Figure(
    go.Funnel(
        y=['Impressions', 'Clics', 'Achats'],
        x=[nb_impressions, nb_clics, nb_achats]
    )
)

st.plotly_chart(fig2)
if __name__ == '__dashboard_tuto__':
    app.run(debug=True)

