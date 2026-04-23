import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { useCart } from '../context/CartContext'
import { Link, useNavigate } from 'react-router-dom'
import './Cart.css'

const Cart = () => {
  const { getAuthHeaders, isAuthenticated, user, loading: authLoading } = useAuth()
  const { carrito, actualizarCantidad, eliminarDelCarrito, vaciarCarrito, calcularTotal } = useCart()
  const navigate = useNavigate()
  const API_BASE = (import.meta.env.VITE_API_URL || 'http://localhost:8000')
    .replace(/\/$/, '')
    .replace(/\/api$/, '')
  const PAYMENT_STORAGE_KEY = 'yeyo_payment_methods'
  
  const [usuario, setUsuario] = useState(null)
  const [direcciones, setDirecciones] = useState([])
  const [ordenes, setOrdenes] = useState([])
  const [paymentMethods, setPaymentMethods] = useState([])
  const [selectedPaymentMethodId, setSelectedPaymentMethodId] = useState('')
  const [showAddPaymentForm, setShowAddPaymentForm] = useState(false)
  const [paymentForm, setPaymentForm] = useState({
    titular: '',
    numero: '',
    mesExp: '',
    anioExp: ''
  })
  const [direccionSeleccionada, setDireccionSeleccionada] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [codigoCupon, setCodigoCupon] = useState('')

  const getCardBrand = (numero) => {
    if (!numero) return 'Tarjeta'
    if (numero.startsWith('4')) return 'Visa'
    if (/^5[1-5]/.test(numero)) return 'Mastercard'
    if (/^3[47]/.test(numero)) return 'Amex'
    return 'Tarjeta'
  }

  const formatMaskedCard = (numero) => {
    const clean = numero.replace(/\D/g, '')
    const last4 = clean.slice(-4)
    return `**** **** **** ${last4}`
  }

  const loadPaymentMethods = () => {
    const raw = localStorage.getItem(PAYMENT_STORAGE_KEY)
    if (!raw) {
      setPaymentMethods([])
      return
    }
    try {
      const parsed = JSON.parse(raw)
      if (Array.isArray(parsed)) {
        setPaymentMethods(parsed)
        if (parsed.length > 0 && !selectedPaymentMethodId) {
          setSelectedPaymentMethodId(String(parsed[0].id))
        }
      }
    } catch {
      setPaymentMethods([])
    }
  }

  const savePaymentMethods = (methods) => {
    setPaymentMethods(methods)
    localStorage.setItem(PAYMENT_STORAGE_KEY, JSON.stringify(methods))
  }

  const handleAddPaymentMethod = () => {
    const cleanNumber = paymentForm.numero.replace(/\D/g, '')
    const mes = parseInt(paymentForm.mesExp, 10)
    const anio = parseInt(paymentForm.anioExp, 10)

    if (!paymentForm.titular.trim()) {
      setError('Ingresa el nombre del titular')
      return
    }

    if (cleanNumber.length < 13 || cleanNumber.length > 19) {
      setError('Ingresa un numero de tarjeta valido')
      return
    }

    if (!mes || mes < 1 || mes > 12) {
      setError('Mes de expiracion invalido')
      return
    }

    if (!anio || anio < new Date().getFullYear()) {
      setError('Anio de expiracion invalido')
      return
    }

    const newMethod = {
      id: Date.now(),
      titular: paymentForm.titular.trim(),
      marca: getCardBrand(cleanNumber),
      maskedNumber: formatMaskedCard(cleanNumber),
      mesExp: mes,
      anioExp: anio
    }

    const updated = [newMethod, ...paymentMethods]
    savePaymentMethods(updated)
    setSelectedPaymentMethodId(String(newMethod.id))
    setPaymentForm({ titular: '', numero: '', mesExp: '', anioExp: '' })
    setShowAddPaymentForm(false)
    setError('')
  }

  useEffect(() => {
    if (isAuthenticated) {
      loadPaymentMethods()
    }
  }, [isAuthenticated])

  // Cargar información del usuario
  useEffect(() => {
    if (!isAuthenticated) return

    const cargarDatos = async () => {
      setLoading(true)
      setError('')
      try {
        const headers = getAuthHeaders()
        
        // Cargar usuario actual
        const resUsuario = await fetch(`${API_BASE}/api/usuarios/me`, {
          headers
        })
        if (!resUsuario.ok) {
          throw new Error(`Error ${resUsuario.status}: ${resUsuario.statusText}`)
        }
        const usuarioData = await resUsuario.json()
        setUsuario(usuarioData)

        // Cargar direcciones del usuario
        const resDirecciones = await fetch(`${API_BASE}/api/usuarios/me/direcciones`, {
          headers
        })
        if (!resDirecciones.ok) {
          throw new Error(`Error cargando direcciones: ${resDirecciones.statusText}`)
        }
        const direccionesData = await resDirecciones.json()
        setDirecciones(direccionesData)

        // Cargar órdenes del usuario
        const resOrdenes = await fetch(`${API_BASE}/api/ordenes`, {
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

    if (!selectedPaymentMethodId) {
      setError('Selecciona un metodo de pago para continuar')
      return
    }

    try {
      // Primero, obtener todas las tallas del servidor
      const resTallas = await fetch(`${API_BASE}/api/tallas`, {
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

      const response = await fetch(`${API_BASE}/api/ordenes`, {
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

      const metodoPago = paymentMethods.find((m) => String(m.id) === String(selectedPaymentMethodId))

      vaciarCarrito()
      setError('')
      setDireccionSeleccionada('')
      setCodigoCupon('')
      navigate(`/pago/confirmacion/${nuevaOrden.id_pedido}`, {
        state: {
          pago: {
            metodo: metodoPago ? `${metodoPago.marca} ${metodoPago.maskedNumber}` : 'Tarjeta registrada',
            total
          }
        }
      })
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

            {/* Metodo de pago */}
            <div className="payment-methods-section">
              <h3>Metodo de pago</h3>

              {paymentMethods.length === 0 ? (
                <p className="no-payment-methods">No tienes metodos de pago guardados.</p>
              ) : (
                <select
                  value={selectedPaymentMethodId}
                  onChange={(e) => setSelectedPaymentMethodId(e.target.value)}
                  className="payment-method-select"
                >
                  <option value="">Selecciona un metodo</option>
                  {paymentMethods.map((method) => (
                    <option key={method.id} value={method.id}>
                      {method.marca} {method.maskedNumber} - Exp {String(method.mesExp).padStart(2, '0')}/{method.anioExp}
                    </option>
                  ))}
                </select>
              )}

              <button
                type="button"
                className="btn-add-payment"
                onClick={() => setShowAddPaymentForm((prev) => !prev)}
              >
                {showAddPaymentForm ? 'Cancelar' : 'Agregar tarjeta'}
              </button>

              {showAddPaymentForm && (
                <div className="payment-form">
                  <input
                    type="text"
                    placeholder="Titular"
                    value={paymentForm.titular}
                    onChange={(e) => setPaymentForm((prev) => ({ ...prev, titular: e.target.value }))}
                    className="input-payment"
                  />
                  <input
                    type="text"
                    placeholder="Numero de tarjeta"
                    value={paymentForm.numero}
                    onChange={(e) => setPaymentForm((prev) => ({ ...prev, numero: e.target.value }))}
                    className="input-payment"
                  />
                  <div className="payment-exp-grid">
                    <input
                      type="number"
                      placeholder="MM"
                      min="1"
                      max="12"
                      value={paymentForm.mesExp}
                      onChange={(e) => setPaymentForm((prev) => ({ ...prev, mesExp: e.target.value }))}
                      className="input-payment"
                    />
                    <input
                      type="number"
                      placeholder="AAAA"
                      min={new Date().getFullYear()}
                      value={paymentForm.anioExp}
                      onChange={(e) => setPaymentForm((prev) => ({ ...prev, anioExp: e.target.value }))}
                      className="input-payment"
                    />
                  </div>
                  <button type="button" className="btn-save-payment" onClick={handleAddPaymentMethod}>
                    Guardar tarjeta
                  </button>
                  <p className="payment-note">Solo se guarda informacion enmascarada (no CVV).</p>
                </div>
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
