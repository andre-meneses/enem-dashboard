import pandas as pd
import data_handler
import streamlit as st
import geopandas as gpd
import plotly.express as px
import numpy as np


def plot_geomap(df, var):

    info_ufs = gpd.read_file('outils/bcim_2016_21_11_2018.gpkg', layer='lim_unidade_federacao_a')
    info_ufs.rename({'sigla': 'SG_UF_ESC'}, axis=1, inplace=True)

    # Agrupa os dados por estado e calcula a média das notas em cada prova
    df_estado = df.groupby('SG_UF_ESC').mean().reset_index()
    df_estado = info_ufs.merge(df_estado, on ='SG_UF_ESC', how='left')

    # plot_estado = df_estado.plot(column='NU_NOTA_MT', cmap='viridis', legend=True, edgecolor='black')

    fig = px.choropleth_mapbox(df_estado,
                               geojson=df_estado.geometry,
                               locations=df_estado.index,
                               color_continuous_scale='deep', 
                               color=var,
                               mapbox_style='carto-positron',
                               center={"lat": -14.235, "lon": -51.9253},
                               zoom=3,
                               opacity=0.5)
    fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})

    return fig

if __name__ == "__main__":
    st.write("""
             # Testando o plot
             """)
    
    df = data_handler.read_enem('enem_data/enem_2018.csv')
    st.plotly_chart(plot_geomap(df, 'NU_NOTA_CN'))

