from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional, List

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: Optional[str] = None
    data_nascimento: Optional[date] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    data_nascimento: Optional[date] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id: int
    data_criacao: datetime
    data_atualizacao: datetime
    
    class Config:
        from_attributes = True

class LogResponse(BaseModel):
    id: int
    usuario_id: int
    acao: str
    descricao: Optional[str] = None
    data_acao: datetime
    
    class Config:
        from_attributes = True

class UsuarioDetailResponse(UsuarioResponse):
    logs: List[LogResponse] = []
