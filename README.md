# Horas Adicionais

Sistema interno para lançamento e aprovação de horas adicionais/atividades de campo,
com fluxo de aprovação em duas etapas (**PMO → Gestão**).

> Este projeto foi reconstruído a partir do schema de banco encontrado em um export
> parcial do Manus.app. O export não trazia as telas nem o CSS originais, então o
> visual aqui é uma proposta nova (paleta petróleo/âmbar, tipografia IBM Plex),
> não uma cópia pixel-a-pixel do app original. Se você tiver screenshots do sistema
> antigo, me envie para eu ajustar o visual.

## Stack

- **Frontend**: React + Vite + TypeScript + Tailwind + shadcn/ui
- **Backend**: Node.js + Express + TypeScript + Drizzle ORM
- **Banco**: PostgreSQL
- **Auth**: JWT em cookie httpOnly + bcrypt
- **Deploy**: Docker + Docker Compose, pronto para stack no Portainer
- **CI**: GitHub Actions publicando imagens no GitHub Container Registry (GHCR)

## Papéis de usuário

| Grupo      | Pode fazer |
|------------|------------|
| `operacao` | Criar, editar e enviar atividades para aprovação |
| `pmo`      | Dar a 1ª aprovação; criar/editar projetos |
| `gestao`   | Dar a 2ª aprovação (após o PMO); gerenciar dias bloqueados |
| `admin`    | Tudo, incluindo gestão de usuários |

Fluxo de status da atividade: `pendente` → `aguardando_aprovacao` → (`aprovada` | `rejeitada`).

## Rodando localmente (sem Docker)

Pré-requisitos: Node 20+, PostgreSQL rodando localmente.

```bash
# Backend
cd server
cp .env.example .env      # edite DATABASE_URL e JWT_SECRET
npm install
npm run db:generate       # gera as migrations a partir do schema
npm run db:migrate        # aplica as migrations no banco
npm run db:seed           # cria o usuário admin inicial
npm run dev                # http://localhost:4000

# Frontend (em outro terminal)
cd client
npm install
npm run dev                # http://localhost:5173
```

Login inicial (definido no seed): `admin@empresa.com.br` / `admin123` — troque a senha
em produção via variáveis `SEED_ADMIN_EMAIL` / `SEED_ADMIN_PASSWORD`.

## Rodando com Docker Compose (local)

```bash
cp .env.example .env       # edite as senhas e o JWT_SECRET
docker compose up --build
```

O frontend fica em `http://localhost:8080` (proxying `/api` para o backend).

**Importante:** antes do primeiro uso, gere as migrations do Drizzle localmente
(`cd server && npm install && npm run db:generate`) e faça commit da pasta
`server/drizzle/` no repositório — é ela que o container do backend aplica ao subir.
Depois do primeiro `docker compose up`, rode o seed uma vez:

```bash
docker compose exec server node dist/seed.js
```

## Publicando no GitHub

```bash
git init
git add .
git commit -m "Sistema de horas adicionais"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/horas-adicionais.git
git push -u origin main
```

O workflow em `.github/workflows/docker-publish.yml` já está configurado para, a cada
push na `main`, buildar e publicar as imagens `ghcr.io/SEU-USUARIO/horas-adicionais-server`
e `...-client`. Não precisa configurar nada — ele usa o `GITHUB_TOKEN` automático do
Actions. Se o pacote GHCR ficar privado, torne-o público em
**GitHub → seu perfil → Packages** ou dê permissão ao Portainer para autenticar no GHCR.

## Deploy no Portainer

Duas formas, escolha uma:

### Opção A — Stack a partir do repositório Git (recomendado)

1. No Portainer: **Stacks → Add stack → Repository**.
2. Cole a URL do seu repositório GitHub e o caminho `docker-compose.yml` (raiz).
3. Em **Environment variables**, cole o conteúdo do `.env.example` já preenchido
   com valores reais (senhas, `JWT_SECRET`, etc).
4. Deploy. O Portainer vai clonar o repo e buildar as três imagens (`db`, `server`, `client`)
   direto no seu Docker host.
5. Ative o **webhook** da stack (Portainer gera uma URL) e configure-o no GitHub
   (`Settings → Webhooks` do repositório) para redeployar automaticamente a cada push.

### Opção B — Stack usando as imagens do GHCR (mais rápido, sem build no host)

Troque no `docker-compose.yml` os blocos `build:` por `image:` apontando para o GHCR, por exemplo:

```yaml
server:
  image: ghcr.io/SEU-USUARIO/horas-adicionais-server:latest
client:
  image: ghcr.io/SEU-USUARIO/horas-adicionais-client:latest
```

e cole esse compose diretamente em **Stacks → Add stack → Web editor** no Portainer.

## Estrutura do projeto

```
.
├── client/           # Frontend React + Vite
├── server/           # Backend Express + Drizzle
├── docker-compose.yml
└── .github/workflows/docker-publish.yml
```
