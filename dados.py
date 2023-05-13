# importando bibliotecas necessárias
import requests
import json

# link contendo a api
api_link = "https://dicio-api-ten.vercel.app/v2/palavra"

# requests
r = requests.get(api_link)

# convertendo os dados do request em dicionário
dados = r.json()

print(dados)
