import requests

url = "https://api.coingecko.com/api/v3/coins/markets"

parametros = {
    "vs_currency": "brl",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1
}
resposta = requests.get(url,params=parametros)

print(resposta.status_code)#TESTE
for cripto in resposta.json():
    print("Nome:", cripto["name"])
    print("Preço:", cripto["current_price"])
    print("Ranking:",  cripto["market_cap_rank"])
    print("Variaçao 24h:", cripto["price_change_percentage_24h"])
    print("-" * 25)