#!/bin/bash

# Script para ver logs

echo "📋 Logs do Sistema de Cadastro"
echo "=============================="
echo ""
echo "Escolha qual log deseja ver:"
echo "1) Todos os logs"
echo "2) Backend"
echo "3) PostgreSQL"
echo "4) Frontend"
echo "5) Sair"
echo ""

read -p "Opção: " opcao

case $opcao in
    1)
        docker-compose logs -f
        ;;
    2)
        docker-compose logs -f backend
        ;;
    3)
        docker-compose logs -f postgres
        ;;
    4)
        docker-compose logs -f frontend
        ;;
    5)
        echo "Saindo..."
        exit 0
        ;;
    *)
        echo "Opção inválida!"
        exit 1
        ;;
esac
