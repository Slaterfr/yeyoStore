# 👟 YeYo Store - Full Stack

Tienda de zapatos en línea con **FastAPI** (backend) + **SQLModel** (ORM) + **React + Vite** (frontend).

---

## 🚀 Inicio Rápido (Automatizado)

### En Windows:
```bash
start.bat
```

### En Linux/Mac/WSL:
```bash
bash start.sh
```

Esto inicia automáticamente ambos servicios:
- ✅ **Backend (FastAPI)** → http://localhost:8000
- ✅ **Frontend (React)** → http://localhost:3000

---

## 📋 Requisitos

- **Backend:** Python 3.10+, PostgreSQL 13+
- **Frontend:** Node.js 16+, npm
- **Sistema:** Windows, Linux, Mac

## 🔧 Configuración Manual

### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar
.\venv\Scripts\activate.ps1  # Windows
# o
source venv/bin/activate     # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Actualizar .env con tus credenciales PostgreSQL
# Base de datos: yeyo_store
# Usuario: postgres
# Contraseña: postgres (o la tuya)

# Iniciar servidor
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar dev server
npm run dev
```

---

## 📚 URLs Importantes

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000/api |
| Swagger Docs | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

---

## 📁 Estructura del Proyecto

```
yeyo-store/
├── backend/
│   ├── db/
│   │   ├── connection.py        # Conexión a BD con SQLModel
│   │   └── base.py              # Base para repositorio
│   ├── models/                  # 13 modelos SQLModel
│   │   ├── usuario.py
│   │   ├── producto.py
│   │   ├── pedido.py
│   │   └── ...
│   ├── services/                # Lógica de negocio
│   │   ├── auth_service.py
│   │   ├── producto_service.py
│   │   └── ...
│   ├── routers/                 # Endpoints API (44 rutas)
│   │   ├── auth.py
│   │   ├── productos.py
│   │   └── ...
│   ├── schemas/                 # Validación Pydantic
│   ├── repositories/            # CRUD genérico
│   ├── dependencies/            # Auth, excepciones
│   ├── main.py                  # Punto de entrada FastAPI
│   ├── config.py                # Configuración
│   ├── requirements.txt         # Dependencias Python
│   └── .env                     # Variables de entorno
│
├── frontend/
│   ├── src/
│   │   ├── components/          # Componentes reutilizables
│   │   │   └── Navigation.jsx
│   │   ├── context/             # Estado global
│   │   │   └── AuthContext.jsx  # Gestión de autenticación
│   │   ├── pages/               # Páginas principales
│   │   │   ├── Home.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Products.jsx
│   │   │   ├── Cart.jsx
│   │   │   └── ...
│   │   ├── App.jsx              # Router principal
│   │   ├── main.jsx             # Punto de entrada React
│   │   └── index.css            # Estilos globales
│   ├── package.json             # Dependencias Node
│   ├── vite.config.js           # Configuración Vite
│   └── .env                     # Variables de entorno
│
├── start.sh                     # Script para Linux/Mac
├── start.bat                    # Script para Windows
└── README.md                    # Este archivo
```

---

## 🎯 Características Implementadas

### Backend (44 endpoints)
- ✅ **Autenticación:** Registro, login, refresh token (JWT + bcrypt)
- ✅ **Usuarios:** CRUD + gestión de direcciones
- ✅ **Productos:** CRUD + fotos + filtrado por talla
- ✅ **Reseñas:** Crear, leer, calificación automática
- ✅ **Wishlist:** Agregar, listar, eliminar
- ✅ **Cupones:** Validación + aplicación
- ✅ **Órdenes:** Crear, listar, cancelar, rastrear
- ✅ **Pagos:** Registro de transacciones
- ✅ **Envíos:** Rastreo de entregas

### Frontend
- ✅ **Autenticación:** Login/Register con tokens en localStorage
- ✅ **Routing:** React Router con 8 páginas
- ✅ **Navigation:** Navbar con menú contextual (login/perfil)
- ✅ **Formularios:** Validación de entrada
- ✅ **State Management:** Context API para auth

---

## 🔐 Autenticación

1. Usuario registra email + contraseña
2. Backend valida y guarda contraseña con bcrypt
3. Responde con `access_token` + `refresh_token`
4. Frontend almacena tokens en localStorage
5. Todos los requests incluyen `Authorization: Bearer {token}`

## 💾 Base de Datos

13 tablas normalizadas (3NF):
- Usuarios, Direcciones
- Productos, Tallas, Fotos
- Reseñas, Wishlist
- Órdenes, DetallesPedido
- Pagos, Envíos, Cupones

---

## 📦 Stack Tecnológico

| Capa | Tecnologías |
|------|-------------|
| **Backend** | FastAPI 0.104, SQLModel 0.0.14, SQLAlchemy 2.0 |
| **BD** | PostgreSQL 13+ |
| **Frontend** | React 18, React Router 6, Vite 5 |
| **HTTP** | Axios |
| **Auth** | JWT (HS256), bcrypt |

---

## 🐛 Troubleshooting

### Puerto en uso

**Windows:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -i :8000
kill -9 <PID>
```

### Error de conexión a BD
- Verifica PostgreSQL está corriendo
- Comprueba credenciales en `backend/.env`
- Confirma que existe la BD `yeyo_store`

### npm no encuentra módulos
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 🚀 Próximos Pasos

