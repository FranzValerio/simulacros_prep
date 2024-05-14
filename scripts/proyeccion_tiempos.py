import numpy as np
from datetime import datetime, timedelta

total_actas_gub = 8321
total_actas_dip = 8398
total_actas_ayun = 8350
tiempo_procesamiento_disponible = 596

actas_capturadas_gub = 3559
actas_capturadas_dip = 4616
actas_capturadas_ayun = 2101

tiempo_prom_acta_gub = 13.42
tiempo_prom_acta_dip = 13.34
tiempo_prom_acta_ayun = 13.68

tiempo_proyectado_total_gub = tiempo_prom_acta_gub * total_actas_gub
tiempo_proyectado_total_dip = tiempo_prom_acta_dip * total_actas_dip
tiempo_proyectado_total_ayun = tiempo_prom_acta_ayun * total_actas_ayun

tiempo_restante_gub = (tiempo_proyectado_total_gub - tiempo_procesamiento_disponible)/60
tiempo_restante_dip = (tiempo_proyectado_total_dip - tiempo_procesamiento_disponible)/60
tiempo_restante_ayun = (tiempo_proyectado_total_ayun - tiempo_procesamiento_disponible)/60

hora_inicio = datetime(2024, 5, 12, 10, 0)

hora_estimada_finalizacion_gub = hora_inicio + timedelta(minutes = tiempo_restante_gub)
hora_estimada_finalizacion_dip = hora_inicio + timedelta(minutes =  tiempo_restante_dip)
hora_estimada_finalizacion_ayun = hora_inicio + timedelta(minutes = tiempo_restante_ayun)

print(f"La fecha estimada para procesar el 100% de las actas de gubernatura, al ritmo llevado en el simulacro sería: {hora_estimada_finalizacion_gub}")
print(f"La fecha estimada para procesar el 100% de las actas de diputaciones, al ritmo llevado en el simulacro sería: {hora_estimada_finalizacion_dip}")
print(f"La fecha estimada para procesar el 100% de las actas de ayuntamientos, al ritmo llevado en el simulacro sería: {hora_estimada_finalizacion_ayun}")

