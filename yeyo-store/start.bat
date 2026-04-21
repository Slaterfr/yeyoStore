@echo off
REM Script para iniciar YeYo Store (Backend + Frontend) en Windows
REM Uso: start.bat

echo.
echo ============================================
echo  🚀 Iniciando YeYo Store...
echo ============================================
echo.

REM Obtener ruta actual
cd /d %~dp0

REM Verificar si existen las carpetas
if not exist "backend" (
  echo ❌ Error: No se encontró la carpeta 'backend'
  pause
  exit /b 1
)

if not exist "frontend" (
  echo ❌ Error: No se encontró la carpeta 'frontend'
  pause
  exit /b 1
)

REM Verificar si existe backend .env
if not exist "backend\.env" (
  echo ❌ Advertencia: backend\.env no existe
  echo.
  echo 📝 Creando archivo .env con valores por defecto...
  REM El .env debería haber sido creado ya, pero si falta:
  echo DATABASE_URL=postgresql://postgres:postgres@localhost:5432/yeyo_store > backend\.env
  echo SQLALCHEMY_ECHO=False >> backend\.env
  echo SECRET_KEY=your-super-secret-key-12345 >> backend\.env
)


REM Iniciar Backend en una nueva ventana
echo 📦 Iniciando Backend (FastAPI en puerto 8000)...
echo    Sistema: PostgreSQL requiere estar corriendo en localhost:5432
echo.
start "YeYo Store - Backend" cmd /k "cd backend && call venv\Scripts\Activate.bat && python -m uvicorn main:app --reload --port 8000"

REM Esperar un poco para que el backend inicie
timeout /t 4 /nobreak

REM Instalar dependencias del frontend si no existen
if not exist "frontend\node_modules" (
  echo.
  echo 📥 Instalando dependencias del frontend...
  cd frontend
  call npm install
  cd ..
  echo     ✓ Instalación completada
)

REM Iniciar Frontend en una nueva ventana
echo.
echo ⚛️  Iniciando Frontend (React + Vite en puerto 3000)...
start "YeYo Store - Frontend" cmd /k "cd frontend && npm run dev"

REM Esperar para mostrar el mensaje
timeout /t 3 /nobreak

echo.
echo ============================================
echo 🎉 YeYo Store está iniciando!
echo ============================================
echo.
echo 📱 Frontend:  http://localhost:3000
echo 🔌 Backend:   http://localhost:8000
echo 📚 API Docs:  http://localhost:8000/docs
echo.
echo ⚠️  REQUISITOS:
echo    - PostgreSQL corriendo en localhost:5432
echo    - Base de datos 'yeyo_store' creada
echo    - Usuario: postgres / Contraseña: postgres
echo.
echo 📖 Para más ayuda, consulta SETUP.md
echo.
echo Cierra las ventanas de terminal para detener los servicios.
echo.
pause
