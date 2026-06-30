from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    telefone = Column(String(20), nullable=True)
    data_nascimento = Column(Date, nullable=True)
    endereco = Column(String(500), nullable=True)
    cidade = Column(String(100), nullable=True)
    estado = Column(String(2), nullable=True)
    cep = Column(String(10), nullable=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    logs = relationship("Log", back_populates="usuario", cascade="all, delete-orphan")

class Log(Base):
    __tablename__ = "logs"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    acao = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=True)
    data_acao = Column(DateTime, default=datetime.utcnow)
    
    usuario = relationship("Usuario", back_populates="logs")
