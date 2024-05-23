import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_group = pd.read_csv('../datasets/ad_seg_day.csv')
df = pd.read_csv('../datasets/dataset_tratado.csv')


st.title("Análise de anúncios de marketing digital")
st.subheader("principais KPIs da base de dados")


col1, col2, col3,col4 = st.columns(4)


unique_ads = df['ad_x'][df['ad_x'].isin(['ad1, ad2, ad3'])].nunique()
col1.metric(label='Total de anúncios únicos', value=unique_ads)

unique_seg = df['segment_x'].nunique()
col2.metric(label='Total de segmentos únicos', value=unique_seg)

total_impressions = df['impressions'].sum()
col3.metric(label='Total de impressões', value=f'{total_impressions:.0f}')

total_conversions = df['conversions'].sum()
col4.metric(label='Total de conversões', value=f'{total_conversions:.0f}')

select_segment = st.selectbox('Selecione um segmento', options=df['segment_x'][df['segment_x'].isin(['seg1','seg2','seg3'])].unique())

select_ad = st.selectbox('Selecione um anuncio', options=df['ad_x'][df['segment_x'].isin(['seg1','seg2','seg3'])].unique())
filtered_segment = df[(df['segment_x'] == select_segment) & (df['ad_x'] == select_ad)]
grouped_segment = filtered_segment.groupby('weekday')['conversions'].sum()
grouped_segment = grouped_segment.sort_values(ascending=False)
#st.bar_chart(grouped_segment)


fig, ax = plt.subplots()
width = 0.35
ind = np.arange(len(grouped_segment))
bars = ax.bar(ind, grouped_segment.values,width)

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom')
    
ax.set_xticks(ind)
ax.set_xticklabels(grouped_segment.index)
st.pyplot(fig)



st.subheader('📈 Premissas estatísticas:')
st.write('Tanto para a tabela de impressões quanto para a de conversões, houveram outliers, que foram removidos para balancear as médias e análises')
st.write('Ao juntar as duas tabelas, não foi encontrada nenhuma correlação positiva entre impressões e conversões. Portanto, impressões não é a melhor métrica para se analisar. É necessário extrair outra métrica que explique melhor as convesões para avançar com modelos de regressão e recomendação mais precisos.')
st.write('Não foram encontradas datas em comum entre as duas tabelas. Portanto, segundo as bases de dados, nos dias que há impressões, não há conversões')

st.subheader('💡 Análises e insights')
st.write('Segundo os dados apresentados,  por mais que o seg2 seja maior em impressões totais, proporcionalmente pelo número de vezes em que se repete, os que possuem mais impressões são seg1 e seg3.')
st.write('Todos os dias possuem uma média equilibrada de registros para impressões, porém o que mais possui relevância em proporção de impressões é Quarta-feira (Wednesday), seguindo de domingo(Sunday). Já em conversões, proporcioalmente também, os melhores dias são Terça-feira (Tuesday) e Quinta-feira (Thursday)')
st.write('O melhor anúncio para impressões é o ad2, mas que entrega melhores conversões é o ad3.')
st.write('De modo geral, os melhores anúncios são ad1 e ad3.')
st.write('Para o seg1, o melhor anúncio em taxa de conversão é o ad3, com 41%.')
st.write('No seg2, o melhor anúncio em taxa de conversão é o ad1, com 54%.')
st.write('Para o seg3, o melhor anúncio em taxa de conversão é o ad3, com 35%.')
st.write('E para o seg4 o melhor anúncio em taxa de conversão é o ad1, com 40%.')
