# Backend - ParkingAlot
 
REST API em Flask + SQLAlchemy para controle de estacionamento.
 
## Requirements
 
- Python 3.12+

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
```
 
## Run
 
```bash
python run.py
```
 
Server: `http://127.0.0.1:5000`