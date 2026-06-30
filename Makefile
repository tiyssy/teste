.PHONY: help build up down logs restart clean test db-shell

help:
	@echo "📋 Comandos disponíveis:"
	@echo ""
	@echo "  make build          - Construir containers"
	@echo "  make up             - Iniciar aplicação"
	@echo "  make down           - Parar aplicação"
	@echo "  make restart        - Reiniciar aplicação"
	@echo "  make logs           - Ver logs em tempo real"
	@echo "  make logs-backend   - Ver logs do backend"
	@echo "  make logs-db        - Ver logs do banco"
	@echo "  make logs-frontend  - Ver logs do frontend"
	@echo "  make clean          - Remover containers e volumes"
	@echo "  make db-shell       - Acessar shell do PostgreSQL"
	@echo "  make db-backup      - Fazer backup do banco"
	@echo "  make status         - Ver status dos containers"
	@echo "  make test-api       - Testar endpoints da API"
	@echo "  make dev            - Iniciar em modo desenvolvimento"
	@echo ""

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "✅ Aplicação iniciada!"
	@echo "   Frontend: http://localhost:3000"
	@echo "   Backend: http://localhost:8000"
	@echo "   Docs: http://localhost:8000/docs"

down:
	docker-compose down

restart:
	docker-compose restart
	@echo "✅ Aplicação reiniciada!"

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-db:
	docker-compose logs -f postgres

logs-frontend:
	docker-compose logs -f frontend

clean:
	docker-compose down -v
	@echo "✅ Limpeza concluída!"

db-shell:
	docker-compose exec postgres psql -U cadastro -d cadastro_db

db-backup:
	@mkdir -p backups
	@docker-compose exec postgres pg_dump -U cadastro cadastro_db > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup realizado!"

status:
	docker-compose ps

test-api:
	@echo "🧪 Testando API..."
	@echo ""
	@echo "1️⃣  Health Check"
	@curl -s http://localhost:8000/health | jq .
	@echo ""
	@echo "2️⃣  Listar Usuários"
	@curl -s http://localhost:8000/api/usuarios | jq . | head -20
	@echo ""
	@echo "✅ Testes concluídos!"

dev:
	docker-compose -f docker-compose.dev.yml up -d
	@echo "✅ Modo desenvolvimento ativado!"

dev-down:
	docker-compose -f docker-compose.dev.yml down
	@echo "✅ Modo desenvolvimento desativado!"
