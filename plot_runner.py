import pandas as pd
import data_handler
import streamlit as st
import geopandas as gpd
import plotly.express as px
import numpy as np
import seaborn as sns


def plot_geomap(df, var, cat=False):

    info_ufs = gpd.read_file('outils/bcim_2016_21_11_2018.gpkg', layer='lim_unidade_federacao_a')
    info_ufs.rename({'sigla': 'SG_UF_ESC'}, axis=1, inplace=True)

    level_groups = {
    1: ['A', 'B', 'C','D','E','F'],
    2: ['G', 'H', 'I','J'],
    3: ['K', 'L', 'M','N'],
    4: ['O', 'P', 'Q']
    }   

    df['Q006'].replace(['A', 'B', 'C','D','E','F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P','Q'], [1,1,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4], inplace=True) 
    df['Q006'].convert_dtypes()

    df["MEDIA_NOTAS"] = df[["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]].mean(axis=1)

    # Agrupa os dados por estado e calcula a média das notas em cada prova
    if not cat:
        df_estado = df.groupby('SG_UF_ESC').mean().reset_index()
    else:
        df_estado = df.groupby('SG_UF_ESC').agg(pd.Series.mode)

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

def plot_violin(df, var):

    
    dados = df[["MEDIA_NOTAS", var]]

    fig = sns.violinplot(data=dados, x=var, y="MEDIA_NOTAS")
    return fig

def plot_dist(df, var):

    # Plotando um histograma da distribuição da média das notas
    fig = sns.histplot(data=df, x=var, kde=True)

    return fig

if __name__ == "__main__":
    st.write("""
             # Testando o plot
             """)
    
    df = data_handler.read_enem('enem_data/enem_2018.csv')
    st.plotly_chart(plot_geomap(df, 'NU_NOTA_CN'))

