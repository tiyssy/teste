# Sistema de Cadastro com Docker e PostgreSQL

Aplicação completa de cadastro de usuários com backend FastAPI, frontend HTML/CSS/JS e banco de dados PostgreSQL, totalmente containerizada com Docker.

## 📋 Características

- **Backend**: FastAPI com Python 3.11
- **Banco de Dados**: PostgreSQL 15
- **Frontend**: HTML5, CSS3 e JavaScript vanilla
- **Containerização**: Docker e Docker Compose
- **API RESTful**: Endpoints completos para CRUD
- **Autenticação**: Pronta para integração
- **Responsivo**: Interface adaptável para mobile

## 🚀 Pré-requisitos

- Docker (versão 20.10+)
- Docker Compose (versão 2.0+)
- Git (opcional)

## 📦 Estrutura do Projeto

```
cadastro-app/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py              # Aplicação FastAPI
│   ├── config.py            # Configurações
│   ├── database.py          # Conexão com BD
│   ├── models.py            # Modelos SQLAlchemy
│   └── schemas.py           # Schemas Pydantic
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── nginx.conf
│   └── index.html           # Interface web
├── database/
│   └── init.sql             # Script de inicialização
├── docker-compose.yml       # Orquestração de containers
├── .env                     # Variáveis de ambiente
├── .env.example             # Exemplo de .env
├── .gitignore
└── README.md
```

## 🔧 Instalação e Execução

### 1. Clonar ou Extrair o Projeto

```bash
# Se estiver em um arquivo compactado
unzip cadastro-app.zip
cd cadastro-app
```

### 2. Configurar Variáveis de Ambiente

O arquivo `.env` já está configurado com valores padrão:

```bash
# Opcional: Copiar do exemplo
cp .env.example .env
```

**Valores padrão:**
- DB_USER: `cadastro`
- DB_PASSWORD: `senha123`
- DB_NAME: `cadastro_db`
- DB_HOST: `postgres`
- DB_PORT: `5432`

### 3. Iniciar os Containers

```bash
# Construir e iniciar todos os serviços
docker-compose up -d

# Ou com rebuild
docker-compose up -d --build
```

### 4. Verificar Status

```bash
# Ver status dos containers
docker-compose ps

# Ver logs
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f backend
docker-compose logs -f postgres
docker-compose logs -f frontend
```

## 🌐 Acessar a Aplicação

Após iniciar os containers, acesse:

- **Frontend**: http://localhost:3000
- **API Backend**: http://localhost:8000
- **Documentação API**: http://localhost:8000/docs
- **Banco de Dados**: localhost:5432

## 📊 Banco de Dados

### Conectar ao PostgreSQL

```bash
# Usar psql
docker-compose exec postgres psql -U cadastro -d cadastro_db

# Ou via ferramenta GUI (DBeaver, pgAdmin, etc.)
# Host: localhost
# Port: 5432
# User: cadastro
# Password: senha123
# Database: cadastro_db
```

### Tabelas Criadas

#### usuarios
```sql
- id (PK)
- nome
- email (UNIQUE)
- telefone
- data_nascimento
- endereco
- cidade
- estado
- cep
- data_criacao
- data_atualizacao
```

#### logs
```sql
- id (PK)
- usuario_id (FK)
- acao
- descricao
- data_acao
```

## 🔌 Endpoints da API

### Usuários

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/usuarios` | Listar todos os usuários |
| GET | `/api/usuarios/{id}` | Obter detalhes de um usuário |
| POST | `/api/usuarios` | Criar novo usuário |
| PUT | `/api/usuarios/{id}` | Atualizar usuário |
| DELETE | `/api/usuarios/{id}` | Deletar usuário |
| GET | `/api/usuarios/{id}/logs` | Obter histórico de um usuário |

### Busca

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/usuarios/search/por-email?email=...` | Buscar por email |
| GET | `/api/usuarios/search/por-nome?nome=...` | Buscar por nome |

### Health

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Status da API |
| GET | `/health` | Health check |

## 📝 Exemplos de Uso

### Criar Usuário

```bash
curl -X POST http://localhost:8000/api/usuarios \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@example.com",
    "telefone": "(11) 98765-4321",
    "data_nascimento": "1990-05-15",
    "endereco": "Rua A, 123",
    "cidade": "São Paulo",
    "estado": "SP",
    "cep": "01310-100"
  }'
```

### Listar Usuários

```bash
curl http://localhost:8000/api/usuarios
```