1. **Configurar PostgreSQL:**
   - Crear BD: `yeyo_store`
   - Actualizar `.env` en backend

2. **Ejecutar startup script:**
   - `bash start.sh` o `start.bat`

3. **Probar autenticación:**
   - Registrarse en http://localhost:3000/register
   - Login en http://localhost:3000/login

4. **Completar frontend:**
   - Integrar llamadas API en Productos, Wishlist, Carrito
   - Implementar flujo de checkout

---

## 📝 Notas de Desarrollo

- Backend usa `--reload` para hot reload
- Frontend usa Vite para hot module replacement
- CORS configurado para localhost (ambos puertos)
- Tokens JWT expiran en 1 hora (configurable en `backend/config.py`)

---

¡Construido con ❤️ para YeYo Store! 👟

---

## 🏗️ Funcionalidades

### Backend (FastAPI)
- **GET `/api/products`** — Devuelve lista de 6 productos en memoria
- **POST `/api/orders`** — Recibe pedido, lo imprime en consola y devuelve `order_id`
- **POST `/api/auth/login`** — Login simulado (sin base de datos)
- **CORS habilitado** para conexión frontend-backend
- **Carpeta `/frontend` servida como archivos estáticos** en la raíz

### Frontend (SPA)
- **Catálogo interactivo** con 6 productos (Nike, Adidas, Vans, New Balance, Puma, Converse)
- **Filtros por categoría** (Tenis, Casual, Deportivo)
- **Carrito de compras** con selector de talla modal
- **Login simulado** (sin datos persistentes)
- **Notificaciones toast** para acciones
- **Diseño completamente responsivo** (móvil, tablet, desktop)

#### Secciones de la SPA:
1. **Catálogo** — Vista inicial con grid de productos
2. **Carrito** — Tabla de items agregados
3. **Login** — Formularios de iniciar sesión / registrarse

---

## 💰 Productos Disponibles

| Nombre | Precio | Categoría | Tallas |
|--------|--------|-----------|--------|
| Nike Air Max 270 | ₡65.000 | Tenis | 38-42 |
| Adidas Stan Smith | ₡48.000 | Casual | 37-41 |
| Vans Old Skool | ₡42.000 | Casual | 36-40 |
| New Balance 574 | ₡58.000 | Deportivo | 39-43 |
| Puma RS-X | ₡55.000 | Tenis | 38, 40-42 |
| Converse Chuck 70 | ₡38.000 | Casual | 36-41 |

---

## 🎨 Diseño

**Tema:** Oscuro (dark mode) con acento verde lima (`#a3e635`)

- **Fondo:** `#0f0f0f` (casi negro)
- **Cards:** `#1a1a1a` (gris oscuro)
- **Acento:** `#a3e635` (verde lima)
- **Tipografía:** Inter (Google Fonts)
- **Bordes:** Redondeados 12px
- **Navbar:** Sticky, con badge del carrito

---

## 📱 Responsividad

- **Grid de productos:** 3 columnas en desktop → 1 columna en móvil
- **Navbar:** Flexible en todos los tamaños
- **Modal y overlays:** Centrados en todos los dispositivos

---

## 🔐 Autenticación

**Simulada** (no hay validación real):
- Login acepta cualquier email que contenga `@`
- Genera un nombre a partir del email
- Token guardado en memoria del navegador
- Al cambiar de página se pierde la sesión (sin persistencia)

---

## 🛒 Flujo de Compra

1. Ver catálogo de productos
2. Filtrar por categoría (opcional)
3. Click en "Agregar al carrito" → Modal para elegir talla
4. Confirmar talla → Notificación toast verde
5. Ver carrito → Tabla con items
6. "Finalizar pedido" → Requiere iniciar sesión
7. Confirmación con número de orden (ej: `ORD-7392`)

---

## 📝 Notas de Desarrollo

### Backend
- Todo el código está en `main.py` (un solo archivo)
- Datos en memoria (lista de diccionarios Python)
- Sin validaciones complejas (es una demo)
- CORS habilitado para todos los orígenes

### Frontend
- SPA con cambio de secciones sin recargar la página
- Fetch API para comunicación con backend
- localStorage para guardar sesión (demo simple)
- Modales inline (sin librerías externas)

---

## 🎓 Caso de Uso Académico

Esta demo es ideal para presentaciones sobre:
- Architecture moderna de web apps (frontend/backend separados)
- REST APIs con FastAPI
- Single Page Applications (SPA)
- Diseño de UX/UI
- Gestión de estado en JavaScript
- Responsive design con CSS Grid

---

## ⚠️ Limitaciones (Demo)

- ❌ No hay persistencia de datos (base de datos)
- ❌ No hay validación real de email
- ❌ No hay encriptación de contraseñas
- ❌ Cart y sesión se limpian al recargar la página
- ❌ Sin autenticación real (JWT simulado)
- ✅ Perfecto para demostración académica

---

## 🚀 Próximas Mejoras (Opcional)

Para una versión de producción, agregar:
- PostgreSQL/MongoDB para persistencia
- Validación real de emails
- Hash de contraseñas (bcrypt)
- JWT tokens reales
- Base de datos de órdenes e historial
- Email de confirmación
- Pasarela de pagos (Stripe, MercadoPago)

---

**Creado para propósitos académicos | 2024**
