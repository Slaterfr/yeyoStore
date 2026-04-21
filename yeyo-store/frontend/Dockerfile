# =====================================================================
# Dockerfile - Frontend YeYo Store (React + Vite)
# =====================================================================
# Multi-stage build
# Stage 1: Build
FROM node:20-alpine as builder

WORKDIR /app

# Copiar archivos de dependencias
COPY package.json package-lock.json ./

# Instalar dependencias
RUN npm ci

# Copiar código
COPY . .

# Build
RUN npm run build

# =====================================================================
# Stage 2: Serve (Nginx)
# =====================================================================
FROM nginx:alpine

# Copiar configuración Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Copiar build desde builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Crear directorio de caché
RUN mkdir -p /var/cache/nginx

# Port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/health || exit 1

# Run Nginx
CMD ["nginx", "-g", "daemon off;"]
