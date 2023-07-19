import pandas as pd
import networkx as nx
import data_handler
import streamlit as st
import geopandas as gpd
import plotly.express as px
import numpy as np
import seaborn as sns
from graph_tool.all import *
import matplotlib.pyplot as plt

def plot_geomap(df, var, cat=False):

    """
    Plot a choropleth map showing the geographical distribution of a given variable in the DataFrame.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data to plot.
        var (str): The column name in 'df' representing the variable to be plotted.
        cat (bool, optional): If True, the variable is treated as categorical. Default is False.

    Returns:
        plotly.graph_objs._figure.Figure: The choropleth map figure.
    """

    df["Q006"].replace(['A', 'B', 'C','D','E','F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P','Q'], [1,1,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4], inplace=True)

    df["Q006"] = df['Q006'].convert_dtypes()

    df["MEDIA_NOTAS"] = df[["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]].mean(axis=1)


    info_ufs = gpd.read_file('outils/bcim_2016_21_11_2018.gpkg', layer='lim_unidade_federacao_a')
    info_ufs.rename({'sigla': 'SG_UF_ESC'}, axis=1, inplace=True)

        # Agrupa os dados por estado e calcula a média das notas em cada prova
    if not cat:
        df_estado = df.groupby('SG_UF_ESC').mean(numeric_only=True).reset_index()
    else:
        df_estado = df.groupby('SG_UF_ESC').agg(pd.Series.mode)

    df_estado = info_ufs.merge(df_estado, on ='SG_UF_ESC', how='left')

    # plot_estado = df_estado.plot(column='NU_NOTA_MT', cmap='viridis', legend=True, edgecolor='black')

    if not cat:
        color_values = df_estado[var].tolist()
    else:
        color_values = df_estado[var].apply(lambda x: str(x)).tolist()


    fig = px.choropleth_mapbox(df_estado,
                               geojson=df_estado.geometry,
                               locations=df_estado.index,
                               color_continuous_scale='deep', 
                               color=color_values,
                               mapbox_style='carto-positron',
                               center={"lat": -14.235, "lon": -51.9253},
                               zoom=3,
                               opacity=0.5)
    fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})

    return fig

def plot_violin(df, var):
    """
    Plot a violin plot to visualize the distribution of a numeric variable in relation to 'MEDIA_NOTAS'.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data to plot.
        var (str): The column name in 'df' representing the variable to be plotted.

    Returns:
        matplotlib.axes._subplots.AxesSubplot: The violin plot.
    """
    
    dados = df[["MEDIA_NOTAS", var]]

    fig = sns.violinplot(data=dados, x=var, y="MEDIA_NOTAS")
    return fig

def plot_dist(df, var):
    """
    Plot a histogram to visualize the distribution of a numeric variable.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data to plot.
        var (str): The column name in 'df' representing the variable to be plotted.

    Returns:
        matplotlib.axes._subplots.AxesSubplot: The histogram plot.
    """

    # Plotando um histograma da distribuição da média das notas
    fig = sns.histplot(data=df, x=var, kde=True)

    return fig

def plot_itens(df, target_sg_area=None):

    df = df.drop_duplicates(subset=['CO_ITEM'])

    df = df.dropna(subset=['SG_AREA', 'NU_PARAM_B'])

    # Step 2: Create a NetworkX graph
    G = nx.Graph()

    # Step 3: Add nodes with unique identifiers (SG_AREA + NU_PARAM_B) as node labels
    for _, row in df.iterrows():
        node_id = f"{row['SG_AREA']}_{row['NU_PARAM_B']}"
        G.add_node(node_id, SG_AREA=row['SG_AREA'], NU_PARAM_B=row['NU_PARAM_B'])

    # Step 4: Connect nodes with the same 'SG_AREA' value
    for area in df['SG_AREA'].unique():
        nodes_with_area = df[df['SG_AREA'] == area]
        node_ids = [f"{row['SG_AREA']}_{row['NU_PARAM_B']}" for _, row in nodes_with_area.iterrows()]
        G.add_edges_from((a, b) for a in node_ids for b in node_ids if a != b)

    # Filter the graph to display only the specified 'SG_AREA'
    if target_sg_area is not None:
        nodes_to_remove = [node for node in G.nodes if not node.startswith(target_sg_area)]
        G.remove_nodes_from(nodes_to_remove)

    # Draw the graph with nodes colored according to 'NU_PARAM_B'

    fig, ax = plt.subplots(1, 1, figsize=(10, 8))

    pos = nx.spring_layout(G)  # Position nodes using the spring layout algorithm
    color = [G.nodes[node]['NU_PARAM_B'] for node in G.nodes]

    # nx.draw_networkx_edges(G, pos=pos, alpha=0.4, ax=ax)

    # Draw nodes
    nodes = nx.draw_networkx_nodes(G, pos=pos, node_color=color, cmap=plt.cm.jet, ax=ax)

    # Draw labels
    nx.draw_networkx_labels(G, pos=pos, font_color='black', font_size=8, ax=ax)

    plt.axis("off")
    plt.colorbar(nodes)


    return fig 

if __name__ == "__main__":
    # st.write("""
             # Testando o plot
             # """)

    df = data_handler.read_enem('enem_data/itens/itens_prova_2016.csv', itens=True)
    plot_clustering(df,'MT')

    
    # df = data_handler.read_enem('enem_data/enem_2018.csv')
    # st.plotly_chart(plot_geomap(df, 'NU_NOTA_CN'))

