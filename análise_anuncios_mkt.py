

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

impressions = pd.read_csv('./datasets/impressions.csv')
conversions = pd.read_csv('./datasets/conversions.csv')

"""## IMPRESSIONS"""

#criando campo de data a partir do timestamp
impressions['ts'] = pd.to_datetime(impressions['ts'])
impressions['date'] = impressions['ts'].dt.date

#criando campo de dia da semana
impressions['date'] = pd.to_datetime(impressions['date'])
impressions['day_of_week'] = impressions['date'].dt.day_name()

#nao precisamos mais da coluna timestamp
impressions = impressions.drop('ts', axis=1)

"""### Análise estatística"""

#ANÁLISE DE OUTLIERS DE IMPRESSIONS
Q1 = impressions['impressions'].quantile(0.25)
Q3 = impressions['impressions'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q1 + 1.5 * IQR
outliers = impressions[(impressions['impressions'] < lower_bound) | (impressions['impressions'] > upper_bound)]


impressions_no_outliers = impressions[(impressions['impressions'] >= lower_bound) & (impressions['impressions'] <= upper_bound)]



"""realizando o tratamento de outliers, 162 registros foram removidos. A média tornou a sua normalidade, de 35 impressões, agora ficou 26

### SEGMENT
"""

#verificando a soma de impressions por segment
seg_grouped = impressions_no_outliers.groupby('segment')['impressions'].sum()
seg_sorted = seg_grouped.sort_values(ascending=False)



impressions_no_outliers['segment'].value_counts()

seg_counts = pd.DataFrame(impressions_no_outliers['segment'].value_counts())

seg_sort = pd.DataFrame(seg_sorted)

analise_seg = pd.merge(seg_counts, seg_sort, on=['segment'])

analise_seg['proporcao'] = analise_seg['impressions'] / analise_seg['count']



"""💡 Vimos aqui que a por mais que o seg2 seja maior em impressões totais, proporcionalmente pelo número de vezes em que se repete, os que possuem mais comentários são seg1 e seg3.

### AD
"""

#realizando a mesma análise para ad
ad_grouped = impressions_no_outliers.groupby('ad')['impressions'].sum()
ad_sorted = ad_grouped.sort_values(ascending=False)




ad_counts = pd.DataFrame(impressions_no_outliers['ad'].value_counts())
ad_sort = pd.DataFrame(ad_sorted)
analise_ad = pd.merge(ad_counts, ad_sort, on=['ad'])

analise_ad['proporcao'] = analise_ad['impressions'] / analise_ad['count']




weekday_grouped = impressions_no_outliers.groupby('day_of_week')['impressions'].sum()
weekday_sorted = weekday_grouped.sort_values(ascending=False)


weekday_counts = pd.DataFrame(impressions_no_outliers['day_of_week'].value_counts())
weekday_sort = pd.DataFrame(weekday_sorted)
analise_weekday = pd.merge(weekday_counts, weekday_sort, on=['day_of_week'])

analise_weekday['proporcao'] = analise_weekday['impressions'] / analise_weekday['count']




conversions['date'] = pd.to_datetime(conversions['date'])
conversions['day_of_week'] = conversions['date'].dt.day_name()

"""### Análise estatística"""

#ANÁLISE DE OUTLIERS DE Conversions
Q1 = conversions['conversions'].quantile(0.25)
Q3 = conversions['conversions'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q1 + 1.5 * IQR
outliers = conversions[(conversions['conversions'] < lower_bound) | (conversions['conversions'] > upper_bound)]


conversions_no_outliers = conversions[(conversions['conversions'] >= lower_bound) & (conversions['conversions'] <= upper_bound)]




seg_grouped_cv = conversions_no_outliers.groupby('segment')['conversions'].sum()
seg_sorted_cv = seg_grouped_cv.sort_values(ascending=False)


seg_counts_cv = pd.DataFrame(conversions_no_outliers['segment'].value_counts())



seg_sort_cv = pd.DataFrame(seg_sorted_cv)

analise_seg_cv = pd.merge(seg_counts_cv, seg_sort_cv, on=['segment'])

analise_seg_cv['proporcao'] = analise_seg_cv['conversions'] / analise_seg_cv['count']




ad_grouped_cv = conversions_no_outliers.groupby('ad')['conversions'].sum()
ad_sorted_cv = ad_grouped_cv.sort_values(ascending=False)

ad_counts_cv = pd.DataFrame(conversions_no_outliers['ad'].value_counts())
ad_sort_cv = pd.DataFrame(ad_sorted_cv)

analise_ad_cv = pd.merge(ad_counts_cv, ad_sort_cv, on=['ad'])

analise_ad_cv['proporcao'] = analise_ad_cv['conversions'] / analise_ad_cv['count']



weekday_grouped_cv = conversions_no_outliers.groupby('day_of_week')['conversions'].sum()
weekday_sorted_cv = weekday_grouped_cv.sort_values(ascending=False)


weekday_counts_cv = pd.DataFrame(conversions_no_outliers['day_of_week'].value_counts())
weekday_sort_cv = pd.DataFrame(weekday_sorted_cv)

analise_weekday_cv = pd.merge(weekday_counts_cv, weekday_sort_cv, on=['day_of_week'])

analise_weekday_cv['proporcao'] = analise_weekday_cv['conversions'] / analise_weekday_cv['count']


data = pd.merge(impressions_no_outliers, conversions_no_outliers, on=['ad','segment'])


data_ad_seg = data.groupby(['ad','segment'])[['impressions','conversions']].sum().reset_index()

data_ad_seg['conversion rate'] = data_ad_seg['conversions'] / data_ad_seg['impressions']




data['conversion rate'] = data['conversions'] / data['impressions']


date = pd.DataFrame({
    'date': pd.date_range(start='1/1/2024', end='12/31/2024')
})

data_new = pd.merge(date, conversions_no_outliers, on=['date'], how='left')

data_new = pd.merge(data_new, impressions_no_outliers, on=['date'], how='left')


data_new['conversions'] = data_new['conversions'].fillna(0)
data_new['impressions'] = data_new['impressions'].fillna(0)

data_new['conversion rate'] = data_new['conversions'] / data_new['impressions']

data_new['conversion rate'] = data_new['conversion rate'].fillna(0)

print(len(data_new[(data_new['impressions'] > 0)]))




data_new['weekday'] = data_new['date'].dt.day_name()



data_filtered = data_new[(data_new['impressions'] > 0) ]#| (data_new['conversions'] > 0)]

# Realizar a operação de agrupamento no DataFrame filtrado
grouped = data_filtered.groupby(['ad_x','segment_x','weekday'])['impressions'].sum()



# grouped.to_csv('./datasets/ad_seg_day2.csv')

# data_new.to_csv('./datasets/dataset_tratado.csv')
# """A sequência seguirá no próximo arquivo, com o streamlit"""

