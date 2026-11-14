# Frontend - ParkingAlot

Interface em Vue 3 + Vite + TypeScript para controle de estacionamento. O visual segue o protótipo em `docs/prototipo/`.

## Requirements

- Node.js 22.18+
- Backend rodando em `http://127.0.0.1:5000`

## Setup

```bash
cd frontend
npm install
```

## Run

```bash
npm run dev
```

## Format

```bash
npm run format
```

## Estrutura

```
src/
├── assets/       # CSS global e variáveis (tokens.css)
├── components/   # componentes reutilizáveis
├── router/       # rotas
├── services/     # chamadas à API
├── stores/       # stores do Pinia
└── views/        # uma view por tela
```

## Nova tela

1. Crie `src/views/NomeView.vue`.
2. Adicione a rota em `src/router/index.ts`.
3. Coloque as chamadas à API em `src/services/nome.ts`.

## Convenções

- Componentes e views em PascalCase (`BaseButton.vue`, `VagasView.vue`).
- Chamadas à API só em `src/services/`. Rotas de listagem e criação terminam com barra (`/vagas/`).
- Cores e medidas só pelas variáveis do `tokens.css`.

## Telas

| Tela          | Rota                   | Endpoints                                                             | Responsável |
| ------------- | ---------------------- | --------------------------------------------------------------------- | ----------- |
| Login         | `/login`               | `POST /login/`                                                        |             |
| Mapa de vagas | `/`                    | `GET /vagas/`, `GET /registros/`, `GET /veiculos/:placa`              |             |
| Entrada       | `/entrada`             | `GET /veiculos/:placa`, `GET /vagas/`, `POST /registros/`             |             |
| Saída         | `/registros/:id/saida` | `GET /registros/:id`, `PUT /registros/:id/saida`, `POST /pagamentos/` |             |
| Registros     | `/registros`           | `GET`, `PUT`, `DELETE /registros/`                                    |             |
| Pagamentos    | `/pagamentos`          | `GET /pagamentos/`                                                    |             |
| Veículos      | `/veiculos`            | `GET`, `POST`, `PUT`, `DELETE /veiculos/`                             |             |
| Colaboradores | `/colaboradores`       | `GET`, `POST`, `PUT`, `DELETE /colaboradores/`                        |             |
| Guardas       | `/guardas`             | `GET`, `POST`, `PUT`, `DELETE /guardas/`                              |             |
| Vagas         | `/vagas`               | `GET`, `POST`, `PUT /vagas/`                                          |             |
