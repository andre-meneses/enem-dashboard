import streamlit as st
import plot_runner as pr
import data_handler as dh

st.write("""
# Microdados ENEM 2016-2020

""")

# st.markdown("<h2 style='text-align: center; color: white;'>Map Plot</h2>", unsafe_allow_html=True)


col1, col2= st.columns(2)

variables = ['NU_NOTA_CN', 'NU_NOTA_MT', 'NU_NOTA_CH', 'NU_NOTA_LC','TP_FAIXA_ETARIA']
anos = ['2016', '2017','2018','2019','2020']

var = col1.selectbox('Selecione a variável', variables)
ano = col2.select_slider('Selecione o ano', anos)

df = dh.read_enem('dados/enem_' + ano + '.csv')
map_plot = pr.plot_geomap(df, var)

st.plotly_chart(map_plot)

