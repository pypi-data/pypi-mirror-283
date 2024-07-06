from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class RpaHistoricoStatusEnum(str, Enum):
    Bloqueado = "A"
    Deletado = "B"
    Descartado = "C"
    DocumentoPublicoGerado = "D"
    DocumentoNaoPublico = "E"
    EmAndamento = "F"
    Falha = "G"
    Incompleto = "H"
    NaoProcesso = "I"
    Pendencia = "J"
    Processando = "K"
    Rejeitado = "L"
    Sucesso = "M"


class RpaHistoricoDTO(BaseModel):
    uuidHistorico: Optional[str] = Field(None, alias="uuidHistorico")
    uuidProcesso: str = Field(..., alias="uuidProcesso")
    uuidRobo: Optional[str] = Field(None, alias="uuidRobo")
    prioridade: int
    desStatus: RpaHistoricoStatusEnum = Field(..., alias="desStatus")
    configEntrada: Optional[dict] = Field(None, alias="configEntrada")
    retorno: Optional[dict] = Field(None, alias="retorno")
    datEntradaFila: Optional[datetime] = Field(None, alias="datEntradaFila")
    datInicioExecucao: Optional[datetime] = Field(None, alias="datInicioExecucao")
    datFimExecucao: Optional[datetime] = Field(None, alias="datFimExecucao")
    identificador: Optional[str] = Field(None, alias="identificador")

    class Config:
        populate_by_name = True
