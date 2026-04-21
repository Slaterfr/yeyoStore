# 🚀 INSTRUCCIONES PARA ACTIVAR LAS 3 CORRECCIONES

## PASO 1: Update SQL de Precios ⚠️ MUY IMPORTANTE

Ejecuta este comando en tu base de datos MySQL **antes de reiniciar**:

```bash
# Copia y pega en tu cliente MySQL
source /path/to/backend/UPDATE_PRECIOS.sql
```

O directamente el SQL:
```sql
UPDATE producto
SET precio_producto = ROUND(precio_producto * 700, 2)
WHERE id_producto > 0;
```

**VERIFICAR CAMBIOS:**
```sql
SELECT id_producto, nombre_producto, precio_producto 
FROM producto 
LIMIT 5;
```

Deberías ver precios como: 59500, 77000, 87500, etc. (en lugar de 85, 110, 125)

---

## PASO 2: Reiniciar Frontend 🔄

```bash
cd yeyo-store/frontend

# Si está corriendo, presiona Ctrl+C primero, luego:
npm start
```

El navegador debería auto-abrir en `http://localhost:3000`

---

## PASO 3: Probar Funcionalidad 🧪

### A. Verificar Imágenes de Productos
1. Navega a "Productos" en el nav menu
2. Deberías ver:
   - ✅ Imágenes reales de zapatos (no placeholder SVG)
   - ✅ Nombre, marca, categoría, precio en colones
   - ✅ Dropdown para seleccionar talla (36-45)

### B. Prueba "Agregar al Carrito"
1. Selecciona una talla del dropdown
2. Cliquea "Agregar al carrito"
3. **Resultado esperado:**
   - Toast notification en esquina inferior derecha
   - Mensaje: "✅ [NombreProducto] (Talla [XX]) agregado al carrito"
   - Desaparece después de 3 segundos

4. **Si NO selecciona talla y cliquea:**
   - Toast dice: "⚠️ Por favor selecciona una talla"

### C. Verificar localStorage del Carrito
1. Abre DevTools: F12 → Application → localStorage
2. Deberías ver clave: `carrito`
3. Valor debería ser JSON con los productos: `[{id_producto, nombre_producto, talla, cantidad, ...}]`

### D. Verificar Precios
1. En la grid de productos, los precios deben mostrar:
   - ₡59,500 (en lugar de $85)
   - ₡77,000 (en lugar de $110)
   - etc.

---

## ¿ALGO NO FUNCIONA? 🔧

### Error: "Las imágenes no cargan"
**Solución:**
```bash
# Asegúrate que el backend esté corriendo:
cd yeyo-store/backend
python main.py  
# o
uvicorn main:app --reload
```

### Error: "No se ve el selector de talla"
**Solución:**
- Reinicia frontend: `npm start`
- Limpia cache: Ctrl+Shift+Delete en navegador
- Recarga página: Ctrl+R

### Error: "Al clickear botón no pasa nada"
**Solución:**
- Abre DevTools: F12 → Console
- Chequea si hay errores en rojo
- Verifica que CartContext esté importado en App.jsx

### Precios siguen en dólares
**Solución:**
- Ejecutaste el UPDATE SQL?
- Reiniciaste el backend después del UPDATE?
- Prueba: `SELECT * FROM producto LIMIT 1;` - chequea precio

---

## 📊 Resumen de URLs Importantes

| Componente | URL | Función |
|-----------|-----|---------|
| Frontend | http://localhost:3000 | App React |
| Productos | http://localhost:3000/productos | Fuerza cargar fotos |
| Backend API | http://localhost:8000 | Servidor FastAPI |
| Fotos API | http://localhost:8000/api/productos/1/fotos | Obtiene fotos |
| Docs API | http://localhost:8000/docs | Swagger UI |

---

## ✅ CHECKLIST FINAL

- [ ] UPDATE SQL ejecutado en BD
- [ ] Frontend reiniciado con `npm start`
- [ ] Backend corriendo (`uvicorn main:app --reload`)
- [ ] Imágenes de productos cargando
- [ ] Selector de talla visible
- [ ] Botón agrega al carrito y muestra toast
- [ ] Precios mostrados en colones (sin símbolo $)
- [ ] localStorage['carrito'] contiene datos
- [ ] Toast notification tiene animación slide-in

---

## 📞 Soporte

Si persisten problemas:
1. Verifica que TODOS los 3 servicios estén corriendo:
   - MySQL/MariaDB con BD `yeyo_store`
   - Backend Python en puerto 8000
   - Frontend Node en puerto 3000

2. Limpia todo:
   ```bash
   # Frontend
   rm -rf node_modules
   npm install
   npm start
   
   # Base de datos
   # Reinicia MySQL service
   ```

3. Chequea logs en DevTools (F12 → Console)
