import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { useCart } from '../context/CartContext'
import { Link } from 'react-router-dom'
import './Cart.css'

const Cart = () => {
  const { getAuthHeaders, isAuthenticated, user, loading: authLoading } = useAuth()
  const { carrito, actualizarCantidad, eliminarDelCarrito, vaciarCarrito, calcularTotal } = useCart()
  
  const [usuario, setUsuario] = useState(null)
  const [direcciones, setDirecciones] = useState([])
  const [ordenes, setOrdenes] = useState([])
  const [direccionSeleccionada, setDireccionSeleccionada] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [codigoCupon, setCodigoCupon] = useState('')

  // Cargar información del usuario
  useEffect(() => {
    if (!isAuthenticated) return

    const cargarDatos = async () => {
      setLoading(true)
      setError('')
      try {
        const headers = getAuthHeaders()
        
        // Cargar usuario actual
        const resUsuario = await fetch('http://localhost:8000/api/usuarios/me', {
          headers
        })
        if (!resUsuario.ok) {
          throw new Error(`Error ${resUsuario.status}: ${resUsuario.statusText}`)
        }
        const usuarioData = await resUsuario.json()
        setUsuario(usuarioData)

        // Cargar direcciones del usuario
        const resDirecciones = await fetch('http://localhost:8000/api/usuarios/me/direcciones', {
          headers
        })
        if (!resDirecciones.ok) {
          throw new Error(`Error cargando direcciones: ${resDirecciones.statusText}`)
        }
        const direccionesData = await resDirecciones.json()
        setDirecciones(direccionesData)

        // Cargar órdenes del usuario
        const resOrdenes = await fetch('http://localhost:8000/api/ordenes', {
          headers
        })
        if (resOrdenes.ok) {
          const ordenesData = await resOrdenes.json()
          setOrdenes(Array.isArray(ordenesData) ? ordenesData : [])
        } else {
          // Si falla, simplemente no mostrar órdenes (usuario nuevo)
          console.warn('No se pudieron cargar las órdenes previas:', resOrdenes.status)
          setOrdenes([])
        }
      } catch (err) {
        console.error('Error en cargarDatos:', err)
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    cargarDatos()
  }, [isAuthenticated])

  // Manejar checkout
  const handleCheckout = async () => {
    if (!direccionSeleccionada) {
      setError('Por favor selecciona una dirección de envío')
      return
    }

    if (carrito.length === 0) {
      setError('Tu carrito está vacío')
      return
    }

    try {
      // Primero, obtener todas las tallas del servidor
      const resTallas = await fetch('http://localhost:8000/api/tallas', {
        headers: getAuthHeaders()
      })
      if (!resTallas.ok) {
        throw new Error('Error cargando tallas')
      }
      const tallas = await resTallas.json()
      
      // Crear un mapeo de valor_talla -> id_talla
      const tallaMap = {}
      tallas.forEach((talla) => {
        tallaMap[talla.valor_talla] = talla.id_talla
      })

      // Construir detalles del pedido con id_talla correcto
      const detalles = carrito.map((item) => {
        const id_talla = tallaMap[item.talla]
        if (!id_talla) {
          throw new Error(`Talla ${item.talla} no encontrada en el servidor`)
        }
        return {
          id_producto: item.id_producto,
          id_talla,
          cantidad_detalle_pedido: item.cantidad
        }
      })

      const pedidoCreate = {
        id_direccion_entrega_pedido: parseInt(direccionSeleccionada),
        detalles,
        codigo_cupon_aplicado: codigoCupon || undefined
      }

      const response = await fetch('http://localhost:8000/api/ordenes', {
        method: 'POST',
        headers: {
          ...getAuthHeaders(),
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(pedidoCreate)
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.detail || 'Error creando la orden')
      }

      const nuevaOrden = await response.json()
      setOrdenes([nuevaOrden, ...ordenes])
      vaciarCarrito()
      setError('')
      setDireccionSeleccionada('')
      setCodigoCupon('')
      alert(`✅ Orden #${nuevaOrden.id_pedido} creada exitosamente`)
    } catch (err) {
      setError(err.message)
    }
  }

  // Cargando autenticación
  if (authLoading) {
    return (
      <div className="cart-container">
        <div className="loading-message">
          <p>Cargando...</p>
        </div>
      </div>
    )
  }

  // No autenticado
  if (!isAuthenticated) {
    return (
      <div className="cart-container">
        <div className="auth-message">
          <h2>Debes estar logueado para ver tu carrito</h2>
          <p>Por favor inicia sesión o regístrate para continuar</p>
          <a href="/login" className="btn-login">Ir a Login</a>
        </div>
      </div>
    )
  }

  // Cargando datos
  if (loading) {
    return <div className="cart-container loading-message"><p>Cargando datos...</p></div>
  }

  const total = calcularTotal()

  return (
    <div className="cart-container">
      <h1>Mi Carrito</h1>

      {error && <div className="error-message">{error}</div>}

      <div className="cart-content">
        {/* Sección de productos */}
        <div className="cart-items">
          <h2>Productos ({carrito.length})</h2>
          
          {carrito.length === 0 ? (
            <div className="empty-cart">
              <p>Tu carrito está vacío</p>
              <a href="/productos" className="btn-continue">Continuar comprando</a>
            </div>
          ) : (
            <>
              <div className="items-list">
                {carrito.map((item) => (
                  <div key={`${item.id_producto}-${item.talla}`} className="cart-item">
                    <div className="item-image">
                      {item.imagen && <img src={item.imagen} alt={item.nombre_producto} />}
                    </div>
                    <div className="item-info">
                      <h4>{item.nombre_producto}</h4>
                      <p className="talla">Talla: {item.talla}</p>
                      <p className="price">₡{Number(item.precio_producto).toLocaleString('es-CR')}</p>
                    </div>
                    <div className="item-quantity">
                      <label>Cantidad:</label>
                      <div className="qty-control">
                        <button onClick={() => actualizarCantidad(item.id_producto, item.talla, item.cantidad - 1)}>-</button>
                        <span>{item.cantidad}</span>
                        <button onClick={() => actualizarCantidad(item.id_producto, item.talla, item.cantidad + 1)}>+</button>
                      </div>
                    </div>
                    <div className="item-subtotal">
                      <p>₡{Number(item.precio_producto * item.cantidad).toLocaleString('es-CR')}</p>
                    </div>
                    <button 
                      className="btn-remove"
                      onClick={() => eliminarDelCarrito(item.id_producto, item.talla)}
                    >
                      ✕
                    </button>
                  </div>
                ))}
              </div>

              <button className="btn-clear" onClick={vaciarCarrito}>
                Vaciar carrito
              </button>
            </>
          )}
        </div>

        {/* Sección de checkout */}
        {carrito.length > 0 && (
          <div className="checkout-section">
            <h2>Resumen de compra</h2>
            
            {/* Información del usuario */}
            {usuario && (
              <div className="user-info">
                <h3>Cliente</h3>
                <p><strong>{usuario.nombre_usuario}</strong></p>
                <p>{usuario.email_usuario}</p>
              </div>
            )}

            {/* Seleccionar dirección */}
            <div className="addresses-section">
              <h3>Dirección de envío</h3>
              {direcciones.length === 0 ? (
                <p className="no-addresses">No tienes direcciones registradas. <a href="/perfil">Agregar dirección</a></p>
              ) : (
                <select 
                  value={direccionSeleccionada}
                  onChange={(e) => setDireccionSeleccionada(e.target.value)}
                  className="address-select"
                >
                  <option value="">Selecciona una dirección</option>
                  {direcciones.map((dir) => (
                    <option key={dir.id_direccion} value={dir.id_direccion}>
                      {dir.calle_direccion} {dir.numero_direccion}, {dir.provincia_direccion}
                    </option>
                  ))}
                </select>
              )}
            </div>

            {/* Cupón */}
            <div className="coupon-section">
              <h3>Código de cupón (opcional)</h3>
              <div className="coupon-input">
                <input 
                  type="text"
                  placeholder="Ingresa código de cupón"
                  value={codigoCupon}
                  onChange={(e) => setCodigoCupon(e.target.value.toUpperCase())}
                  className="input-coupon"
                />
              </div>
            </div>

            {/* Totales */}
            <div className="totals">
              <div className="total-row">
                <span>Subtotal:</span>
                <strong>₡{Number(total).toLocaleString('es-CR')}</strong>
              </div>
              <div className="total-row">
                <span>Envío:</span>
                <strong>Gratis</strong>
              </div>
              <div className="total-row final">
                <span>Total:</span>
                <strong>₡{Number(total).toLocaleString('es-CR')}</strong>
              </div>
            </div>

            {/* Botón checkout */}
            <button 
              className="btn-checkout"
              onClick={handleCheckout}
              disabled={!direccionSeleccionada || carrito.length === 0}
            >
              Procesar compra
            </button>
          </div>
        )}
      </div>

      {/* Órdenes recientes */}
      <div className="orders-section">
        <h2>Tus órdenes recientes</h2>
        {ordenes.length === 0 ? (
          <div className="empty-orders">
            <p>No tienes órdenes recientes</p>
            <a href="/productos" className="btn-continue">Ir a comprar</a>
          </div>
        ) : (
          <div className="orders-list">
            {ordenes.slice(0, 5).map((orden) => (
              <div key={orden.id_pedido} className="order-card">
                <div className="order-header">
                  <h4>Orden #{orden.id_pedido}</h4>
                  <span className={`status status-${orden.estado_pedido_pedido}`}>{orden.estado_pedido_pedido}</span>
                </div>
                <p className="order-date">{new Date(orden.fecha_pedido_pedido).toLocaleDateString('es-CR')}</p>
                <p className="order-total">₡{Number(orden.monto_total_pedido).toLocaleString('es-CR')}</p>
                <Link to={`/orden/${orden.id_pedido}`} className="order-details-link">
                  Ver detalles →
                </Link>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default Cart
