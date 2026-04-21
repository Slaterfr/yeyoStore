# 🚀 YeYo Store - Deployment Guide

## 📋 Pre-requisitos

- Git
- Docker & Docker Compose
- Supabase account (para database en producción)
- Render account (para hosting)

---

## 🐳 Desarrollo Local con Docker

### 1. Preparar variables de entorno

```bash
# Copia el archivo de ejemplo
cp .env.example .env.docker

# Edita .env.docker con tus valores locales (opcional, tiene defaults)
```

### 2. Levantar los servicios

```bash
docker-compose up -d

# Verifica que todo está corriendo
docker-compose ps

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

### 3. Acceder a la aplicación

- **Frontend**: http://localhost
- **Backend**: http://localhost:8000
- **Backend Docs**: http://localhost:8000/docs
- **Database**: `localhost:5432` (PostgreSQL local para desarrollo)

### 4. Ver logs individuales

```bash
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres
```

---

## 🌐 Deployment a Render

### 1. Preparar repositorio Git

```bash
# Inicializar repositorio (si no está)
git init

# Agregar todos los archivos
git add .

# Commit inicial
git commit -m "Initial commit: YeYo Store with Docker"

# Agregar remote (reemplazar URL)
git remote add origin https://github.com/tu-usuario/yeyo-store.git

# Push a main branch
git branch -M main
git push -u origin main
```

### 2. Crear servicios en Render

**Backend:**
- Ir a https://render.com/dashboard
- New → Web Service
- Conectar repositorio GitHub
- Root Directory: `backend/`
- Build Command: (vacío - Docker lo maneja)
- Start Command: (vacío - Docker lo define)
- Environment: Add variables desde `.env.example`:
  - `DATABASE_URL`: Tu URL de Supabase PostgreSQL
  - `SECRET_KEY`: Generar secreta nueva para producción
  - `ALGORITHM`: `HS256`
  - `ALLOWED_ORIGINS`: `https://yourdomain.com`
  - `ENVIRONMENT`: `production`
  - `DEBUG`: `false`

**Frontend:**
- New → Web Service
- Conectar repositorio GitHub
- Root Directory: `frontend/`
- Environment variables:
  - `VITE_API_URL`: `https://backend-service.onrender.com`

### 3. Variables de entorno en Render

#### Backend requiere:
```env
DATABASE_URL=postgresql://user:pass@db.supabase.co:5432/postgres
SECRET_KEY=your-production-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=production
DEBUG=false
ALLOWED_ORIGINS=https://frontend-domain.onrender.com,https://yourdomain.com
```

#### Frontend requiere:
```env
VITE_API_URL=https://backend-service.onrender.com
VITE_APP_NAME=YeYo Store
```

### 4. Conectar Supabase

1. En Supabase, obtener URL de conexión:
   - Dashboard → Project Settings → Database
   - URI: `postgresql://[user]:[password]@[host]:[port]/[database]`

2. Copiar URL completa a `DATABASE_URL` en Render Backend

---

## 📦 Estructura del Proyecto

```
yeyo-store/
├── backend/
│   ├── Dockerfile              # Build FastAPI
│   ├── .dockerignore           # Excluye archivos del build
│   ├── main.py                 # Punto de entrada
│   ├── config.py               # Configuración
│   ├── requirements.txt         # Dependencias Python
│   └── ...
├── frontend/
│   ├── Dockerfile              # Build React + Nginx
│   ├── .dockerignore           # Excluye archivos del build
│   ├── nginx.conf              # Configuración Nginx SPA
│   ├── package.json            # Dependencias Node
│   ├── src/                    # Código React
│   └── ...
├── docker-compose.yml          # Orquestación local
├── .env.example                # Variables de ejemplo
└── README.md                   # Este archivo
```

---

## 🔄 Flujo de Deployment

### Desarrollo Local
```bash
docker-compose up -d
# Editar código
# Los cambios se aplican en caliente (con --reload)
docker-compose down
```

### Producción (Render)
```bash
# Hacer cambios localmente
git add .
git commit -m "Descripción del cambio"
git push origin main

# Render automáticamente:
# 1. Detecta los Dockerfiles
# 2. Construye las imágenes
# 3. Levanta los servicios
# 4. Expone URLs públicas
```

---

## 🛠️ Troubleshooting

### Backend no conecta a la BD
- Verificar `DATABASE_URL` está correcta en variables de entorno
- Verificar que PostgreSQL está corriendo
- Ver logs: `docker-compose logs postgres`

### Frontend muestra "Cannot GET /"
- Verificar Nginx está sirviendo correctamente
- Ver logs: `docker-compose logs frontend`
- Revisar nginx.conf está copiado al contenedor

### Build falla en Render
- Verificar Dockerfile tiene sintaxis correcta
- Revisar .dockerignore no excluye archivos necesarios
- Ver logs de build en Render dashboard

### CORS errors
- Verificar `ALLOWED_ORIGINS` incluye dominio del frontend
- En desarrollo: `http://localhost:80`
- En producción: `https://yourdomain.com`

---

## ✅ Checklist Pre-Production

- [ ] `.env` local nunca está en git (verificar .gitignore)
- [ ] `.env.example` tiene estructura pero sin valores sensibles
- [ ] Dockerfile ambos servicios tienen HEALTHCHECK
- [ ] Docker-compose.yml usa variables de entorno
- [ ] nginx.conf sirve SPA correctamente (try_files)
- [ ] SECRET_KEY es única y fuerte en producción
- [ ] DATABASE_URL apunta a Supabase real
- [ ] CORS configurado con dominio correcto
- [ ] Imágenes Docker optimizadas (multi-stage builds)
- [ ] Health checks configurados en Render

---

## 📚 Recursos Útiles

- [Render Docs](https://render.com/docs)
- [Docker Docs](https://docs.docker.com/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Nginx SPA Config](https://spa-github-pages.rafrex.com/)

---

## 🚀 Quick Commands

```bash
# Inicializar git
git init && git add . && git commit -m "Initial"

# Ver contenedores
docker-compose ps

# Ingresar a contenedor
docker-compose exec backend bash
docker-compose exec frontend sh

# Borrar todo
docker-compose down -v

# Rebuild
docker-compose up -d --build

# Push a production
git push origin main
```

¡Listo para deployar! 🎉
