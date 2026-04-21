# Script PowerShell para iniciar YeYo Store
# Uso: .\start.ps1

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host " 🚀 Iniciando YeYo Store..." -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si existen las carpetas necesarias
if (-not (Test-Path "backend")) {
    Write-Host "❌ Error: No se encontró la carpeta 'backend'" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

if (-not (Test-Path "frontend")) {
    Write-Host "❌ Error: No se encontró la carpeta 'frontend'" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar y crear .env si es necesario
if (-not (Test-Path "backend\.env")) {
    Write-Host "⚠️  backend\.env no encontrado, crear uno..." -ForegroundColor Yellow
    @"
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/yeyo_store
SQLALCHEMY_ECHO=False
SECRET_KEY=your-super-secret-key-12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
APP_NAME=YeYo Store API
APP_VERSION=1.0.0
DEBUG=True
ENVIRONMENT=development
"@ | Out-File "backend\.env" -Encoding UTF8
    Write-Host "✓ Archivo .env creado" -ForegroundColor Green
}

# Verificar venv
if (-not (Test-Path "backend\venv")) {
    Write-Host "❌ Entorno virtual de Python no encontrado" -ForegroundColor Red
    Write-Host ""
    Write-Host "👉 Por favor ejecuta primero:" -ForegroundColor Yellow
    Write-Host "   cd backend" -ForegroundColor Cyan
    Write-Host "   python -m venv venv" -ForegroundColor Cyan
    Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
    Write-Host "   pip install -r requirements.txt" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Iniciar Backend
Write-Host ""
Write-Host "📦 Iniciando Backend (FastAPI en puerto 8000)..." -ForegroundColor Green
Write-Host "   Asegúrate de que PostgreSQL está corriendo en localhost:5432" -ForegroundColor Yellow
Write-Host ""

Start-Process powershell {
    cd backend
    .\venv\Scripts\Activate.ps1
    python -m uvicorn main:app --reload --port 8000
} -NoNewWindow

# Esperar a que el backend inicie
Write-Host "⏳ Esperando a que Backend inicie..." -ForegroundColor Gray
Start-Sleep -Seconds 4

# Instalar dependencias del frontend si es necesario
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host ""
    Write-Host "📥 Instalando dependencias de Frontend..." -ForegroundColor Green
    Push-Location frontend
    npm install
    Pop-Location
    Write-Host "✓ Dependencias instaladas" -ForegroundColor Green
}

# Iniciar Frontend
Write-Host ""
Write-Host "⚛️  Iniciando Frontend (React + Vite en puerto 3000)..." -ForegroundColor Green
Write-Host ""

Start-Process powershell {
    cd frontend
    npm run dev
} -NoNewWindow

# Esperar un poco
Start-Sleep -Seconds 2

# Mostrar información
Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host " 🎉 YeYo Store está iniciando!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "📱 Frontend:  " -NoNewline; Write-Host "http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔌 Backend:   " -NoNewline; Write-Host "http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Docs:  " -NoNewline; Write-Host "http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  REQUISITOS:" -ForegroundColor Yellow
Write-Host "   - PostgreSQL corriendo en localhost:5432"
Write-Host "   - Base de datos 'yeyo_store' creada"
Write-Host "   - Usuario: postgres / Contraseña: postgres"
Write-Host ""
Write-Host "📖 Para más ayuda, consulta SETUP.md" -ForegroundColor Yellow
Write-Host ""
Write-Host "Cierra las ventanas de PowerShell para detener los servicios." -ForegroundColor Gray
Write-Host ""

Read-Host "Presiona Enter para salir"
