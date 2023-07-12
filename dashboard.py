import streamlit as st
import requests
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go

st.title("Bienvenue sur l'application de Sié Charles SOU !")
st.write("Je vous souhaite bon visionnage!")

data = None
url_api = "http://localhost:8000/charlesapi/data"

# Fonction pour appeler l'API et obtenir les données
def get_data_from_api():
    response = requests.get(url_api)
    return pd.DataFrame(response.json())

# Afficher le bouton dans le dashboard
if st.button('Obtenir les données'):
    # Appeler la fonction pour obtenir les données de l'API
    data = get_data_from_api()

# Afficher les données dans le dashboard
if data is not None:
    st.dataframe(data)

if data is not None:
        df = pd.DataFrame(data)  # Utilisation de data pour créer un DataFrame df

    # Calcul du chiffre d'affaires
        chiffre_affaires = df['price'].sum()
        st.write(f"<span style='color:red; font-size:40px;'>Chiffre d'affaires : {chiffre_affaires} € </span>", unsafe_allow_html=True)

    ## Box plot
        fig = px.box(df, x='product_id', y='age')
        fig.update_layout(
            xaxis_title='Produits',
            yaxis_title="Âge",
            title="Relation entre l'âge et les produits")
        st.plotly_chart(fig)

        # Les ventes en fonctions des campagnes
        # Grouper les données par campagne et calculer les ventes
        sales_data = df.groupby('campaign_id')['price'].sum().reset_index()

        # Création du diagramme des ventes en fonction des campagnes
        fig = px.bar(sales_data, x='campaign_id', y='price', title='Diagramme des ventes en fonction des campagnes')

        # Affichage du diagramme dans Streamlit
        st.plotly_chart(fig)

    # Entonnoir
        # Conversion des variables en date
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df['timestamp_x'] = pd.to_datetime(df['timestamp_x'], unit='s')
        df['timestamp_y'] = pd.to_datetime(df['timestamp_y'], unit='s')

        # Calcul des statistiques
        nb_impressions = df['timestamp'].count()
        nb_clics = df['timestamp_x'].count()
        nb_achats = df['timestamp_y'].count()

        # Création du diagramme en entonnoir
        fig2 = go.Figure(
            go.Funnel(
                y=['Impressions', 'Clics', 'Achats'],
                x=[nb_impressions, nb_clics, nb_achats]
            )
        )

        # Affichage du diagramme dans Streamlit
        fig2.update_layout(title="Diagramme en entonnoir")
        st.plotly_chart(fig2)

        # Filtrage des données en fonction de la campaign_id sélectionnée
        campaign_ids = df['campaign_id'].unique()
        selected_campaign_id = st.selectbox('Sélectionnez une campaign_id', campaign_ids)
        filtered_df = df[df['campaign_id'] == selected_campaign_id]

        # Calcul des statistiques sur les données filtrées
        nb_impressions = filtered_df['timestamp'].count()
        nb_clics = filtered_df['timestamp_x'].count()
        nb_achats = filtered_df['timestamp_y'].count()

        # Création du diagramme en entonnoir avec les données filtrées
        fig2 = go.Figure(
            go.Funnel(
                y=['Impressions', 'Clics', 'Achats'],
                x=[nb_impressions, nb_clics, nb_achats]
            )
        )

        # Affichage du diagramme dans Streamlit
        fig2.update_layout(title="Diagramme en entonnoir - Filtrage des données en fonction de la campaign_id sélectionnée")
        st.plotly_chart(fig2)



