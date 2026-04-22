import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import './EditProduct.css'

const EditProduct = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { getAuthHeaders } = useAuth()
  const API_BASE = (import.meta.env.VITE_API_URL || 'http://localhost:8000')
    .replace(/\/$/, '')
    .replace(/\/api$/, '')

  const [producto, setProducto] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)
  const [toastMessage, setToastMessage] = useState('')
  const [toastVisible, setToastVisible] = useState(false)

  const [formData, setFormData] = useState({
    nombre_producto: '',
    descripcion_producto: '',
    precio_producto: '',
    stock_producto: '',
    categoria_producto: '',
    marca_producto: ''
  })

  // Cargar producto
  useEffect(() => {
    cargarProducto()
  }, [id])

  const cargarProducto = async () => {
    setLoading(true)
    setError('')
    try {
      const response = await fetch(`${API_BASE}/api/productos/${id}`, {
        headers: getAuthHeaders()
      })

      if (!response.ok) {
        throw new Error('Producto no encontrado')
      }

      const data = await response.json()
      setProducto(data)
      setFormData({
        nombre_producto: data.nombre_producto,
        descripcion_producto: data.descripcion_producto,
        precio_producto: data.precio_producto,
        stock_producto: data.stock_producto,
        categoria_producto: data.categoria_producto,
        marca_producto: data.marca_producto
      })
    } catch (err) {
      console.error('Error cargando producto:', err)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const mostrarToast = (mensaje) => {
    setToastMessage(mensaje)
    setToastVisible(true)
    setTimeout(() => setToastVisible(false), 3000)
  }

  const handleGuardar = async (e) => {
    e.preventDefault()
    setSaving(true)
    setError('')

    try {
      const response = await fetch(`${API_BASE}/api/admin/productos/${id}`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify({
          nombre_producto: formData.nombre_producto,
          descripcion_producto: formData.descripcion_producto,
          precio_producto: parseFloat(formData.precio_producto),
          stock_producto: parseInt(formData.stock_producto),
          categoria_producto: formData.categoria_producto,
          marca_producto: formData.marca_producto
        })
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.detail || 'Error guardando producto')
      }

      mostrarToast('✅ Producto actualizado exitosamente')
      setTimeout(() => navigate('/admin/inventario'), 1500)
    } catch (err) {
      console.error('Error guardando:', err)
      setError(err.message)
      mostrarToast(`❌ ${err.message}`)
    } finally {
      setSaving(false)
    }
  }

  const handleCancelar = () => {
    navigate('/admin/inventario')
  }

  if (loading) {
    return (
      <div className="edit-product-container">
        <div className="loading-message">Cargando producto...</div>
      </div>
    )
  }

  if (!producto) {
    return (
      <div className="edit-product-container">
        <div className="error-message">
          <h2>Error</h2>
          <p>{error || 'Producto no encontrado'}</p>
          <button onClick={handleCancelar} className="btn-volver">Volver</button>
        </div>
      </div>
    )
  }

  return (
    <div className="edit-product-container">
      <div className="edit-header">
        <h1>✏️ Editar Producto</h1>
        <p className="producto-id">ID: {id}</p>
      </div>

      <form onSubmit={handleGuardar} className="edit-form">
        <div className="form-section">
          <h2>Información General</h2>

          <div className="form-group">
            <label htmlFor="nombre">Nombre del Producto *</label>
            <input
              type="text"
              id="nombre"
              name="nombre_producto"
              value={formData.nombre_producto}
              onChange={handleChange}
              required
              placeholder="Ej: Nike Air Max 90"
            />
          </div>

          <div className="form-group">
            <label htmlFor="descripcion">Descripción</label>
            <textarea
              id="descripcion"
              name="descripcion_producto"
              value={formData.descripcion_producto}
              onChange={handleChange}
              placeholder="Descripción detallada del producto"
              rows="4"
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="marca">Marca *</label>
              <input
                type="text"
                id="marca"
                name="marca_producto"
                value={formData.marca_producto}
                onChange={handleChange}
                required
                placeholder="Ej: Nike"
              />
            </div>

            <div className="form-group">
              <label htmlFor="categoria">Categoría *</label>
              <select
                id="categoria"
                name="categoria_producto"
                value={formData.categoria_producto}
                onChange={handleChange}
                required
              >
                <option value="">Selecciona categoría</option>
                <option value="Tenis">Tenis</option>
                <option value="Casual">Casual</option>
                <option value="Deportivo">Deportivo</option>
              </select>
            </div>
          </div>
        </div>

        <div className="form-section">
          <h2>Precios e Inventario</h2>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="precio">Precio (₡) *</label>
              <input
                type="number"
                id="precio"
                name="precio_producto"
                value={formData.precio_producto}
                onChange={handleChange}
                required
                step="0.01"
                min="0"
                placeholder="0.00"
              />
            </div>

            <div className="form-group">
              <label htmlFor="stock">Stock Disponible *</label>
              <input
                type="number"
                id="stock"
                name="stock_producto"
                value={formData.stock_producto}
                onChange={handleChange}
                required
                min="0"
                placeholder="0"
              />
            </div>
          </div>

          <div className="info-box">
            <p>
              <strong>Precio Actual:</strong> ₡{Number(producto.precio_producto).toLocaleString('es-CR')}
            </p>
            <p>
              <strong>Stock Actual:</strong> {producto.stock_producto} unidades
            </p>
            <p className={`stock-status ${producto.stock_producto === 0 ? 'agotado' : producto.stock_producto < 10 ? 'bajo' : 'normal'}`}>
              {producto.stock_producto === 0 ? '🔴 Agotado' : producto.stock_producto < 10 ? '🟡 Stock Bajo' : '🟢 Stock Normal'}
            </p>
          </div>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="form-actions">
          <button
            type="button"
            onClick={handleCancelar}
            className="btn-cancelar"
            disabled={saving}
          >
            Cancelar
          </button>
          <button
            type="submit"
            className="btn-guardar"
            disabled={saving}
          >
            {saving ? 'Guardando...' : '✅ Guardar Cambios'}
          </button>
        </div>
      </form>

      {toastVisible && <div className="toast-notification">{toastMessage}</div>}
    </div>
  )
}

export default EditProduct
