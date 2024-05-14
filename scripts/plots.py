import pandas as pd
import plotly.express as px

data = pd.read_csv('C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/Data adicional/totales_simulacro_1.csv')

data['Porcentaje_Capturadas'] = ((data['Capturadas'] / data['Esperadas']) * 100).round(4)

group_porcentaje_capt = data.groupby('Tipo_eleccion')['Porcentaje_Capturadas'].mean().reset_index()

print(group_porcentaje_capt)
# for tipo in group_porcentaje_cont['Tipo_eleccion'].unique():

#     fig = px.pie(group_porcentaje_cont[group_porcentaje_cont['Tipo_eleccion'] == tipo], 
#                  values = 'Porcentaje_Contabilizado',
#                  names = 'Tipo_eleccion',
#                  title = f'Porcentaje de Actas contabilizadas para {tipo}')
    
#     fig.show()

fig = px.pie(group_porcentaje_capt, values='Porcentaje_Capturadas', names='Tipo_eleccion',
             title='Porcentaje Contabilizado por Tipo de Elección',
             color_discrete_sequence=px.colors.qualitative.Prism,
             )

fig.update_traces(textposition = 'inside',
                  texttemplate = '%{label}: %{value:.2f}%',
                  textfont_size = 20)

fig.update_layout(uniformtext_minsize = 18, uniformtext_mode = 'hide')
fig.show()