# 👟 YeYo Store - Documentación Técnica v1.0

**Fecha de generación:** Abril 16, 2026  
**Versión del proyecto:** 1.0.0  
**Base de datos:** PostgreSQL 13+  
**ORM:** SQLModel 0.0.14  
**Framework Web:** FastAPI 0.104.1

---

## 📋 Tabla de Contenidos

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Estructura de Carpetas](#estructura-de-carpetas)
4. [Modelos de Base de Datos](#modelos-de-base-de-datos)
5. [Análisis de Almacenamiento](#análisis-de-almacenamiento)
6. [Guía de Instalación](#guía-de-instalación)
7. [Endpoints de la API](#endpoints-de-la-api)
8. [Flujos de Negocio](#flujos-de-negocio)
9. [Consideraciones de Seguridad](#consideraciones-de-seguridad)
10. [Roadmap Futuro](#roadmap-futuro)

---

## 📊 Resumen Ejecutivo

### Objetivo
Transformar una tienda virtual de zapatos de datos en memoria a una arquitectura escalable con:
- ✅ Base de datos PostgreSQL normalizada (13 tablas)
- ✅ Capas de arquitectura separadas (routers → servicios → repositories → modelos)
- ✅ Autenticación JWT con refresh tokens
- ✅ 4 nuevas funcionalidades: wishlist, reseñas, galería de fotos, cupones

### Impacto
- **Performance:** Consultas optimizadas con índices en campos clave
- **Escalabilidad:** Arquitectura preparada para 2,000+ usuarios / 6,500+ pedidos anuales
- **Mantenibilidad:** Código modular con separación clara de responsabilidades
- **Seguridad:** Hashing de contraseñas (bcrypt), JWT tokens, validaciones centralizadas

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (HTML/CSS/JS)                   │
│                  Corre en http://localhost:8000                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP/REST API
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                          FASTAPI (main.py)                      │
│            Middleware: CORS, Error Handling, Auth              │
└────────┬────────────────────────────────────────────────┬───────┘
         │                                                  │
         ▼                                                  ▼
┌─────────────────────────┐              ┌────────────────────────┐
│      ROUTERS (API)      │              │   DEPENDENCIAS         │
├─────────────────────────┤              ├────────────────────────┤
│ /auth (login, refresh)  │              │ JWT Auth (get_current) │
│ /usuarios (CRUD)        │              │ Exceptions centralizadas
│ /productos (catálogo)   │              │ Password hashing       │
│ /ordenes (compras)      │              │                        │
│ /resenas (reviews)      │              │                        │
│ /wishlist (favoritos)   │              │                        │
│ /cupones (descuentos)   │              │                        │
└─────────────┬───────────┘              └────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        SERVICIOS (Business Logic)               │
├─────────────────────────────────────────────────────────────────┤
│ AuthService         │ UsuarioService      │ ProductoService     │
│ ReseñaService       │ ListaDeseosService  │ CuponService        │
│ DireccionService    │ ... (más servicios) │                     │
│                                                                  │
│ ✓ Validaciones de negocio                                       │
│ ✓ Cálculos de descuentos                                        │
│ ✓ Actualización de ratings                                      │
│ ✓ Manejo de transacciones                                       │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    REPOSITORIES (Data Access)                   │
├─────────────────────────────────────────────────────────────────┤
│ BaseRepository (CRUD genérico)                                  │
│   ↓                                                              │
│ UserRepository    │ ProductRepository    │ CuponRepository     │
│ DireccionRepo     │ ReseñaRepository     │ ListaDeseosRepo     │
│ ... (más repos)   │                      │                     │
│                                                                  │
│ ✓ Queries personalizadas                                        │
│ ✓ Índices optimizados                                           │
│ ✓ Manejo de sesiones                                            │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MODELOS SQLModel                           │
├─────────────────────────────────────────────────────────────────┤
│ Usuario | Direccion  | Producto  | Talla  | ProductoTalla      │
│ FotoProducto | Reseña | ListaDeseos | Cupon | Pedido           │
│ DetallePedido | Pago | Envio                                   │
│                                                                  │
│ ✓ Normalizados (sin multivalores)                               │
│ ✓ Relaciones definidas                                          │
│ ✓ Constraints únicos donde aplica                               │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PostgreSQL + SQLAlchemy                      │
│              Base de datos relacional completa                  │
└─────────────────────────────────────────────────────────────────┘
```

### Ventajas de esta arquitectura

| Aspecto | Beneficio |
|--------|----------|
| **Separación de capas** | Cada capa tiene responsabilidad clara, fácil de testear |
| **Reutilización** | BaseRepository evita código duplicado |
| **Mantenibilidad** | Cambios en BD solo afectan repositories |
| **Escalabilidad** | Servicios pueden cachearse o paralelizarse |
| **Seguridad** | Validaciones centralizadas en servicios |
| **Performance** | Queries optimizadas en repositories |

---

## 📁 Estructura de Carpetas

```
yeyo-store/
│
├── backend/
│   ├── config.py                 # ⚙️ Configuración centralizada
│   ├── main.py                   # 🚀 Punto de entrada FastAPI
│   ├── requirements.txt           # 📦 Dependencias Python
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   └── connection.py          # 🔌 Engine, SessionLocal, create_db_and_tables()
│   │
│   ├── dependencies/
│   │   ├── __init__.py
│   │   ├── auth.py               # 🔐 JWT, hashing, get_current_user()
│   │   └── exceptions.py          # ⚠️ Custom exceptions centralizadas
│   │
│   ├── schemas/                  # ✓ Pydantic + SQLModel schemas
│   │   ├── __init__.py
│   │   ├── auth.py               # LoginRequest, TokenResponse
│   │   ├── usuario.py            # UsuarioCreate, UsuarioResponse
│   │   ├── direccion.py
│   │   ├── producto.py
│   │   ├── reseña.py
│   │   ├── lista_deseos.py
│   │   ├── cupon.py
│   │   └── pedido.py
│   │
│   ├── models/                   # 🗄️ SQLModel (ORM)
│   │   ├── __init__.py
│   │   ├── usuario.py            # Tabla: usuario
│   │   ├── direccion.py          # Tabla: direccion
│   │   ├── producto.py           # Tabla: producto
│   │   ├── talla.py              # Tabla: talla
│   │   ├── producto_talla.py     # Tabla: producto_talla (many-to-many)
│   │   ├── foto_producto.py      # Tabla: foto_producto
│   │   ├── reseña.py             # Tabla: reseña
│   │   ├── lista_deseos.py       # Tabla: lista_deseos
│   │   ├── cupon.py              # Tabla: cupon
│   │   ├── pedido.py             # Tabla: pedido
│   │   ├── detalle_pedido.py     # Tabla: detalle_pedido
│   │   ├── pago.py               # Tabla: pago
│   │   └── envio.py              # Tabla: envio
│   │
│   ├── repositories/             # 🔍 Data access layer
│   │   ├── __init__.py
│   │   ├── base_repository.py    # CRUD genérico
│   │   ├── user_repository.py    # (Futuro - queries específicas)
│   │   ├── producto_repository.py
│   │   └── ... más repositories
│   │
│   ├── services/                 # 💼 Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py       # Registrar, login, refresh token
│   │   ├── user_service.py       # CRUD de usuarios
│   │   ├── direccion_service.py  # Gestión de direcciones
│   │   ├── producto_service.py   # Catálogo de productos
│   │   ├── reseña_service.py     # Reseñas y ratings
│   │   ├── lista_deseos_service.py # Wishlist
│   │   └── cupon_service.py      # Descuentos y validaciones
│   │
│   └── routers/                  # 🛣️ API endpoints
│       ├── __init__.py
│       ├── auth.py               # POST /auth/login, /auth/register, /auth/refresh
│       ├── usuarios.py           # GET/PUT /usuarios, dirección
│       ├── productos.py          # GET /productos, /productos/{id}
│       ├── ordenes.py            # POST/GET /ordenes
│       ├── resenas.py            # POST/GET /resenas
│       ├── wishlist.py           # POST/DELETE /wishlist
│       └── cupones.py            # GET /cupones/validate
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
├── .env                          # 🔑 Variables de entorno (NO subir a git)
└── ARQUITECTURA.md               # 📖 Este archivo
```

---

## 🗄️ Modelos de Base de Datos

### Entidad-Relación Normalizado

```
usuario (PK: id_usuario)
├── email_usuario (UNIQUE)
├── password_usuario (hasheado bcrypt)
└── Relaciones:
    ├── 1:many → direccion
    ├── 1:many → pedido
    ├── 1:many → reseña
    └── 1:many → lista_deseos

direccion (PK: id_direccion, FK: id_usuario)
├── Normalizado: provincia, canton, distrito separados
├── es_principal_direccion (booleano)
└── Relaciones:
    ├── many:1 → usuario
    ├── 1:many → pedido
    └── 1:many → envio

producto (PK: id_producto)
├── precio_producto (NUMERIC(10,2))
├── stock_producto
├── promedio_calificacion_producto (calculado)
└── Relaciones:
    ├── 1:many → foto_producto
    ├── 1:many → reseña
    ├── 1:many → detalle_pedido
    ├── 1:many → lista_deseos
    └── many:many → talla (a través de producto_talla)

talla (PK: id_talla)
├── valor_talla (36, 37, 38, ...)
├── tipo_medida_talla (EU, US, CM)
└── Relaciones:
    └── many:many → producto (a través de producto_talla)

producto_talla (PK: id_producto_talla)
⚠️ TABLA DE UNIÓN (many-to-many)
├── FK: id_producto, id_talla
├── stock_disponible_producto_talla
└── UNIQUE CONSTRAINT: (id_producto, id_talla)

foto_producto (PK: id_foto_producto, FK: id_producto)
├── url_foto_producto (URL externa Cloudinary)
├── es_principal_foto_producto
├── orden_foto_producto
└── Relaciones:
    └── many:1 → producto

reseña (PK: id_reseña, FK: id_usuario, id_producto)
├── calificacion_reseña (1-5)
├── titulo_reseña
├── comentario_reseña (TEXT)
├── UNIQUE CONSTRAINT: (id_usuario, id_producto)
└── Relaciones:
    ├── many:1 → usuario
    └── many:1 → producto

lista_deseos (PK: id_lista_deseos, FK: id_usuario, id_producto)
⚠️ WISHLIST
├── UNIQUE CONSTRAINT: (id_usuario, id_producto)
└── Relaciones:
    ├── many:1 → usuario
    └── many:1 → producto

cupon (PK: id_cupon)
├── codigo_cupon (UNIQUE)
├── descuento_porcentaje_cupon (NUMERIC(5,2))
├── maximo_usos_cupon
├── contador_usos_cupon
├── fecha_expiracion_cupon (NULL = sin expirar)
├── esta_activo_cupon
└── Relaciones:
    └── 1:many → pedido

pedido (PK: id_pedido)
├── FK: id_usuario, id_direccion_entrega, id_cupon_aplicado (nullable)
├── fecha_pedido_pedido (TIMESTAMP)
├── fecha_entrega_pedido (nullable)
├── monto_total_pedido (con descuento aplicado)
├── estado_pedido_pedido (pendiente, confirmado, enviado, entregado)
└── Relaciones:
    ├── many:1 → usuario
    ├── many:1 → direccion
    ├── many:1 → cupon (nullable)
    ├── 1:many → detalle_pedido
    ├── 1:1 → pago (nullable)
    └── 1:1 → envio (nullable)

detalle_pedido (PK: id_detalle_pedido)
✨ NUEVO: precio_unitario_detalle_pedido (historial de precios)
├── FK: id_pedido, id_producto, id_talla
├── cantidad_detalle_pedido
├── precio_unitario_detalle_pedido (NUMERIC(10,2)) ← NUEVO
├── impuesto_detalle_pedido (13% IVA Costa Rica)
├── subtotal_detalle_pedido (calculado)
└── Relaciones:
    ├── many:1 → pedido
    ├── many:1 → producto
    └── many:1 → talla

pago (PK: id_pago, FK: id_pedido UNIQUE)
├── Relación 1:1 con pedido
├── metodo_pago_pago (tarjeta, transferencia, sinpe)
├── estado_pago_pago (pendiente, completado, fallido)
└── Relaciones:
    └── 1:1 → pedido

envio (PK: id_envio, FK: id_pedido UNIQUE)
├── Relación 1:1 con pedido
├── FK: id_direccion_envio
├── estado_envio_envio (pendiente, en_transito, entregado)
├── fecha_envio_envio
├── costo_envio_envio (NUMERIC(8,2))
└── Relaciones:
    ├── 1:1 → pedido
    └── many:1 → direccion
```

### Tipos de Dato y Tamaños

| Tipo SQL | Python | Bytes | Rango |
|----------|--------|-------|-------|
| SERIAL | int | 4 | 0 a 2,147,483,647 |
| VARCHAR(n) | str | n | Cadenas de hasta n caracteres |
| TEXT | str | variable | Texto largo (sin límite práctico) |
| NUMERIC(p,d) | Decimal | 10 | Números decimales precisos |
| BOOLEAN | bool | 1 | true/false |
| TIMESTAMP | datetime | 8 | Fecha y hora con precisión |
| DATE | date | 4 | Fecha sin hora |

---

## 📊 Análisis de Almacenamiento

### Cálculo de Tamaño de BD Vacía

```
Overhead PostgreSQL (sistema):     3 MB
Estructura de tablas (13 tablas):  104 KB
═════════════════════════════════════════
Total BD Vacía:                    ~3.1 MB
```

### Proyección de Datos (3 Meses)

#### Supuestos
- Usuarios activos: 500 (crecimiento lineal 167/mes)
- Productos en catálogo: 100 (estáticos)
- Promedio 2 direcciones/usuario
- Promedio 3 fotos/producto
- Tallas: 10 opciones estándar
- **Pedidos:** 500/mes (1,500 en 3 meses)
- **Detalles pedido:** 3 items/pedido (4,500 registros)
- **Reseñas:** 10% de clientes reseñan (150 en 3 meses)
- **Wishlist:** 20% de clientes usan (300 items)
- **Cupones:** 5% de compras usan cupón

#### Mes 1

| Tabla | Registros | Bytes/Reg | Subtotal |
|-------|-----------|----------|----------|
| usuario | 167 | 400 | 67 KB |
| dirección | 334 | 350 | 117 KB |
| reseña | 50 | 1200 | 60 KB |
| lista_deseos | 100 | 30 | 3 KB |
| cupon | 30 | 100 | 3 KB |
| pedido | 500 | 250 | 125 KB |
| detalle_pedido | 1500 | 60 | 90 KB |
| pago | 500 | 100 | 50 KB |
| envio | 500 | 150 | 75 KB |
| **Subtotal datos** | — | — | **590 KB** |
| **Índices (30%)** | — | — | **177 KB** |
| **Mes 1 Total** | — | — | **~767 KB** |

#### Mes 3 (Acumulado)

| Tabla | Registros | Bytes/Reg | Subtotal |
|-------|-----------|----------|----------|
| usuario | 500 | 400 | 200 KB |
| dirección | 1000 | 350 | 350 KB |
| reseña | 150 | 1200 | 180 KB |
| lista_deseos | 300 | 30 | 9 KB |
| cupon | 30 | 100 | 3 KB |
| pedido | 1500 | 250 | 375 KB |
| detalle_pedido | 4500 | 60 | 270 KB |
| pago | 1500 | 100 | 150 KB |
| envio | 1500 | 150 | 225 KB |
| **Subtotal datos** | — | — | **1.7 MB** |
| **Índices (30%)** | — | — | **510 KB** |
| **Mes 3 Total** | — | — | **~2.2 MB** |

#### BD después de 3 meses
```
Overhead: 3.0 MB
Datos:    2.2 MB
═════════════════════
Total:    ~5.3 MB ✅ MUY MANEJABLE
```

### Crecimiento Temporal

**Diario (Mes 3):**
- +5.6 usuarios
- +16.7 pedidos
- +13 KB datos

**Mensual:**
- +167-200 usuarios
- +500-667 pedidos
- +400-450 KB datos

**Cuatrimestral (4 meses):**
| Métrica | Valor |
|---------|-------|
| Usuarios acumulados | 667 |
| Pedidos acumulados | 2,167 |
| Tamaño datos | ~3 MB |
| **BD Total** | **~6.1 MB** |
| Tasa crecimiento | +0.75 MB/mes |

### Proyección Anual

| Métrica | Proyección |
|---------|------------|
| Usuarios | 2,000 |
| Pedidos | 6,500 |
| **BD Principal** | **~12-15 MB** |
| **WAL (transaccional)** | 32-48 MB |
| **Total disco** | ~60 MB |
| **Capacidad servidor 2 GB** | 260+ meses (21+ años) |

### Archivos Transaccionales (WAL)

- **Segmentos:** 16 MB c/u, rotación automática
- **Generación:** 1.5-2 MB/mes
- **Espacio activo:** 32-48 MB
- **Backups 7 días:** 10-14 MB histórico

---

## 🚀 Guía de Instalación

### Prerrequisitos

```
- Python 3.10+
- PostgreSQL 13+
- pip (gestor de paquetes Python)
- Git
```

### Paso 1: Clonar/Configurar Proyecto

```bash
cd yeyo-store/backend
```

### Paso 2: Crear Virtual Environment

```bash
python -m venv venv

# Activar (Windows PowerShell)
.\\venv\\Scripts\\Activate.ps1

# O en cmd
venv\Scripts\activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Variables de Entorno

Editar `.env`:

```dotenv
# DATABASE
DATABASE_URL=postgresql://postgres:password@localhost:5432/yeyo_store

# JWT
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# APP
DEBUG=True
ENVIRONMENT=development
```

### Paso 5: Crear Base de Datos

```bash
# Desde PostgreSQL
createdb -U postgres yeyo_store
```

### Paso 6: Ejecutar Servidor

```bash
uvicorn backend.main:app --reload
```

**Salida esperada:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Paso 7: Acceder a la Aplicación

- **API:** http://localhost:8000
- **Docs Swagger:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Frontend:** http://localhost:8000

---

## 🔌 Endpoints de la API

### Autenticación (`/api/auth`)

```
POST /api/auth/register
├── Body: { "nombre_usuario", "email_usuario", "password_usuario" }
└── Response: UsuarioResponse

POST /api/auth/login
├── Body: { "email_usuario", "password_usuario" }
└── Response: { "access_token", "refresh_token", "token_type" }

POST /api/auth/refresh
├── Body: { "refresh_token" }
└── Response: { "access_token", "refresh_token", "token_type" }
```

### Usuarios (`/api/usuarios`)

```
GET /api/usuarios/me
├── Headers: Authorization: Bearer <access_token>
└── Response: UsuarioResponseDetallado

PUT /api/usuarios/me
├── Headers: Authorization: Bearer <access_token>
├── Body: { "nombre_usuario?", "email_usuario?" }
└── Response: UsuarioResponseDetallado

POST /api/usuarios/me/direcciones
├── Headers: Authorization: Bearer <access_token>
├── Body: DireccionCreate
└── Response: DireccionResponse

GET /api/usuarios/me/direcciones
├── Headers: Authorization: Bearer <access_token>
└── Response: List[DireccionResponse]
```

### Productos (`/api/productos`)

```
GET /api/productos
├── Query: skip=0, limit=100
└── Response: List[ProductoResponse]

GET /api/productos/{id}
├── Incluye: fotos, últimas 5 reseñas, rating, stock, tallas
└── Response: ProductoResponseDetallado

GET /api/productos?categoria=tenis
├── Filtra por categoría
└── Response: List[ProductoResponse]

GET /api/productos/{id}/fotos
├── Galería de imágenes
└── Response: List[FotoProducto]

GET /api/productos/{id}/resenas
├── Últimas reseñas
└── Response: List[ReseñaResponse]
```

### Reseñas (`/api/resenas`)

```
POST /api/productos/{id}/resenas
├── Headers: Authorization: Bearer <access_token>
├── Body: ReseñaCreate
├── Validaciones: usuario compró el producto, única reseña/usuario/producto
└── Response: ReseñaResponse

PUT /api/resenas/{id}
├── Headers: Authorization: Bearer <access_token>
├── Body: ReseñaUpdate
└── Response: ReseñaResponse

DELETE /api/resenas/{id}
├── Headers: Authorization: Bearer <access_token>
├── Recalcula rating promedio del producto
└── Response: { "success": true }
```

### Lista de Deseos (`/api/wishlist`)

```
POST /api/wishlist
├── Headers: Authorization: Bearer <access_token>
├── Body: { "id_producto" }
└── Response: ListaDeseosResponse

GET /api/wishlist
├── Headers: Authorization: Bearer <access_token>
└── Response: List[ListaDeseosResponse]

DELETE /api/wishlist/{id_producto}
├── Headers: Authorization: Bearer <access_token>
└── Response: { "success": true }
```

### Cupones (`/api/cupones`)

```
GET /api/cupones/validate?codigo=PROMO2024
├── Valida sin aplicar
├── Verificaciones: existe, activo, no expirado, usos restantes
└── Response: CuponValidateResponse

POST /api/ordenes
├── Headers: Authorization: Bearer <access_token>
├── Body: { "detalles", "id_direccion_entrega", "codigo_cupon?" }
├── Aplica cupón si se proporciona
└── Response: PedidoResponse
```

### Órdenes (`/api/ordenes`)

```
POST /api/ordenes
├── Headers: Authorization: Bearer <access_token>
├── Body: PedidoCreate (con items y dirección entrega)
├── Validaciones: stock disponible, cupón válido
└── Response: PedidoResponse (con monto total)

GET /api/ordenes
├── Headers: Authorization: Bearer <access_token>
├── Query: skip=0, limit=100
└── Response: List[PedidoResponse]

GET /api/ordenes/{id}
├── Headers: Authorization: Bearer <access_token>
├── Solo el dueño puede ver
└── Response: PedidoResponseDetallado
```

---

## 💼 Flujos de Negocio

### Flujo 1: Registro e Inicio de Sesión

```
Cliente anónimo
    ↓
POST /auth/register
├── Validar email único
├── Hashear contraseña (bcrypt)
└── Crear usuario en BD
    ↓
POST /auth/login
├── Buscar usuario por email
├── Verificar contraseña
├── Generar JWT tokens
└── Retornar access_token + refresh_token
    ↓
Cliente autenticado ✅
```

### Flujo 2: Comprar Producto con Cupón

```
Cliente autenticado
    ↓
GET /productos
└── Ver catálogo
    ↓
POST /wishlist ← (opcional)
└── Agregar favoritos
    ↓
GET /cupones/validate?codigo=PROMO
├── Validar cupón
│  ├── ¿Existe?
│  ├── ¿Está activo?
│  ├── ¿Expiró?
│  └── ¿Usos restantes?
└── Retornar descuento%
    ↓
POST /ordenes
├── Validar stock de cada item
├── Validar dirección entrega
├── Aplicar cupón (incrementar contador_usos)
├── Calcular monto total CON descuento
│  = (cantidad × precio + impuesto) - (monto_total × descuento%)
├── Crear orden
├── Crear detalle_pedido (con precio_unitario historial)
├── Crear pago (estado: pendiente)
└── Crear envío
    ↓
Orden confirmada ✅
Transacción completada
```

### Flujo 3: Dejar Reseña Sobre Producto

```
Cliente autenticado con compra previa
    ↓
GET /productos/{id}/resenas
└── Ver reseñas existentes
    ↓
POST /productos/{id}/resenas
├── Validar: usuario no ha reseñado antes
├── Crear reseña (calificación 1-5)
├── Guardar comentario
└── Trigger: actualizar promedio_calificacion_producto
    ↓
Reseña creada ✅
Rating promedio actualizado
    ↓
GET /productos/{id}
└── Mostrar nuevo rating en ficha
```

### Flujo 4: Gestionar Lista de Deseos

```
Cliente autenticado
    ↓
POST /wishlist
├── Validar: producto no está en wishlist
└── Agregar
    ↓
GET /wishlist
└── Ver todos los favoritos
    ↓
DELETE /wishlist/{id_producto}
└── Remover
    ↓
POST /ordenes (con productos de wishlist)
└── Comprar directamente desde wishlist
```

---

## 🔐 Consideraciones de Seguridad

### 1. Autenticación (JWT)

```python
# ✅ Access token: 30 minutos (corta duración)
# ✅ Refresh token: 7 días (para renovar sin re-loguear)
# ✅ Ambos firmados con SECRET_KEY secreto

Header: Authorization: Bearer <JWT_TOKEN>
Validación en cada endpoint protegido
```

### 2. Hashing de Contraseñas

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

# NUNCA guardar contraseña en texto plano
hashed = pwd_context.hash(password)
is_valid = pwd_context.verify(password, hashed)
```

### 3. Validaciones en Servicios

```python
# Excepciones centralizadas
- UsuarioNoEncontrado
- CredencialesInvalidas
- NoAutorizado (solo dueño puede editar)
- TokenInvalido/Expirado
```

### 4. CORS

```python
allow_origins = ["http://localhost:8000", "http://localhost:3000"]
allow_credentials = True
allow_methods = ["GET", "POST", "PUT", "DELETE"]
allow_headers = ["*"]
```

### 5. SQL Injection Prevention

```python
# ✅ SQLModel params are parameterized (safe)
# ❌ NUNCA hacer: f"SELECT * FROM usuario WHERE email = '{email}'"
# ✅ SIEMPRE hacer:
statement = select(Usuario).where(Usuario.email_usuario == email)
```

### 6. Validacion de Datos

```python
# Pydantic schemas validan:
- Tipos de dato
- Longitud de strings
- Rangos numéricosmínimos/máximos
- Emails válidos
- Enums
```

### 7. Errores Genéricos

```python
# ✅ NO revelar detalles de implementación
# Malo: "SQL syntax error near column 'foo'"
# Bueno: "Error al procesar solicitud"
```

### 8. Variables de Entorno

```bash
# .env NO debe subirse a Git
.git ignore:
.env
venv/
__pycache__/
*.pyc
```

### 9. HTTPS en Producción

```python
if settings.ENVIRONMENT == "production":
    assert DATABASE_URL.startswith("postgresql://")
    assert SECRET_KEY != "development-key"
    # Usar HTTPS, no HTTP
```

---

## 🗺️ Roadmap Futuro

### Fase 2: Mejoras Inmediatas

```
□ Crear routers (auth, usuarios, productos, ordenes, resenas, wishlist, cupones)
□ Script de seed data para llenar BD inicial
□ Tests unitarios (pytest)
□ Tests de integración
□ Paginación con cursor
□ Búsqueda full-text en productos
```

### Fase 3: Features de Negocio

```
□ Email transaccionales (confirmación, rechazo cupón, seguimiento)
□ SMS notificaciones
□ Sistema de puntos/rewards
□ Programa de referidos
□ Recomendaciones de productos (ML simple)
□ Carrito persistente entre sesiones
```

### Fase 4: Infraestructura & Operaciones

```
□ Docker + docker-compose
□ CI/CD (GitHub Actions)
□ Logging centralizado (Sentry)
□ Monitoreo de performance
□ Backups automáticos
□ Rate limiting en endpoints públicos
□ API versioning (/api/v1/, /api/v2/)
```

### Fase 5: Pagos & Transacciones

```
□ Integración Stripe
□ Integración PayPal
□ Procesamiento de reembolsos
□ Historial de transacciones
□ Reportes financieros
```

### Fase 6: Admin Dashboard

```
□ Panel de control (Flask/React)
□ Reportes de ventas
□ Gestión de inventario
□ Gestión de cupones
□ Estadísticas de usuarios
□ Moderation de reseñas
```

---

## 📞 Soporte Técnico

### Problemas Comunes

#### "psycopg2 error: could not connect to server"
```bash
# Verificar que PostgreSQL está corriendo
# Windows: Services → PostgreSQL
# Verificar DATABASE_URL en .env
```

#### "ModuleNotFoundError: No module named 'sqlmodel'"
```bash
pip install -r requirements.txt
```

#### "CORS blocked request"
```python
# Verificar que el origen está en CORS_ORIGINS
# development: allow_origins=["*"]
# production: allow_origins=["https://yourdomain.com"]
```

#### "Token expired"
```
Access token válido por 30 min
Usar refresh_token para generar nuevo access_token
POST /auth/refresh con refresh_token válido (7 días)
```

---

## 📚 Referencias

- **FastAPI:** https://fastapi.tiangolo.com/
- **SQLModel:** https://sqlmodel.tiangolo.com/
- **PostgreSQL:** https://www.postgresql.org/docs/
- **JWT:** https://tools.ietf.org/html/rfc7519
- **Bcrypt:** https://en.wikipedia.org/wiki/Bcrypt

---

## 📄 Changelog

### v1.0.0 (Abril 16, 2026)

✅ **Implementado:**
- Arquitectura completa (Routers → Servicios → Repositories → Modelos)
- 13 tablas normalizadas en PostgreSQL
- Autenticación JWT con refresh tokens
- 4 nuevas funcionalidades: wishlist, reseñas, galería, cupones
- System de excepciones centralizado
- Pydantic schemas para validación
- Documentación técnica completa

🔄 **Por hacer:** 
- Routers API endpoints
- Scripts de seed data
- Tests (unitarios e integración)

---

**Última actualización:** Abril 16, 2026  
**Autor:** Equipo de Desarrollo - YeYo Store  
**Licencia:** Privada - Proyecto Académico
