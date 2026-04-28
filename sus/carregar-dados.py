import requests
import json
import os

BASE_URL = "https://apidadosabertos.saude.gov.br/vacinacao/doses-aplicadas-pni-2025"
ARQUIVO = "vacinas_2025.json"


def buscar_todos_dados():
    dados_totais = []
    offset = 0
    limit = 500

    try:
        while True:
            print(f"Buscando offset={offset}")

            response = requests.get(
                BASE_URL,
                params={"limit": limit, "offset": offset},
                headers={"accept": "application/json"},
                timeout=10
            )

            if response.status_code != 200:
                print("Erro:", response.status_code)
                break

            data = response.json()
            registros = data.get("doses_aplicadas_pni", [])

            if not registros:
                break

            dados_totais.extend(registros)

            offset += 1

        # salva no arquivo
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(dados_totais, f, ensure_ascii=False, indent=2)

        print("Dados salvos com sucesso!")
        return dados_totais

    except Exception as e:
        print("Erro na API:", e)

        if os.path.exists(ARQUIVO):
            print("Usando backup local...")
            with open(ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return None


dados = buscar_todos_dados()
print(f"Total: {len(dados) if dados else 0}")