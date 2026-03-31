# 📊 Análise de Dados de Vacinação do SUS

## 📌 Introdução

Este projeto tem como finalidade desenvolver uma aplicação para análise de dados públicos de vacinação disponibilizados pelo Sistema Único de Saúde (SUS).

A aplicação consome dados de uma API pública, realiza o tratamento das informações utilizando Python e apresenta análises estatísticas por meio de um dashboard interativo com Streamlit.

---

## 🎯 Objetivo Geral

Desenvolver uma aplicação que transforme dados públicos de vacinação em análises estatísticas claras e úteis, apresentadas através de visualizações interativas.

---

## ✅ Objetivos Específicos

* Consumir dados da API pública de vacinação
* Realizar tratamento e limpeza dos dados
* Aplicar análises com pandas
* Desenvolver dashboard com Streamlit
* Exibir indicadores relevantes sobre vacinação

---

## 🌐 Fonte de Dados

Os dados são obtidos por meio da:

**API Dados Abertos Saúde - Vacinação PNI 2025**
Disponibiliza informações públicas relacionadas às doses aplicadas no Programa Nacional de Imunizações.

---

## 🛠️ Tecnologias Utilizadas

* Python
* requests
* pandas
* Streamlit
* API Dados Abertos do SUS

---

## 📊 Escopo do Projeto

O sistema realiza análise dos dados de vacinação considerando:

* Pessoas vacinadas fora da cidade de residência
* Distribuição por sexo
* Vacinas mais aplicadas
* Distribuição por faixa etária
* Distribuição por cor/raça

---

## 📏 Regras de Negócio

* Apenas registros válidos serão utilizados
* Registros com valores nulos poderão ser desconsiderados
* Idades serão agrupadas em faixas etárias
* Comparação entre município de residência e vacinação
* Contagem baseada no tipo de vacina aplicada
* Padronização de valores categóricos

---

## 🚫 Limitações do Projeto

O projeto não contempla:

* Persistência em banco de dados
* Sistema de autenticação
* Inserção ou edição de dados
* Integração com múltiplas APIs

---

## 📈 Resultados Esperados

A aplicação deverá permitir identificar:

* Quantidade de pessoas vacinadas fora da cidade
* Distribuição da vacinação por sexo
* Ranking das vacinas mais aplicadas
* Distribuição por faixa etária
* Distribuição por cor/raça

---

## ⚠️ Considerações

* A aplicação depende da disponibilidade da API pública
* Mudanças na API podem impactar o sistema
* Dados devem ser validados antes do uso
* Registros inconsistentes podem ser descartados
* Não há persistência de dados (consulta em tempo real)
* A performance depende do volume retornado pela API

---

## ▶️ Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_PROJETO>
```

### 2. Criar ambiente virtual (opcional, recomendado)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

Caso ainda não tenha o arquivo:

```bash
pip freeze > requirements.txt
```

---

### 4. Executar a aplicação

```bash
streamlit run index.py
```

---

## 💻 Estrutura Básica do Projeto

```
📁 projeto
 ┣ 📄 index.py
 ┣ 📄 requirements.txt
 ┗ 📄 README.md
```