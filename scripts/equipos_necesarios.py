# Definiendo los tiempos promedio de procesamiento en minutos
tiempo_gubernatura = 124.01
tiempo_diputaciones = 127.24
tiempo_ayuntamientos = 116.51

# Número total de actas por categoría
actas_gubernatura = 8338 * 0.9
actas_diputaciones = 8414 * 0.9
actas_ayuntamientos = 8356 * 0.9

# Tiempo disponible para procesar las actas en minutos (desde las 20:00 horas del 2 de junio hasta las 23:59 horas del 3 de junio)
tiempo_disponible = (23 * 60 + 59) + 12 * 60

# Calculando el tiempo total requerido para procesar todas las actas en cada categoría
total_minutos_gubernatura = actas_gubernatura * tiempo_gubernatura 
total_minutos_diputaciones = actas_diputaciones * tiempo_diputaciones 
total_minutos_ayuntamientos = actas_ayuntamientos * tiempo_ayuntamientos 

# Sumando el tiempo total necesario para procesar todas las actas
tiempo_total_requerido = total_minutos_gubernatura + total_minutos_diputaciones + total_minutos_ayuntamientos

# Calculando cuántos equipos de captura son necesarios para cumplir con el intervalo de tiempo
equipos_necesarios = tiempo_total_requerido / tiempo_disponible
print(equipos_necesarios)


# # Datos proporcionados
# actas_gubernatura = 8338
# actas_diputaciones = 8414
# actas_ayuntamientos = 8356

# tiempo_por_acta_gubernatura = 13.44  # minutos
# tiempo_por_acta_diputaciones = 13.36  # minutos
# tiempo_por_acta_ayuntamientos = 13.69  # minutos

# # Calcular el 90% del número total de actas para cada tipo de elección
# actas_gubernatura_90 = actas_gubernatura * 0.9
# actas_diputaciones_90 = actas_diputaciones * 0.9
# actas_ayuntamientos_90 = actas_ayuntamientos * 0.9

# # Calcular el tiempo total necesario para procesar el 90% de las actas de cada tipo de elección
# tiempo_necesario_gubernatura = actas_gubernatura_90 * tiempo_por_acta_gubernatura
# tiempo_necesario_diputaciones = actas_diputaciones_90 * tiempo_por_acta_diputaciones
# tiempo_necesario_ayuntamientos = actas_ayuntamientos_90 * tiempo_por_acta_ayuntamientos

# # Tiempo total disponible en minutos
# tiempo_disponible = 4 * 60  # 4 horas en minutos

# # Calcular el número de equipos necesarios para cada tipo de elección
# equipos_necesarios_gubernatura = tiempo_necesario_gubernatura / tiempo_disponible
# equipos_necesarios_diputaciones = tiempo_necesario_diputaciones / tiempo_disponible
# equipos_necesarios_ayuntamientos = tiempo_necesario_ayuntamientos / tiempo_disponible

# # Calcular el número total de equipos necesarios
# total_equipos_necesarios = equipos_necesarios_gubernatura + equipos_necesarios_diputaciones + equipos_necesarios_ayuntamientos

# # Redondear al siguiente número entero
# total_equipos_necesarios = int(total_equipos_necesarios) + 1 if total_equipos_necesarios % 1 > 0 else int(total_equipos_necesarios)

# print(f"Número total de equipos necesarios: {total_equipos_necesarios}")