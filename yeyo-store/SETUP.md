# 🚀 Guía de Instalación - YeYo Store

## Problema Encontrado

❌ El backend no estaba corriendo (error: `ERR_CONNECTION_REFUSED` en puerto 8000)
❌ Los archivos viejos del frontend (HTML vanilla) conflictaban con React

## ✅ Lo que hemos arreglado

✓ Eliminado `index.html`, `css/`, `js/` anteriores
✓ Creado nuevo `index.html` para React
✓ Creado `.env` en backend con configuración PostgreSQL
✓ Verificado que `vite.config.js` está correctamente configurado

---

## 📋 Requisitos del Sistema

- **PostgreSQL 13+** (instalado y corriendo)
- **Python 3.10+**
- **Node.js 16+** y npm

### Verificar Instalaciones

```powershell
# Verificar Python
python --version

# Verificar Node.js
node --version
npm --version

# Verificar PostgreSQL (desde PowerShell)
psql --version
```

---

## 🔧 Paso 1: Configurar Base de Datos PostgreSQL

### Windows - Opción A: Instalar desde cli

Si no tienes PostgreSQL instalado, descárgalo desde: https://www.postgresql.org/download/windows/

### Windows - Opción B: Usar WSL/Docker (Recomendado)

```bash
# Si usas Docker:
docker run --name postgres-yeyo -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=yeyo_store -p 5432:5432 -d postgres:15
```

### Crear Base de Datos

**Abrir PostgreSQL CLI:**

```powershell
psql -U postgres -h localhost
```

**Crear la base de datos:**

```sql
CREATE DATABASE yeyo_store;
\connect yeyo_store
```

**Salir:**

```sql
\q
```

---

## 🐍 Paso 2: Configurar Backend

```powershell
cd .\yeyo-store\backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

**Si tienes error de ejecución:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

---

## ⚛️ Paso 3: Configurar Frontend

```powershell
cd ..\frontend

# Instalar dependencias
npm install
```

---

## 🎯 Paso 4: Ejecutar Aplicación

### Opción A: Usar Script Automático (RECOMENDADO)

**Desde la carpeta raíz del proyecto:**

```powershell
.\start.bat
```

Esto abrirá 2 ventanas de terminal:
- Una para el backend (puerto 8000)
- Una para el frontend (puerto 3000)

### Opción B: Ejecutar Manualmente

**Terminal 1 - Backend:**

```powershell
cd .\yeyo-store\backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**

```powershell
cd .\yeyo-store\frontend
npm run dev
```

---

## ✨ ¡Éxito! Acceder a la Aplicación

| Componente | URL |
|-----------|-----|
| **Frontend** | http://localhost:3000 |
| **Backend API** | http://localhost:8000/api |
| **Swagger Docs** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |

---

## 🧪 Primera Prueba

1. Abre http://localhost:3000 en tu navegador
2. Ve a "Registrarse"
3. Crea una cuenta con email + contraseña
4. Login con tus credenciales
5. ¡Deberías ver tu email en la página de perfil!

---

## 🐛 Solución de Problemas

### Error: "Puerto 8000/3000 ya está en uso"

```powershell
# Encontrar y matar proceso en puerto
netstat -ano | findstr :8000
taskkill /PID <numero> /F
```

### Error: "No se puede conectar a PostgreSQL"

```
❌ PROBLEMA: "postgresql://postgres:postgres@localhost:5432/yeyo_store"
           se rechaza la conexión

✓ SOLUCIÓN:
1. Verifica que PostgreSQL esté corriendo
2. Verifica credenciales en backend/.env
3. Verifica que la BD "yeyo_store" existe
```

### Error: "ModuleNotFoundError"

```powershell
# Asegúrate de que venv está activado
.\venv\Scripts\Activate.ps1

# Reinstala dependencias
pip install --upgrade -r requirements.txt
```

### Error: "npm: command not found"

- Node.js podría no estar instalado
- Descárgalo desde: https://nodejs.org/

### Frontend muestra error 404 en favicon

✓ Esto es normal y no afecta la funcionalidad
- Podemos ignorarlo por ahora

---

## 📝 Variables de Entorno

### Backend (.env)

```env
# Base de Datos
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/yeyo_store

# JWT
SECRET_KEY=tu-clave-secreta-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000/api
```

---

## 🚀 Próximos Pasos

Una vez que todo esté corriendo:

1. **Registra un usuario de prueba**
   - Usa cualquier email válido
   - Contraseña de tu elección

2. **Prueba los endpoints en Swagger**
   - Ve a http://localhost:8000/docs
   - Click en cada endpoint y "Try it out"

3. **Integra las páginas del frontend**
   - Products.jsx necesita llamadas a API
   - Wishlist.jsx necesita estado global
   - Cart.jsx necesita carrito compartido

4. **Carga datos de prueba**
   - Crear algunos productos en la BD
   - Probar flujo de compra completo

---

## 💡 Comandos Útiles

```powershell
# Limpiar todo y empezar de nuevo
rm -r .\backend\venv
rm -r .\frontend\node_modules
# Luego vuelve a Paso 2

# Reestablecer BD
dropdb -U postgres yeyo_store
createdb -U postgres yeyo_store

# Ver logs del backend (si falla silenciosamente)
# Busca en la ventana del backend qué dice

# Matar todos los procesos Python (cuidado!)
taskkill /F /IM python.exe
```

---

## ✅ Checklist de Configuración

- [ ] PostgreSQL instalado y corriendo
- [ ] BD `yeyo_store` creada
- [ ] Backend venv activado
- [ ] Backend dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Backend `.env` configurado
- [ ] Frontend `npm install` ejecutado
- [ ] Frontend `.env` configurado (VITE_API_URL)
- [ ] `npm run dev` inicia React en puerto 3000
- [ ] `uvicorn main:app --reload` inicia backend en puerto 8000
- [ ] Frontend muestra UI sin errores de conexión

---

¿Alguna pregunta? Revisa la sección de Solución de Problemas arriba. 👆
