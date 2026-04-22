import { useState, useEffect } from 'react'
import { useAuth } from '../../context/AuthContext'
import { useNavigate } from 'react-router-dom'
import './Inventario.css'

const Inventario = () => {
  const { getAuthHeaders } = useAuth()
  const navigate = useNavigate()
  const API_BASE = (import.meta.env.VITE_API_URL || 'http://localhost:8000')
    .replace(/\/$/, '')
    .replace(/\/api$/, '')
  const [productos, setProductos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [searchTerm, setSearchTerm] = useState('')
  const [filtroStock, setFiltroStock] = useState({ min: null, max: null })
  const [toastMessage, setToastMessage] = useState('')
  const [toastVisible, setToastVisible] = useState(false)

  // Cargar inventario
  useEffect(() => {
    cargarInventario()
  }, [])

  const cargarInventario = async () => {
    setLoading(true)
    setError('')
    try {
      const response = await fetch(`${API_BASE}/api/admin/inventario?limit=500`, {
        headers: getAuthHeaders()
      })

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`)
      }

      const data = await response.json()
      setProductos(Array.isArray(data) ? data : [])
    } catch (err) {
      console.error('Error cargando inventario:', err)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const mostrarToast = (mensaje) => {
    setToastMessage(mensaje)
    setToastVisible(true)
    setTimeout(() => setToastVisible(false), 3000)
  }

  // Buscar productos
  const productosFiltrados = productos.filter((p) => {
    const matchSearch = searchTerm === '' || 
      p.nombre_producto.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.marca_producto.toLowerCase().includes(searchTerm.toLowerCase())

    const matchStock = (filtroStock.min === null || p.stock_producto >= filtroStock.min) &&
      (filtroStock.max === null || p.stock_producto <= filtroStock.max)

    return matchSearch && matchStock
  })

  const handleEditProduct = (productoId) => {
    navigate(`/admin/productos/${productoId}/editar`)
  }

  const handleDeleteStock = async (productoId) => {
    if (!confirm('¿Establecer stock a 0?')) return

    try {
      const response = await fetch(`${API_BASE}/api/admin/productos/${productoId}/stock?nuevo_stock=0`, {
        method: 'PATCH',
        headers: getAuthHeaders()
      })

      if (!response.ok) {
        throw new Error('Error actualizando stock')
      }

      // Actualizar lista
      setProductos(productos.map(p => 
        p.id_producto === productoId ? { ...p, stock_producto: 0 } : p
      ))
      mostrarToast('✅ Stock establecido a 0')
    } catch (err) {
      mostrarToast(`❌ ${err.message}`)
    }
  }

  if (loading) {
    return (
      <div className="inventario-container">
        <div className="loading-message">Cargando inventario...</div>
      </div>
    )
  }

  return (
    <div className="inventario-container">
      <div className="inventario-header">
        <h1>📦 Inventario</h1>
        <p className="total-productos">Total: {productosFiltrados.length} productos</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      {/* Filtros */}
      <div className="inventario-filtros">
        <div className="filtro-busqueda">
          <input
            type="text"
            placeholder="Buscar por nombre o marca..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="filtro-stock">
          <label>Stock Mínimo:</label>
          <input
            type="number"
            min="0"
            placeholder="Min"
            value={filtroStock.min || ''}
            onChange={(e) => setFiltroStock({
              ...filtroStock,
              min: e.target.value === '' ? null : parseInt(e.target.value)
            })}
            className="input-small"
          />
        </div>

        <div className="filtro-stock">
          <label>Stock Máximo:</label>
          <input
            type="number"
            min="0"
            placeholder="Max"
            value={filtroStock.max || ''}
            onChange={(e) => setFiltroStock({
              ...filtroStock,
              max: e.target.value === '' ? null : parseInt(e.target.value)
            })}
            className="input-small"
          />
        </div>

        <button
          onClick={() => {
            setSearchTerm('')
            setFiltroStock({ min: null, max: null })
          }}
          className="btn-limpiar"
        >
          Limpiar
        </button>
      </div>

      {/* Tabla de inventario */}
      <div className="inventario-tabla-wrapper">
        {productosFiltrados.length === 0 ? (
          <div className="empty-estado">
            <p>No hay productos que coincidan con los filtros</p>
          </div>
        ) : (
          <table className="inventario-tabla">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Marca</th>
                <th>Categoría</th>
                <th>Precio</th>
                <th>Stock</th>
                <th>Calificación</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {productosFiltrados.map((producto) => (
                <tr key={producto.id_producto} className={`stock-${producto.stock_producto > 10 ? 'ok' : producto.stock_producto > 0 ? 'bajo' : 'agotado'}`}>
                  <td className="id-cell">{producto.id_producto}</td>
                  <td className="nombre-cell">{producto.nombre_producto}</td>
                  <td>{producto.marca_producto}</td>
                  <td>{producto.categoria_producto}</td>
                  <td className="precio-cell">₡{Number(producto.precio_producto).toLocaleString('es-CR')}</td>
                  <td className="stock-cell">
                    <span className={`stock-badge ${producto.stock_producto === 0 ? 'cero' : producto.stock_producto < 10 ? 'bajo' : 'normal'}`}>
                      {producto.stock_producto}
                    </span>
                  </td>
                  <td className="calificacion-cell">
                    ⭐ {producto.promedio_calificacion_producto.toFixed(1)}
                  </td>
                  <td className="acciones-cell">
                    <button
                      onClick={() => handleEditProduct(producto.id_producto)}
                      className="btn-editar"
                      title="Editar producto"
                    >
                      ✏️
                    </button>
                    <button
                      onClick={() => handleDeleteStock(producto.id_producto)}
                      className="btn-accion-peligro"
                      title="Establecer stock a 0"
                    >
                      🗑️
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Toast */}
      {toastVisible && <div className="toast-notification">{toastMessage}</div>}
    </div>
  )
}

export default Inventario
