import requests

url = "https://cartografia.ife.org.mx/sige7/views/cartografia/ajax/get_municipio.php"

response = requests.get(url)

with open("get_mun.json", 'wb') as f:

    f.write(response.content)

