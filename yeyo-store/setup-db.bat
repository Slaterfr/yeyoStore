@echo off
REM Script para verificar y configurar PostgreSQL para YeYo Store
REM Este script ayuda a crear la base de datos necesaria

echo.
echo ============================================
echo  🗄️  Configurar PostgreSQL para YeYo Store
echo ============================================
echo.

REM Verificar si psql está disponible
where psql >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ ERROR: psql no encontrado
    echo.
    echo PostrgreSQL no parece estar instalado o no está en el PATH
    echo.
    echo Descargar desde: https://www.postgresql.org/download/windows/
    echo.
    pause
    exit /b 1
)

echo ✓ PostgreSQL encontrado
echo.

REM Crear la base de datos
echo 📋 Creando base de datos 'yeyo_store'...
echo.

REM Intentar conectar y crear la base de datos
psql -U postgres -h localhost -c "CREATE DATABASE yeyo_store;" 2>nul

if %errorlevel% equ 0 (
    echo ✅ Base de datos 'yeyo_store' creada (o ya existe)
) else (
    echo ⚠️  No se pudo conectar a PostgreSQL
    echo.
    echo Verifica que:
    echo  1. PostgreSQL está corriendo
    echo  2. Usuario 'postgres' existe (por defecto típicamente sí existe)
    echo  3. La contraseña es 'postgres' (por defecto)
    echo.
    echo Si PostgreSQL pide contraseña y no sabes cuál es, prueba:
    echo  - postgres (la predeterminada)
    echo  - Leave blank and press Enter
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Base de datos configurada correctamente
echo.
echo Ahora puedes ejecutar:
echo  - .\start.bat (para iniciar la aplicación)
echo  - .\start.ps1 (alternativa con PowerShell)
echo.
pause
