# Backend - ParkingAlot
 
REST API em Flask + SQLAlchemy para controle de estacionamento.
 
## Requirements
 
- Python 3.12+
- Docker (opcional)

## Setup
 
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
 
## Environment variables
 
`.env` na pasta `backend/`:
 
```
DATABASE_URL=sqlite:///parkingalot.db
FLASK_ENV=development
```
 
## Run
 
```bash
python run.py
```
 
Server: `http://127.0.0.1:5000`
 
## Run with Docker
 
```bash
docker compose up --build
```
 
Server: `http://localhost:5000`
 
Stop:
 
```bash
docker compose down
```