import pandas as pd
import streamlit as st
import geopandas as gpd
import plotly.express as px
import numpy as np

sampled_chunks = []
chunk_size = 10000

INFO_UFS = gpd.read_file('bcim_2016_21_11_2018.gpkg', layer='lim_unidade_federacao_a')
INFO_UFS.rename({'sigla': 'SG_UF_ESC'}, axis=1, inplace=True)

# Read the CSV file in chunks and sample from each chunk
for chunk in pd.read_csv('DADOS/microdados_enem_2016.csv', chunksize = chunk_size, encoding='ISO-8859-1', on_bad_lines='skip', sep=';'):

    sampled_chunk = chunk.sample(frac=0.01)
    sampled_chunks.append(sampled_chunk)

# Concatenate the sampled chunks into a single DataFrame
df = pd.concat(sampled_chunks)

# Agrupa os dados por estado e calcula a média das notas em cada prova
df_estado = df.groupby('SG_UF_ESC').mean().reset_index()
df_estado = INFO_UFS.merge(df_estado, on ='SG_UF_ESC', how='left')

# plot_estado = df_estado.plot(column='NU_NOTA_MT', cmap='viridis', legend=True, edgecolor='black')

fig = px.choropleth_mapbox(df_estado,
                           geojson=df_estado.geometry,
                           locations=df_estado.index,
                            color_continuous_scale='viridis', range_color=(0, 600),
                           color='NU_NOTA_MT',
                           mapbox_style='carto-positron',
                           zoom=10,
                           opacity=0.5)
fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})

st.plotly_chart(fig)

