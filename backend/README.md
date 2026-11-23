# Backend - ParkingAlot
 
REST API em Flask + SQLAlchemy para controle de estacionamento.
 
## Requirements
 
- Python 3.12+

## Setup
 
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
 
## Environment variables
 
`.env` na pasta `backend/`:
 
```
DATABASE_URL=sqlite:///parkingalot.db
```
 
## Run
 
```bash
python run.py
```
 
Server: `http://127.0.0.1:5000`
 
## First guard

```bash
flask --app run criar-guarda
```

CPF só com números; turno `Manhã`, `Tarde` ou `Noite`.

## Sample data

```bash
flask --app run popular-banco
```

Cria vagas, colaboradores, veículos e registros de exemplo. Rode depois do `criar-guarda`.

## Lint / Format (Ruff)
 
```bash
ruff check .
ruff format .
```
 
(pra formatar automático ao salvar, baixe a extensão Ruff do VSCode)