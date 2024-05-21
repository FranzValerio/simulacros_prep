import pandas as pd

file_path = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/BDD_Simulacro_2/PUE_GUB_2024.csv'

with open(file_path, 'r', encoding='utf-8') as file:

    lines = file.readlines()

first_five_rows = lines[4:5]

column_names = lines[3].strip().split(',')
data_first_five = [line.strip().split(',') for line in first_five_rows]

df_first_five = pd.DataFrame(data_first_five, columns=column_names)

print(df_first_five)

