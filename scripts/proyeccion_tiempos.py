import numpy as np
from datetime import datetime, timedelta

hora_inicio = datetime(2024, 5, 17, 10, 30)

fecha_corte = datetime(2024, 5, 17, 21, 00) # modificar de acuerdo a la BDD

diff_tiempo = fecha_corte - hora_inicio # Tiempo entre inicio y corte de la inf


total_actas_gub = 8338
total_actas_dip = 8414
total_actas_ayun = 8356

tiempo_procesamiento_disponible = diff_tiempo.total_seconds() / 60 # tiempo que ha pasado desde el inicio de la captura a la fecha de corte

# El 596 correspondía al tiempo que había pasado entre las 10:00 am y las 19:43 12/05

actas_capturadas_gub = 8338
actas_capturadas_dip = 8414
actas_capturadas_ayun = 8356

tiempo_prom_acta_gub = 124.01
tiempo_prom_acta_dip = 127.24
tiempo_prom_acta_ayun = 116.51

tiempo_proyectado_total_gub = tiempo_prom_acta_gub * total_actas_gub
tiempo_proyectado_total_dip = tiempo_prom_acta_dip * total_actas_dip
tiempo_proyectado_total_ayun = tiempo_prom_acta_ayun * total_actas_ayun

tiempo_restante_gub = (tiempo_proyectado_total_gub - tiempo_procesamiento_disponible)/60
tiempo_restante_dip = (tiempo_proyectado_total_dip - tiempo_procesamiento_disponible)/60
tiempo_restante_ayun = (tiempo_proyectado_total_ayun - tiempo_procesamiento_disponible)/60

hora_estimada_finalizacion_gub = hora_inicio + timedelta(minutes = tiempo_restante_gub)
hora_estimada_finalizacion_dip = hora_inicio + timedelta(minutes =  tiempo_restante_dip)
hora_estimada_finalizacion_ayun = hora_inicio + timedelta(minutes = tiempo_restante_ayun)

print(f"Fecha de corte de la información: {fecha_corte}")
print(f"La fecha estimada para procesar el 100% de las actas de gubernatura, al ritmo llevado en el simulacro sería: {hora_estimada_finalizacion_gub}")
print(f"La fecha estimada para procesar el 100% de las actas de diputaciones, al ritmo llevado en el simulacro sería: {hora_estimada_finalizacion_dip}")
print(f"La fecha estimada para procesar el 100% de las actas de ayuntamientos, al ritmo llevado en el simulacro sería: {hora_estimada_finalizacion_ayun}")

