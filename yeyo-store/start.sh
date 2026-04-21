#!/bin/bash

# Script para iniciar YeYo Store (Backend + Frontend)
# Uso: bash start.sh

echo "🚀 Iniciando YeYo Store..."

# Colores para terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Obtener ruta actual
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$SCRIPT_DIR"

# Verificar si existen las carpetas
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
  echo "❌ Error: No se encontraron las carpetas backend o frontend"
  exit 1
fi

# Función para detener procesos al salir
cleanup() {
  echo ""
  echo "🛑 Deteniendo servicios..."
  kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
  exit 0
}

# Trap para capturar Ctrl+C
trap cleanup SIGINT SIGTERM

# Iniciar Backend
echo -e "${BLUE}📦 Iniciando Backend (FastAPI)...${NC}"
cd "$SCRIPT_DIR/backend"

# Activar venv si existe
if [ -d "venv" ]; then
  source venv/bin/activate 2>/dev/null || true
fi

uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
echo -e "${GREEN}✅ Backend iniciado (PID: $BACKEND_PID)${NC}"

sleep 2

# Iniciar Frontend
echo -e "${BLUE}⚛️  Iniciando Frontend (React + Vite)...${NC}"
cd "$SCRIPT_DIR/frontend"

# Instalar dependencias si no existen node_modules
if [ ! -d "node_modules" ]; then
  echo "📥 Instalando dependencias del frontend..."
  npm install
fi

npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}✅ Frontend iniciado (PID: $FRONTEND_PID)${NC}"

echo ""
echo -e "${GREEN}═════════════════════════════════════════${NC}"
echo -e "${GREEN}🎉 YeYo Store está corriendo!${NC}"
echo -e "${GREEN}═════════════════════════════════════════${NC}"
echo ""
echo "📱 Frontend:  http://localhost:3000"
echo "🔌 Backend:   http://localhost:8000"
echo "📚 API Docs:  http://localhost:8000/docs"
echo ""
echo "Presiona Ctrl+C para detener los servicios"
echo ""

# Esperar a que los procesos terminen
wait