### Buscar por Email

```bash
curl http://localhost:8000/api/usuarios/search/por-email?email=joao@example.com
```

### Atualizar Usuário

```bash
curl -X PUT http://localhost:8000/api/usuarios/1 \
  -H "Content-Type: application/json" \
  -d '{
    "telefone": "(11) 99999-9999"
  }'
```

### Deletar Usuário

```bash
curl -X DELETE http://localhost:8000/api/usuarios/1
```

## 🛑 Parar os Containers

```bash
# Parar todos os serviços
docker-compose down

# Parar e remover volumes (cuidado: deleta dados!)
docker-compose down -v

# Parar apenas um serviço
docker-compose stop backend
```

## 🔄 Reiniciar Serviços

```bash
# Reiniciar todos
docker-compose restart

# Reiniciar um específico
docker-compose restart backend
```

## 🐛 Troubleshooting

### Erro: "Connection refused"

```bash
# Verificar se os containers estão rodando
docker-compose ps

# Verificar logs
docker-compose logs postgres
docker-compose logs backend
```

### Erro: "Port already in use"

```bash
# Mudar as portas no docker-compose.yml
# Ou parar o serviço que está usando a porta

# Encontrar qual processo está usando a porta
lsof -i :3000
lsof -i :8000
lsof -i :5432

# Matar o processo
kill -9 <PID>
```

### Banco de dados não conecta

```bash
# Verificar se o PostgreSQL está saudável
docker-compose exec postgres pg_isready -U cadastro

# Ver logs do PostgreSQL
docker-compose logs postgres

# Reiniciar o PostgreSQL
docker-compose restart postgres
```

### Frontend não carrega a API

```bash
# Verificar se o backend está rodando
docker-compose logs backend

# Testar conexão com a API
curl http://localhost:8000/health

# Verificar configuração do nginx
docker-compose exec frontend cat /etc/nginx/conf.d/default.conf
```

## 📈 Monitoramento

### Ver uso de recursos

```bash
docker stats
```

### Ver logs em tempo real

```bash
docker-compose logs -f
```

### Acessar shell de um container

```bash
# Backend
docker-compose exec backend bash

# PostgreSQL
docker-compose exec postgres bash

# Frontend
docker-compose exec frontend sh
```

## 🔐 Segurança

### Alterar Senha do Banco

1. Editar `.env`:
```bash
DB_PASSWORD=sua_senha_segura
```

2. Remover volume antigo:
```bash
docker-compose down -v
```

3. Reiniciar:
```bash
docker-compose up -d
```

### Variáveis de Ambiente em Produção

```bash
# Criar arquivo .env.production
DB_USER=usuario_seguro
DB_PASSWORD=senha_muito_segura_123!@#
DB_NAME=cadastro_prod
DEBUG=false
ENVIRONMENT=production
```

## 🚀 Deploy em Produção

### Usando Portainer

1. Acesse Portainer
2. Vá para Stacks
3. Clique em "Add Stack"
4. Cole o conteúdo do `docker-compose.yml`
5. Configure as variáveis de ambiente
6. Deploy

### Usando Docker Swarm

```bash
docker stack deploy -c docker-compose.yml cadastro
```

### Usando Kubernetes

```bash
# Converter para Kubernetes
kompose convert -f docker-compose.yml

# Deploy
kubectl apply -f .
```

## 📚 Documentação Adicional

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Docker Compose Docs](https://docs.docker.com/compose/)

## 💡 Próximos Passos

- [ ] Adicionar autenticação JWT
- [ ] Implementar paginação avançada
- [ ] Adicionar filtros e ordenação
- [ ] Criar testes automatizados
- [ ] Implementar cache com Redis
- [ ] Adicionar validações mais robustas
- [ ] Criar dashboard de analytics
- [ ] Implementar backup automático

## 📄 Licença

Este projeto é fornecido como está, livre para uso e modificação.

## 🤝 Suporte

Para dúvidas ou problemas:

1. Verificar os logs: `docker-compose logs -f`
2. Consultar a documentação da API: http://localhost:8000/docs
3. Revisar este README

## ✨ Melhorias Futuras

- Autenticação e autorização
- Rate limiting
- Caching
- Testes unitários e de integração
- CI/CD pipeline
- Monitoring com Prometheus
- Logging centralizado com ELK

---

**Versão**: 1.0.0  
**Última atualização**: 2024  
**Desenvolvido com ❤️**
