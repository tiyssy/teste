#!/bin/bash

# Script para iniciar a aplicação

set -e

echo "🚀 Iniciando Sistema de Cadastro..."
echo "=================================="

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado!"
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado!"
    exit 1
fi

# Criar arquivo .env se não existir
if [ ! -f .env ]; then
    echo "📝 Criando arquivo .env..."
    cp .env.example .env
fi

# Build e start
echo "📦 Construindo containers..."
docker-compose build

echo "🔄 Iniciando serviços..."
docker-compose up -d

# Aguardar o banco de dados estar pronto
echo "⏳ Aguardando banco de dados..."
sleep 5

# Verificar status
echo ""
echo "✅ Aplicação iniciada com sucesso!"
echo ""
echo "📍 Acesse:"
echo "   Frontend: http://localhost:3000"
echo "   API: http://localhost:8000"
echo "   Docs: http://localhost:8000/docs"
echo ""
echo "📊 Banco de dados:"
echo "   Host: localhost"
echo "   Port: 5432"
echo "   User: cadastro"
echo "   Password: senha123"
echo ""
echo "💡 Comandos úteis:"
echo "   Ver logs: docker-compose logs -f"
echo "   Parar: docker-compose down"
echo "   Status: docker-compose ps"
echo ""
