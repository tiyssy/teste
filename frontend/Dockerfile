FROM node:20-alpine as builder

WORKDIR /app

# Copiar arquivos necessários
COPY package*.json ./
RUN npm install

COPY . .

# Build da aplicação (se necessário)
# RUN npm run build

# Usar nginx para servir
FROM nginx:alpine

# Copiar configuração do nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar arquivos estáticos
COPY --from=builder /app /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
