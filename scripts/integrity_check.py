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
img_path = 'C:/Users/Francisco Valerio/Desktop/Gubernatura_024_TEHUACAN_1972_B01.jpg'


codigo_integridad = '9b93735b01863b5e3e2b891b8aa9171698d77b46a0e7a04e864d8a76e355e3ec'

hash_calculado = calcular_sha256(img_path)

print("Programa de verificación de actas.")
print()
print(f"SHA-256 imagen: {hash_calculado}")
print(f"Código de integridad (BDD): {codigo_integridad}")

print()
print()

if hash_calculado == codigo_integridad:

    print("El SHA-256 del Acta coincide. No hay alteración.")
    
else:
    print("El SHA-256 del Acta no coincide. Hay alteración.")