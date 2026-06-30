# 🧪 Guia de Teste Rápido

Este guia mostra como testar a aplicação após iniciar com Docker.

## ✅ Checklist de Inicialização

### 1. Iniciar a Aplicação

```bash
cd cadastro-app
docker-compose up -d
```

### 2. Aguardar Inicialização

```bash
# Verificar status
docker-compose ps

# Aguardar ~10-15 segundos para o banco de dados estar pronto
sleep 15
```

### 3. Verificar Saúde dos Serviços

```bash
# Health check do backend
curl http://localhost:8000/health

# Resposta esperada:
# {"status":"ok"}
```

## 🧪 Testes Funcionais

### Teste 1: Verificar API

```bash
# Acessar documentação interativa
# Abrir no navegador: http://localhost:8000/docs
```

### Teste 2: Listar Usuários Iniciais

```bash
curl http://localhost:8000/api/usuarios

# Resposta esperada: Array com 3 usuários de exemplo
```

### Teste 3: Criar Novo Usuário

```bash
curl -X POST http://localhost:8000/api/usuarios \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Teste Silva",
    "email": "teste@example.com",
    "telefone": "(11) 91234-5678",
    "data_nascimento": "1995-03-20",
    "endereco": "Rua Teste, 999",
    "cidade": "São Paulo",
    "estado": "SP",
    "cep": "01310-100"
  }'

# Resposta esperada: Usuário criado com ID
```

### Teste 4: Buscar por Email

```bash
curl "http://localhost:8000/api/usuarios/search/por-email?email=teste@example.com"

# Resposta esperada: Usuário encontrado
```

### Teste 5: Buscar por Nome

```bash
curl "http://localhost:8000/api/usuarios/search/por-nome?nome=Teste"

# Resposta esperada: Usuários com "Teste" no nome
```

### Teste 6: Acessar Frontend

```bash
# Abrir no navegador: http://localhost:3000
# Você deve ver:
# - Formulário de cadastro à esquerda
# - Lista de usuários à direita
# - Tabela com usuários de exemplo
```

### Teste 7: Testar CRUD no Frontend

1. **Listar**: A página carrega automaticamente os usuários
2. **Criar**: Preencha o formulário e clique em "Cadastrar Usuário"
3. **Buscar**: Use a caixa de busca para filtrar por nome
4. **Ver Detalhes**: Clique em "Ver" para abrir modal com informações completas
5. **Editar**: Clique em "Editar" para modificar dados
6. **Deletar**: Clique em "Deletar" para remover um usuário

### Teste 8: Verificar Banco de Dados

```bash
# Conectar ao PostgreSQL
docker-compose exec postgres psql -U cadastro -d cadastro_db

# Dentro do psql:
\dt                              # Listar tabelas
SELECT * FROM usuarios;          # Ver usuários
SELECT * FROM logs;              # Ver logs de atividades
\q                               # Sair
```

### Teste 9: Verificar Logs

```bash
# Ver todos os logs
docker-compose logs

# Ver logs do backend
docker-compose logs backend

# Ver logs do PostgreSQL
docker-compose logs postgres

# Ver logs em tempo real
docker-compose logs -f
```

## 📊 Dados de Teste Pré-carregados

A aplicação vem com 3 usuários de exemplo:

1. **João Silva**
   - Email: joao@example.com
   - Telefone: (11) 98765-4321
   - Cidade: São Paulo, SP

2. **Maria Santos**
   - Email: maria@example.com
   - Telefone: (21) 99876-5432
   - Cidade: Rio de Janeiro, RJ

3. **Pedro Oliveira**
   - Email: pedro@example.com
   - Telefone: (31) 97654-3210
   - Cidade: Belo Horizonte, MG

## 🔍 Troubleshooting Rápido

### Erro: "Connection refused" na porta 3000

```bash
# Verificar se o frontend está rodando
docker-compose ps frontend

# Ver logs do frontend
docker-compose logs frontend

# Reiniciar frontend
docker-compose restart frontend
```

### Erro: "Connection refused" na porta 8000

```bash
# Verificar se o backend está rodando
docker-compose ps backend

# Ver logs do backend
docker-compose logs backend

# Reiniciar backend
docker-compose restart backend
```

### Erro: "Connection refused" na porta 5432

```bash
# Verificar se o PostgreSQL está rodando
docker-compose ps postgres

# Ver logs do PostgreSQL
docker-compose logs postgres

# Verificar se o banco está saudável
docker-compose exec postgres pg_isready -U cadastro
```

### Erro: "Email já cadastrado"

Isso é esperado! Tente criar um usuário com um email diferente.

### Erro: "Usuário não encontrado"

Verifique se o ID do usuário existe. Use GET `/api/usuarios` para listar todos.

## 🚀 Performance

### Teste de Carga Simples

```bash
# Criar 100 usuários de teste
for i in {1..100}; do
  curl -X POST http://localhost:8000/api/usuarios \
    -H "Content-Type: application/json" \
    -d "{
      \"nome\": \"Usuário $i\",
      \"email\": \"usuario$i@example.com\",
      \"cidade\": \"Cidade $i\",
      \"estado\": \"SP\"
    }"
done
```

### Monitorar Recursos

```bash
# Ver uso de CPU e memória
docker stats

# Pressione Ctrl+C para sair
```

## 📈 Verificar Crescimento do Banco

```bash
# Contar usuários
curl http://localhost:8000/api/usuarios | jq 'length'

# Contar logs
docker-compose exec postgres psql -U cadastro -d cadastro_db -c "SELECT COUNT(*) FROM logs;"
```

## 🔐 Teste de Segurança Básica

### Validação de Email

```bash
# Tentar criar com email inválido
curl -X POST http://localhost:8000/api/usuarios \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Teste",
    "email": "email_invalido"
  }'

# Deve retornar erro 422 (Unprocessable Entity)
```

### Validação de Campos Obrigatórios

```bash
# Tentar criar sem nome
curl -X POST http://localhost:8000/api/usuarios \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@example.com"
  }'

# Deve retornar erro 422
```

## 📝 Notas Importantes

- Os dados são persistidos no volume Docker `postgres_data`
- Ao fazer `docker-compose down -v`, todos os dados são deletados
- O arquivo `.env` contém as credenciais do banco
- Não compartilhe o `.env` em repositórios públicos
- A API está documentada em http://localhost:8000/docs

## ✨ Próximos Passos

Após confirmar que tudo funciona:

1. Customize o banco de dados conforme necessário
2. Adicione mais campos aos usuários
3. Implemente autenticação
4. Configure HTTPS
5. Deploy em produção

---

**Dúvidas?** Consulte o README.md para mais informações!
