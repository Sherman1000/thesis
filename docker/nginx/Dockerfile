# Stage 1: build React static files
# Node 16: soporta lockfileVersion 3 del package-lock.json
# NODE_OPTIONS: webpack 4 (react-scripts 4) con Node 17+ requiere openssl-legacy-provider
FROM node:16-alpine AS build

WORKDIR /app/frontend

COPY ./frontend/package.json ./
COPY ./frontend/package-lock.json ./
RUN npm ci --legacy-peer-deps

COPY ./frontend/ ./
# Node 16 no necesita openssl-legacy-provider; evitamos el script de package.json que lo usa (para Node 22 local)
RUN npx react-scripts build

# Stage 2: servir con nginx
FROM nginx:stable-alpine
COPY --from=build /app/frontend/build /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]