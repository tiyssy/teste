from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from typing import List

from database import get_db, engine
from models import Base, Usuario, Log
from schemas import (
    UsuarioCreate, UsuarioUpdate, UsuarioResponse, 
    UsuarioDetailResponse, LogResponse
)
from config import settings

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Inicializar FastAPI
app = FastAPI(
    title="API de Cadastro",
    description="API para gerenciar cadastro de usuários",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== ROTAS ====================

@app.get("/", tags=["Health"])
async def root():
    """Verificar se a API está funcionando"""
    return {
        "message": "API de Cadastro funcionando!",
        "version": "1.0.0",
        "environment": settings.environment
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check da aplicação"""
    return {"status": "ok"}

# ==================== USUARIOS ====================

@app.get("/api/usuarios", response_model=List[UsuarioResponse], tags=["Usuários"])
async def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todos os usuários com paginação"""
    usuarios = db.query(Usuario).offset(skip).limit(limit).all()
    return usuarios

@app.get("/api/usuarios/{usuario_id}", response_model=UsuarioDetailResponse, tags=["Usuários"])
async def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obter detalhes de um usuário específico"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return usuario

@app.post("/api/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, tags=["Usuários"])
async def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Criar um novo usuário"""
    # Verificar se email já existe
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    novo_usuario = Usuario(**usuario.dict())
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    # Registrar log
    log = Log(
        usuario_id=novo_usuario.id,
        acao="CRIACAO",
        descricao=f"Usuário {novo_usuario.nome} criado"
    )
    db.add(log)
    db.commit()
    
    return novo_usuario

@app.put("/api/usuarios/{usuario_id}", response_model=UsuarioResponse, tags=["Usuários"])
async def atualizar_usuario(usuario_id: int, usuario_update: UsuarioUpdate, db: Session = Depends(get_db)):
    """Atualizar dados de um usuário"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Atualizar apenas os campos fornecidos
    dados_atualizacao = usuario_update.dict(exclude_unset=True)
    for campo, valor in dados_atualizacao.items():
        setattr(usuario, campo, valor)
    
    usuario.data_atualizacao = datetime.utcnow()
    db.commit()
    db.refresh(usuario)
    
    # Registrar log
    log = Log(
        usuario_id=usuario.id,
        acao="ATUALIZACAO",
        descricao=f"Usuário {usuario.nome} atualizado"
    )
    db.add(log)
    db.commit()
    
    return usuario

@app.delete("/api/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Usuários"])
async def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Deletar um usuário"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    nome_usuario = usuario.nome
    db.delete(usuario)
    db.commit()
    
    return None

@app.get("/api/usuarios/{usuario_id}/logs", response_model=List[LogResponse], tags=["Logs"])
async def obter_logs_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obter histórico de logs de um usuário"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    logs = db.query(Log).filter(Log.usuario_id == usuario_id).order_by(desc(Log.data_acao)).all()
    return logs

# ==================== BUSCA ====================

@app.get("/api/usuarios/search/por-email", response_model=UsuarioResponse, tags=["Busca"])
async def buscar_por_email(email: str, db: Session = Depends(get_db)):
    """Buscar usuário por email"""
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return usuario

@app.get("/api/usuarios/search/por-nome", response_model=List[UsuarioResponse], tags=["Busca"])
async def buscar_por_nome(nome: str, db: Session = Depends(get_db)):
    """Buscar usuários por nome (parcial)"""
    usuarios = db.query(Usuario).filter(Usuario.nome.ilike(f"%{nome}%")).all()
    return usuarios

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
