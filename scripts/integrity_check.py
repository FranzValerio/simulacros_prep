import hashlib

def calcular_sha256(file):
    """
    Calcula el hash SHA-256 del archivo proporcionado.
    
    :: Ruta al archivo de la imagen del acta.
    :return: Cadena con el hash SHA-256.
    """
    sha256 = hashlib.sha256()

    with open(file, 'rb') as f:

        for bloque in iter(lambda: f.read(4096), b''):

            sha256.update(bloque)

    return sha256.hexdigest()

# Ruta al archivo de la imagen del acta
# img_path = 'C:/Users/Francisco Valerio/Desktop/Gubernatura_024_TEHUACAN_1972_B01.jpg'


# codigo_integridad = '9b93735b01863b5e3e2b891b8aa9171698d77b46a0e7a04e864d8a76e355e3ec'

# hash_calculado = calcular_sha256(img_path)

gub_3junio = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/BDD/PUE_GUB_2024.csv'
gub_26junio = 'C:/Users/Francisco Valerio/Downloads/20240603_2000_PREP_PUE(1)/20240603_2000_PREP_GUB_PUE/PUE_GUB_2024.csv'

dip_3junio = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/BDD/PUE_DIP_LOC_2024.csv'
dip_26junio = 'C:/Users/Francisco Valerio/Downloads/20240603_2000_PREP_PUE(1)/20240603_2000_PREP_DIP_LOC_PUE/PUE_DIP_LOC_2024.csv'

ayun_3junio = 'C:/Users/Francisco Valerio/Desktop/INE/Simulacros/simulacros_prep/BDD/PUE_AYUN_2024.csv'
ayun_26junio =  'C:/Users/Francisco Valerio/Downloads/20240603_2000_PREP_PUE(1)/20240603_2000_PREP_AYUN_PUE/PUE_AYUN_2024.csv'


hash_gub_3junio = calcular_sha256(gub_3junio)
hash_gub_26junio = calcular_sha256(gub_26junio)

hash_dip_3junio = calcular_sha256(dip_3junio)
hash_dip_26junio = calcular_sha256(dip_26junio)

hash_ayun_3junio = calcular_sha256(ayun_3junio)
hash_ayun_26junio = calcular_sha256(ayun_26junio)

print("Programa de verificación de actas.")
print()
print(f"SHA-256 GUB (3 de junio): {hash_gub_3junio}")
print(f"SHA-256 GUB (26 de junio): {hash_gub_26junio}")
print()
print()

if hash_gub_3junio == hash_gub_26junio:

    print("El SHA-256 de la Base de datos de Gubernatura coincide. No hay alteración.")
    
else:
    print("El SHA-256 de la Base de datos de Gubernatura no coincide. Hay alteración.")

print()
print(f"SHA-256 DIP (3 de junio): {hash_dip_3junio}")
print(f"SHA-256 DIP (26 de junio): {hash_dip_26junio}")
print()
print()

if hash_dip_3junio == hash_dip_26junio:

    print("El SHA-256 de la Base de datos de Diputaciones coincide. No hay alteración.")
    
else:
    print("El SHA-256 de la Base de datos de Gubernatura no coincide. Hay alteración.")

print()
print(f"SHA-256 AYUN (3 de junio): {hash_ayun_3junio}")
print(f"SHA-256 AYUN (26 de junio): {hash_ayun_26junio}")
print()
print()

if hash_ayun_3junio == hash_ayun_26junio:

    print("El SHA-256 de la Base de datos de Ayuntamientos coincide. No hay alteración.")
    
else:
    print("El SHA-256 de la Base de datos de Ayuntamientos no coincide. Hay alteración.")

