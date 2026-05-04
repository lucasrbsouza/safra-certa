# 🤝 Contribuindo com o SafraCerta

Obrigado pelo interesse em contribuir com o **SafraCerta**.

Este projeto foi desenvolvido com foco acadêmico e tem como objetivo evoluir continuamente como ferramenta de apoio à tomada de decisão no setor agropecuário.

Toda contribuição é bem-vinda.

---

## 📌 Como Contribuir

Você pode contribuir de diferentes formas:

* Reportando bugs
* Sugerindo melhorias
* Corrigindo problemas existentes
* Melhorando a documentação
* Implementando novas funcionalidades
* Escrevendo testes

---

## 🚀 Configuração do Ambiente

### 1. Faça um fork do projeto

```bash
git fork https://github.com/lucasrbsouza/safra-certa.git
```

### 2. Clone seu fork

```bash
git clone https://github.com/seu-usuario/safra-certa.git
cd safra-certa
```

### 3. Configure o ambiente

```bash
cp .env.example .env
```

### 4. Suba os containers

```bash
docker-compose up -d --build
```

---

## 🌱 Fluxo de Desenvolvimento

Crie uma branch para sua contribuição:

```bash
git checkout -b feature/nome-da-feature
```

Exemplos:

* `feature/dashboard-graficos`
* `fix/calculo-break-even`
* `docs/atualizacao-readme`

---

## 🧪 Testes

Antes de enviar qualquer alteração, execute os testes:

```bash
docker-compose exec backend pytest
```

Se adicionar nova regra de negócio, inclua testes correspondentes.

---

## 📝 Padrões de Código

### Backend (Python)

* Seguir **PEP 8**
* Utilizar tipagem estática sempre que possível
* Priorizar separação por camadas
* Manter regras de negócio desacopladas

### Frontend (Vue)

* Utilizar Composition API
* Componentes reutilizáveis
* Nomeação clara e consistente
* Evitar lógica complexa dentro das views

---

## 💬 Commits

Utilize commits semânticos:

```text
feat: adiciona cálculo de margem líquida
fix: corrige erro na integração com HG Brasil
docs: atualiza instruções de instalação
test: adiciona testes do simulador
refactor: reorganiza camada de serviços
```

---

## 🔍 Pull Requests

Ao abrir um Pull Request:

1. Explique claramente a mudança
2. Relacione com issue (se existir)
3. Inclua evidências/testes
4. Garanta que tudo esteja funcionando

---

## 🐛 Reportando Problemas

Ao abrir uma issue, informe:

* Descrição detalhada
* Passos para reproduzir
* Resultado esperado
* Resultado atual
* Logs (se aplicável)

---

## 📜 Código de Conduta

Esperamos interações respeitosas e colaborativas.

Críticas técnicas são bem-vindas; ataques pessoais, não.

---

## 🌾 Obrigado

Sua contribuição ajuda o **SafraCerta** a evoluir como ferramenta tecnológica para o agronegócio brasileiro.
