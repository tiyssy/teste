#!/bin/bash

# Script para parar a aplicação

echo "🛑 Parando Sistema de Cadastro..."
echo "=================================="

docker-compose down

echo "✅ Aplicação parada com sucesso!"
echo ""
echo "💡 Para remover volumes (dados): docker-compose down -v"
