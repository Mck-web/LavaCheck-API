from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="LavaCheck API")

# Configuração de CORS para permitir requisições dos arquivos HTML locais
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class VeiculoIn(BaseModel):
    placa: str
    modelo: str
    cliente: str
    whatsapp: str
    avarias: Optional[str] = ""

class Veiculo(VeiculoIn):
    id: int
    status: str = "Aguardando"

# Banco de dados em memória para o projeto de extensão
patio_db = []
ticket_counter = 1

@app.post("/checkin")
def fazer_checkin(veiculo: VeiculoIn):
    global ticket_counter
    novo_veiculo = Veiculo(**veiculo.dict(), id=ticket_counter)
    patio_db.append(novo_veiculo)
    ticket_counter += 1
    return {"mensagem": "Sucesso", "ticket": novo_veiculo.id, "placa": novo_veiculo.placa}

@app.get("/patio", response_model=List[Veiculo])
def listar_patio():
    return patio_db

@app.delete("/checkout/{placa}")
def dar_baixa(placa: str):
    global patio_db
    veiculo = next((v for v in patio_db if v.placa == placa), None)
    if veiculo:
        patio_db = [v for v in patio_db if v.placa != placa]
        return {"mensagem": f"Veículo {placa} baixado. Cliente notificado no WhatsApp."}
    return {"erro": "Veículo não encontrado"}