import streamlit as st
import pandas as pd

jobsdata = pd.read_csv('oficios.csv')

job_current = st.number_input('Job current level', min_value=0, max_value=199, value=0, step=1, key='job_level')
job_wanted = st.number_input('Job wanted level', min_value=0, max_value=200, value=200, step=1, key='job_wanted_level')
job_type = st.selectbox('Job type', jobsdata['Oficio'].unique(), index=0, key='job_type')

if st.button('Filter jobs data'):
    jobsdata = jobsdata[jobsdata['Oficio'] == job_type]

format_data = jobsdata[['id', 'Oficio', 'Niveles', 'Recetas', 'Recursos', 'Cantidad']]

st.dataframe(format_data)

filtered_data = jobsdata[(jobsdata['Niveles'] >= job_current) & (jobsdata['Niveles'] < job_wanted)]
format_data2 = filtered_data.groupby(['Recursos']).agg({'Cantidad': 'sum', 'Niveles': 'min'})
format_data2.sort_values(by=['Niveles', 'Cantidad'], ascending=[True, False], inplace=True)
format_data2['Collected?'] = False

st.title('To Collect')
st.data_editor(
    format_data2
)

st.title('To Craft')

filtered_data_craft = jobsdata[(jobsdata['Niveles'] >= job_current) & (jobsdata['Niveles'] < job_wanted)]
format_data3 = filtered_data_craft[['Recetas', 'Niveles']].drop_duplicates().sort_values(by='Niveles')
format_data3['Crafted?'] = False
st.data_editor(
    format_data3
)