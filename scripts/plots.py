import pandas as pd
import plotly.express as px

data = pd.read_csv('C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/Data adicional/totales_simulacro_1.csv')

data['Porcentaje_Capturadas'] = ((data['Capturadas'] / data['Esperadas']) * 100).round(4)

data['Porcentaje_Contabilizadas'] = ((data['Contabilizadas'] / data['Esperadas'] * 100)).round(4)

group_porcentaje_capt = data.groupby('Tipo_eleccion')['Porcentaje_Capturadas'].mean().reset_index()

group_porcentaje_cont = data.groupby('Tipo_eleccion')['Porcentaje_Contabilizadas'].mean().reset_index()

print(group_porcentaje_capt)

print(group_porcentaje_cont)
# for tipo in group_porcentaje_cont['Tipo_eleccion'].unique():

#     fig = px.pie(group_porcentaje_cont[group_porcentaje_cont['Tipo_eleccion'] == tipo], 
#                  values = 'Porcentaje_Contabilizado',
#                  names = 'Tipo_eleccion',
#                  title = f'Porcentaje de Actas contabilizadas para {tipo}')
    
#     fig.show()

fig_1 = px.pie(group_porcentaje_capt, values='Porcentaje_Capturadas', names='Tipo_eleccion',
             title='Porcentaje de Actas Capturadas por Tipo de Elección',
             color_discrete_sequence=px.colors.qualitative.Prism,
             )

fig_1.update_traces(textposition = 'inside',
                  texttemplate = '%{label}: %{value:.2f}%',
                  textfont_size = 20)

fig_1.update_layout(uniformtext_minsize = 18, uniformtext_mode = 'hide',
                    title = {
                        'text': "Porcentaje de Actas Capturadas por Tipo de Elección",
                        'font': {'size': 25}
                    },
                    legend_title_text = 'Tipo de Elección',
                    legend = dict(font_size = 18, title_font_size = 25))
fig_1.show()


fig_2 = px.pie(group_porcentaje_cont, values='Porcentaje_Contabilizadas', names='Tipo_eleccion',
             title='Porcentaje de Actas Contabilizadas por Tipo de Elección',
             color_discrete_sequence=px.colors.qualitative.Safe,
             )

fig_2.update_traces(textposition = 'inside',
                  texttemplate = '%{label}: %{value:.2f}%',
                  textfont_size = 20)

fig_2.update_layout(uniformtext_minsize = 18, uniformtext_mode = 'hide',
                    title = {
                        'text': "Porcentaje de Actas Contabilizadas por Tipo de Elección",
                        'font': {'size': 25}
                    },
                    legend_title_text = 'Tipo de Elección',
                    legend = dict(font_size = 18, title_font_size = 25))

fig_2.show()