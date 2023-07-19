import streamlit as st
import plot_runner as pr
import data_handler as dh
from mlp import load_model
from sklearn.neural_network import MLPRegressor
import numpy as np

def streamlit_grade_plot():
    """
    Displays a streamlit plot for grade distribution based on selected variables.
    """
    var_dict = {
        'Matemática': 'NU_NOTA_MT',
        'Ciências das Natureza': 'NU_NOTA_CN',
        'Ciências Humanas': 'NU_NOTA_CH',
        'Linguagens': 'NU_NOTA_LC',
        'Redação': 'NU_NOTA_REDACAO'
    }

    col1, col2 = st.columns(2)

    variables = list(var_dict.keys())
    anos = ['2016', '2017', '2018', '2019', '2020']

    var = col1.selectbox('Selecione a prova', variables)
    var = var_dict[var]

    ano = col2.select_slider('Selecione o ano', anos)

    df = dh.read_enem(f'dados/enem_{ano}.csv')

    map_plot = pr.plot_geomap(df, var)
    dist_plot = pr.plot_dist(df, var)

    st.plotly_chart(map_plot)
    st.write("""### Distribuição das notas""")
    st.pyplot(dist_plot.figure)


def streamlit_categorical_plot():
    """
    Displays a streamlit plot for categorical variables.
    """
    tp_cor_raca_dict = {
        '0': 'Não declarado',
        '1': 'Branca',
        '2': 'Preta',
        '3': 'Parda',
        '4': 'Amarela',
        '5': 'Indígena',
        '6': 'Não dispõe da informação'
    }

    tp_faixa_etaria_dict = {
        '1': 'Menor de 17 anos',
        '2': '17 anos',
        '3': '18 anos',
        '4': '19 anos',
        '5': '20 anos',
        '6': '21 anos',
        '7': '22 anos',
        '8': '23 anos',
        '9': '24 anos',
        '10': '25 anos',
        '11': 'Entre 26 e 30 anos',
        '12': 'Entre 31 e 35 anos',
        '13': 'Entre 36 e 40 anos',
        '14': 'Entre 41 e 45 anos',
        '15': 'Entre 46 e 50 anos',
        '16': 'Entre 51 e 55 anos',
        '17': 'Entre 56 e 60 anos',
        '18': 'Entre 61 e 65 anos',
        '19': 'Entre 66 e 70 anos',
        '20': 'Maior de 70 anos'
    }

    var_dict = {'Faixa Etária': 'TP_FAIXA_ETARIA', 'Cor': 'TP_COR_RACA'}
    dicts = {'TP_FAIXA_ETARIA': tp_faixa_etaria_dict, 'TP_COR_RACA': tp_cor_raca_dict}

    col1, col2 = st.columns(2)

    variables = list(var_dict.keys())
    anos = ['2016', '2017', '2018', '2019', '2020']

    var = col1.selectbox('Selecione a variável', variables)
    var = var_dict[var]

    ano = col2.select_slider('Selecione o ano', anos)

    df = dh.read_enem(f'dados/enem_{ano}.csv')

    map_plot = pr.plot_geomap(df, var, cat=True)
    dist_plot = pr.plot_dist(df, var)

    st.plotly_chart(map_plot)
    st.write("""#### Legenda""")
    for key, item in dicts[var].items():
        st.write("- ", key, " : ", item)


def streamlit_income_plot():
    """
    Displays a streamlit plot for income distribution.
    """
    var_dict = {'Renda': 'Q006'}

    col1, col2 = st.columns(2)

    variables = list(var_dict.keys())
    anos = ['2016', '2017', '2018', '2019', '2020']

    var = col1.selectbox('Selecione a variável', variables)
    var = var_dict[var]

    ano = col2.select_slider('Selecione o ano', anos, key='aaa')

    df = dh.read_enem(f'dados/enem_{ano}.csv')

    map_plot = pr.plot_geomap(df, var)
    renda_plot = pr.plot_violin(df, 'Q006')

    st.plotly_chart(map_plot)
    st.write("""### Violin Plot""")
    st.pyplot(renda_plot.figure)

def streamlit_itens_plot():
    """
    Displays a streamlit plot for question itens.
    """

    col1, col2 = st.columns(2)

    variables = ['CN', 'CH', 'MT', 'LC']
    anos = ['2016', '2017', '2018', '2019', '2020']

    var = col1.selectbox('Selecione a variável', variables)

    ano = col2.select_slider('Selecione o ano', anos, key='bbb')

    df = dh.read_enem(f'itens_prova_{ano}.csv', itens=True)

    plot = pr.plot_itens(df, var)

    st.pyplot(plot)

def main():

    st.write("""# Microdados ENEM 2016-2020""")

    plot = st.sidebar.selectbox('Visualização:', ['Notas', 'Participantes', 'Dados socioeconômicos', 'Questões'])

    st.sidebar.write("Previsão Nota ")

    col1, col2 = st.sidebar.columns(2)

    acertos_cn = col1.number_input("Acertos CN:", value=25)
    acertos_ch = col2.number_input("Acertos CH:", value=25)
    acertos_mt = col1.number_input("Acertos MT:", value=25)
    acertos_lc = col2.number_input("Acertos LC:", value=25)

    model_cn = load_model('models/trained_model_CN.joblib')
    model_ch = load_model('models/trained_model_CH.joblib')
    model_mt = load_model('models/trained_model_MT.joblib')
    model_lc = load_model('models/trained_model_LC.joblib')

    nota_cn = model_cn.predict(np.array(acertos_cn).reshape(1,-1))
    nota_ch = model_ch.predict(np.array(acertos_ch).reshape(1,-1))
    nota_mt = model_mt.predict(np.array(acertos_mt).reshape(1,-1))
    nota_lc = model_lc.predict(np.array(acertos_lc).reshape(1,-1))

    cn = col1.empty()
    cn.write(f"Nota CN: {nota_cn}")
    ch = col2.empty()
    ch.write(f"Nota CH: {nota_ch}")
    mt = col1.empty()
    mt.write(f"Nota MT: {nota_mt}")
    lc = col2.empty()
    lc.write(f"Nota LC: {nota_lc}")

    if plot == 'Notas':
        streamlit_grade_plot()
    if plot == 'Participantes':
        streamlit_categorical_plot()
    if plot == 'Dados socioeconômicos':
        streamlit_income_plot()
    if plot == 'Questões':
        streamlit_itens_plot()

if __name__ == '__main__':
    main()

