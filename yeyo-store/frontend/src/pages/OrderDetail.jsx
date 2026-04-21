import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './OrderDetail.css'

const OrderDetail = () => {
  const { id } = useParams()
  const { getAuthHeaders, isAuthenticated } = useAuth()
  const API_BASE = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '')
  const [pedido, setPedido] = useState(null)
  const [direccion, setDireccion] = useState(null)
  const [productoImages, setProductoImages] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  // Fake tracking timeline data for all orders (all confirmed)
  const getTimelineStages = () => {
    const fecha = new Date(pedido?.fecha_pedido_pedido)
    const stages = [
      {
        label: 'Pedido confirmado',
        date: fecha,
        time: '9:15 am',
        completed: true
      },
      {
        label: 'Preparando envío',
        date: new Date(fecha.getTime() + 5 * 60 * 60 * 1000),
        time: '2:40 pm',
        completed: true
      },
      {
        label: 'En camino',
        date: new Date(fecha.getTime() + 24 * 60 * 60 * 1000),
        time: '8:00 am',
        completed: true
      },
      {
        label: 'Entregado',
        date: new Date(fecha.getTime() + 3 * 24 * 60 * 60 * 1000),
        time: null,
        completed: false
      }
    ]
    return stages
  }

  const getEstimatedDelivery = () => {
    if (!pedido?.fecha_pedido_pedido) return null
    const fecha = new Date(pedido.fecha_pedido_pedido)
    const delivery = new Date(fecha.getTime() + 3 * 24 * 60 * 60 * 1000)
    return delivery
  }

  useEffect(() => {
    if (isAuthenticated) {
      cargarDetallesPedido()
    }
  }, [id, isAuthenticated])

  const cargarDetallesPedido = async () => {
    setLoading(true)
    setError('')
    try {
      // Cargar pedido
      const resPedido = await fetch(`${API_BASE}/api/ordenes/${id}`, {
        headers: getAuthHeaders()
      })
      if (!resPedido.ok) throw new Error('Pedido no encontrado')
      const dataPedido = await resPedido.json()
      setPedido(dataPedido)

      // Cargar imágenes de productos
      if (dataPedido.detalles && dataPedido.detalles.length > 0) {
        const images = {}
        for (const detalle of dataPedido.detalles) {
          try {
            const resProducto = await fetch(
              `${API_BASE}/api/productos/${detalle.id_producto}`,
              { headers: getAuthHeaders() }
            )
            if (resProducto.ok) {
              const producto = await resProducto.json()
              images[detalle.id_producto] = producto
            }
          } catch (e) {
            console.log(`Error loading product ${detalle.id_producto}`)
          }
        }
        setProductoImages(images)
      }

      // Cargar dirección de entrega (por ahora usamos datos del pedido si están disponibles)
      // En una versión mejorada, el backend debería incluir la dirección en la respuesta
      setDireccion({
        nombre: 'Dirección de entrega',
        provincia: 'San José',
        canton: 'San José',
        distrito: 'Heredia',
        exacta: 'Barrio Los Ángeles, 200m norte del parque'
      })
    } catch (err) {
      setError(err.message || 'Error cargando la orden')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const formatFecha = (fecha) => {
    if (!fecha) return '-'
    return new Date(fecha).toLocaleDateString('es-CR', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    })
  }

  const getCurrentStageIndex = () => {
    if (!pedido) return 0
    // For demo: show "En camino" as current status (index 2)
    return 2
  }

  const formatPrice = (crcPrice) => {
    // Prices in order are already in CRC (with 30% discount applied)
    return Math.round(Number(crcPrice)).toLocaleString('es-CR')
  }

  if (!isAuthenticated) {
    return (
      <div className="order-detail-container">
        <div className="order-error">Debes iniciar sesión para ver tu orden</div>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="order-detail-container">
        <div className="order-loading">Cargando detalles de la orden...</div>
      </div>
    )
  }

  if (!pedido) {
    return (
      <div className="order-detail-container">
        <div className="order-error">
          <p>{error || 'Orden no encontrada'}</p>
          <Link to="/perfil" className="back-link">← Volver a mis pedidos</Link>
        </div>
      </div>
    )
  }

  const timeline = getTimelineStages()
  const currentStage = getCurrentStageIndex()
  const estimatedDelivery = getEstimatedDelivery()
  const firstItem = pedido.detalles?.[0]
  const producto = firstItem ? productoImages[firstItem.id_producto] : null

  return (
    <div className="order-detail-container">
      <div className="order-tracking-page">
        {/* Left Column - Tracking Info */}
        <div className="tracking-left">
          <div className="order-header-card">
            <div className="order-title-row">
              <h1>Pedido ORD-{String(pedido.id_pedido).padStart(4, '0')}</h1>
              <span className="status-badge-current">En camino</span>
            </div>
            {estimatedDelivery && (
              <p className="estimated-delivery">
                Fecha estimada de entrega: <strong>{formatFecha(estimatedDelivery)}</strong>
              </p>
            )}
          </div>

          {/* Timeline */}
          <div className="tracking-timeline">
            {timeline.map((stage, index) => (
              <div key={index} className={`timeline-stage ${index <= currentStage ? 'active' : ''} ${index === currentStage ? 'current' : ''}`}>
                <div className="timeline-dot"></div>
                {index < timeline.length - 1 && <div className="timeline-line"></div>}
                <div className="timeline-content">
                  <p className="stage-label">{stage.label}</p>
                  {stage.date && stage.time ? (
                    <p className="stage-date">{formatFecha(stage.date)} — {stage.time}</p>
                  ) : (
                    <p className="stage-date pending">Pendiente</p>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Delivery Address */}
          <div className="delivery-address-card">
            <h3>Dirección de entrega</h3>
            {direccion && (
              <div className="address-info">
                <p><strong>Jefferson Villalobos</strong></p>
                <p>{direccion.provincia}, Costa Rica</p>
                <p>{direccion.canton}, {direccion.canton}</p>
                <p>{direccion.exacta}</p>
              </div>
            )}
          </div>
        </div>

        {/* Right Column - Order Summary */}
        <div className="tracking-right">
          <div className="order-summary-card">
            <h2>Resumen del pedido</h2>

            {firstItem && (
              <div className="summary-item">
                <div className="item-image">
                  {producto?.fotos?.[0]?.ruta_foto_foto ? (
                    <img
                      src={`${API_BASE}${producto.fotos[0].ruta_foto_foto}`}
                      alt={producto.nombre_producto}
                      onError={(e) => (e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"%3E%3Crect fill="%23444" width="100" height="100"/%3E%3Ctext x="50" y="50" font-size="20" text-anchor="middle" dominant-baseline="middle" fill="%23999"%3E?%3C/text%3E%3C/svg%3E')}
                    />
                  ) : (
                    <div className="image-placeholder">📦</div>
                  )}
                </div>
                <div className="item-details">
                  <p className="item-name">{producto?.nombre_producto || `Producto #${firstItem.id_producto}`}</p>
                  <p className="item-size">Talla 41 x{firstItem.cantidad_detalle_pedido}</p>
                </div>
                <p className="item-price">₡{formatPrice(firstItem.precio_unitario_detalle_pedido)}</p>
              </div>
            )}

            <div className="summary-breakdown">
              <div className="breakdown-row">
                <span>Subtotal</span>
                <span>₡{formatPrice(pedido.monto_total_pedido)}</span>
              </div>
              <div className="breakdown-row">
                <span>Envío</span>
                <span className="shipping-free">Gratis</span>
              </div>
              <div className="breakdown-row total">
                <span>Total</span>
                <span>₡{formatPrice(pedido.monto_total_pedido)}</span>
              </div>
            </div>

            <button className="report-button">Reportar problema</button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default OrderDetail
