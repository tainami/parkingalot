# Frontend - ParkingAlot

Interface em Vue 3 + Vite + TypeScript para controle de estacionamento.

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
├── assets/       # CSS global e variáveis
├── components/   # componentes reutilizáveis
├── router/       # rotas
├── services/     # chamadas à API
├── stores/       # stores do Pinia
├── types/        # tipos compartilhados
├── utils/        # formatação, cálculo de tarifa e exportação para Excel
└── views/        # uma view por tela
```
