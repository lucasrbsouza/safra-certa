# 🌾 SafraCerta

<div align="center">

**Simulador de Viabilidade Financeira para Produtores Rurais**

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Vue](https://img.shields.io/badge/Vue.js-3-42b883)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![License](https://img.shields.io/badge/License-Apache%202.0-orange)

Projeto desenvolvido para a disciplina de **Estágio Curricular Supervisionado — Fábrica de Software I**

</div>

---

## Simulador de Viabilidade Financeira para Produtores Rurais

Projeto desenvolvido para a disciplina de **Estágio Curricular Supervisionado — Fábrica de Software I** (*Março de 2026*).

---

## 📖 Sobre o Projeto

O setor agropecuário brasileiro é caracterizado por alta exposição a riscos de mercado e volatilidade de preços.

O **SafraCerta** é um ecossistema de software concebido como um **Dashboard de Simulação Financeira** para auxiliar produtores rurais (especialmente pequenos e médios), gestores e cooperativas.

O sistema cruza dados de custos estimados de produção (*insumos, combustível, mão de obra*) com cotações de mercado em tempo real de commodities (**soja, milho e feijão**).

Com isso, realiza o cálculo do **Ponto de Equilíbrio (Break-even Point)**, revelando a quantidade exata de sacas por hectare necessárias para cobrir os custos operacionais e atingir o lucro.

---

## 🎯 Principais Funcionalidades

### Cadastro de Custos Operacionais

Inserção detalhada de custos por hectare:

* Sementes
* Fertilizantes
* Defensivos
* Mão de obra
* Combustível
* Outros custos operacionais

### Monitoramento de Mercado

Cotações atualizadas das culturas:

* 🌱 Soja
* 🌽 Milho
* 🫘 Feijão

Integração via **API HG Brasil** ou uso de dados simulados.

### Cálculo Dinâmico de Viabilidade

Projeção imediata de:

* Ponto de equilíbrio
* Custo total
* Preço de venda
* Margem de lucro

### Suporte à Decisão Visual

Indicadores gráficos (*velocímetro de viabilidade*) que apontam se o cenário atual está:

* ✅ **Viável**
* ❌ **Inviável**

---

## 🛠️ Tecnologias Utilizadas

O projeto segue uma arquitetura **Cliente-Servidor clássica**, com separação clara de responsabilidades.

### Backend (API REST)

* Python 3.12
* FastAPI
* SQLAlchemy
* PostgreSQL
* Uvicorn
* Pytest

### Frontend (SPA)

* Vue.js 3 (Composition API)
* Vite
* Pinia
* Vue Router
* Axios

### Infraestrutura

* Docker
* Docker Compose
* Nginx

---

## 🚀 Como Executar o Projeto

A forma mais simples de rodar o **SafraCerta** é via Docker.

O projeto já inclui um `docker-compose.yml` responsável por subir:

* Banco de dados
* API Backend
* Frontend

### Pré-requisitos

* Docker instalado
* Docker Compose instalado

### 1. Clone o repositório

```bash
git clone https://github.com/lucasrbsouza/safra-certa.git
cd safra-certa
```

### 2. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

**Opcional:**
Caso possua uma chave da HG Brasil:

* Defina `HG_BRASIL_API_KEY`
* Altere `COMMODITY_PROVIDER=hgbrasil`

Por padrão, o sistema roda em **modo mock (simulado)**.

### 3. Suba os containers

```bash
docker-compose up -d --build
```

### 4. Acesse as aplicações

**Frontend**
`http://localhost:5173`

**Swagger da API**
`http://localhost:8000/docs`

---

## 🧪 Rodando os Testes (Backend)

O backend possui uma suíte automatizada de testes unitários e de integração.

Execute com:

```bash
docker-compose exec backend pytest
```

---

## 📂 Estrutura do Projeto

```text
safra-certa/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── domain/
│   │   ├── gateways/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   └── services/
│   ├── tests/
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── composables/
│   │   ├── pages/
│   │   ├── router/
│   │   ├── services/
│   │   └── stores/
│   └── index.html
│
├── database/
└── docker-compose.yml
```

---

## 👥 Equipe Desenvolvedora

### José Lucas Silva Souza

**Scrum Master / Lead Dev**
Modelagem do banco de dados, segurança e arquitetura backend

### Guilherme Gomes Benigno

**Product Owner**
Validação de regras de negócio, requisitos e QA

### Alcimar Rosal Benvindo Filho

**Fullstack Developer**
Frontend Vue.js, integrações e UX/UI

---

## 📄 Licença

Este projeto está licenciado sob a **Apache License 2.0**.

