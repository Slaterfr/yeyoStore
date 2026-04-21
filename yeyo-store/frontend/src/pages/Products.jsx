import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { useCart } from '../context/CartContext'
import { useWishlist } from '../context/WishlistContext'
import './Products.css'

const Products = () => {
  const { getAuthHeaders } = useAuth()
  const { agregarAlCarrito } = useCart()
  const { wishlist, agregarAListaDeseos, eliminarDeListaDeseos, estaEnListaDeseos } = useWishlist()
  const [productos, setProductos] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [fotos, setFotos] = useState({}) // { producto_id: [fotos] }
  const [tallaSeleccionada, setTallaSeleccionada] = useState({}) // { producto_id: talla }
  const [toastMessage, setToastMessage] = useState('')
  const [toastVisible, setToastVisible] = useState(false)

  // Filtros
  const [searchTerm, setSearchTerm] = useState('')
  const [categoriaFilter, setCategoriaFilter] = useState('')
  const [precioMin, setPrecioMin] = useState(0)
  const [precioMax, setPrecioMax] = useState(500000)
  const [tallaFilter, setTallaFilter] = useState('')
  const [ordenar, setOrdenar] = useState('nombre')

  // Opciones disponibles
  const categorias = ['Tenis', 'Casual', 'Deportivo']
  const tallas = ['36', '37', '38', '39', '40', '41', '42', '43', '44', '45']

  // Cargar fotos de un producto
  const cargarFotosProducto = async (productoId) => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/productos/${productoId}/fotos`,
        {
          headers: getAuthHeaders()
        }
      )
      if (response.ok) {
        const data = await response.json()
        setFotos((prev) => ({
          ...prev,
          [productoId]: data.fotos || []
        }))
      }
    } catch (err) {
      console.error(`Error cargando fotos del producto ${productoId}:`, err)
    }
  }

  // Cargar productos
  const cargarProductos = async () => {
    setLoading(true)
    setError('')
    try {
      let url = 'http://localhost:8000/api/productos'
      const params = new URLSearchParams()

      if (searchTerm) params.append('q', searchTerm)
      if (categoriaFilter) params.append('categoria', categoriaFilter)
      if (precioMin) params.append('precio_min', precioMin)
      if (precioMax) params.append('precio_max', precioMax)
      if (tallaFilter) params.append('talla', tallaFilter)

      if (params.toString()) {
        url += '?' + params.toString()
      }

      const response = await fetch(url, {
        headers: getAuthHeaders()
      })

      if (!response.ok) throw new Error('Error cargando productos')

      const data = await response.json()
      let items = Array.isArray(data) ? data : data.items || []

      // Ordenar
      items.sort((a, b) => {
        switch (ordenar) {
          case 'nombre':
            return a.nombre_producto.localeCompare(b.nombre_producto)
          case 'precio_asc':
            return a.precio_producto - b.precio_producto
          case 'precio_desc':
            return b.precio_producto - a.precio_producto
          case 'calificacion':
            return b.promedio_calificacion_producto - a.promedio_calificacion_producto
          case 'vendidos':
            return b.stock_producto - a.stock_producto
          default:
            return 0
        }
      })

      setProductos(items)
      
      // Cargar fotos para cada producto
      items.forEach((producto) => {
        cargarFotosProducto(producto.id_producto)
      })
    } catch (err) {
      setError('Error al cargar productos: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  // Buscar cuando cambian filtros
  useEffect(() => {
    cargarProductos()
  }, [searchTerm, categoriaFilter, precioMin, precioMax, tallaFilter, ordenar])

  // Mostrar toast por 3 segundos
  const mostrarToast = (mensaje) => {
    setToastMessage(mensaje)
    setToastVisible(true)
    setTimeout(() => setToastVisible(false), 3000)
  }

  // Manejar toggle de lista de deseos
  const handleToggleWishlist = (producto) => {
    if (estaEnListaDeseos(producto.id_producto)) {
      eliminarDeListaDeseos(producto.id_producto)
      mostrarToast(`❌ ${producto.nombre_producto} eliminado de lista de deseos`)
    } else {
      agregarAListaDeseos({
        ...producto,
        imagen: fotos[producto.id_producto]?.[0]?.url_foto_producto || null
      })
      mostrarToast(`❤️ ${producto.nombre_producto} agregado a lista de deseos`)
    }
  }

  // Manejar agregar al carrito
  const handleAgregarAlCarrito = (producto) => {
    const talla = tallaSeleccionada[producto.id_producto]
    
    if (!talla) {
      mostrarToast('⚠️ Por favor selecciona una talla')
      return
    }

    // Agregar al carrito
    agregarAlCarrito(
      {
        ...producto,
        imagen: fotos[producto.id_producto]?.[0]?.url_foto_producto || null
      },
      talla
    )

    // Mostrar confirmación
    mostrarToast(`✅ ${producto.nombre_producto} (Talla ${talla}) agregado al carrito`)
    
    // Limpiar talla seleccionada
    setTallaSeleccionada((prev) => ({
      ...prev,
      [producto.id_producto]: ''
    }))
  }

  const limpiarFiltros = () => {
    setSearchTerm('')
    setCategoriaFilter('')
    setPrecioMin(0)
    setPrecioMax(500000)
    setTallaFilter('')
    setOrdenar('nombre')
  }

  return (
    <div className="products-container">
      {/* Sidebar Filtros */}
      <aside className="filters-sidebar">
        <h3>Filtros</h3>

        {/* Búsqueda */}
        <div className="filter-group">
          <label>Buscar:</label>
          <input
            type="text"
            placeholder="Nike, Adidas..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        {/* Categoría */}
        <div className="filter-group">
          <label>CATEGORIA</label>
          {categorias.map((cat) => (
            <label key={cat} className="checkbox-label">
              <input
                type="checkbox"
                checked={categoriaFilter === cat}
                onChange={(e) => setCategoriaFilter(e.target.checked ? cat : '')}
              />
              <span>{cat}</span>
            </label>
          ))}
        </div>

        {/* Precio */}
        <div className="filter-group">
          <label>PRECIO (COLONES)</label>
          <div className="price-inputs">
            <input
              type="number"
              value={precioMin}
              onChange={(e) => setPrecioMin(Number(e.target.value))}
              placeholder="Min"
            />
            <span>-</span>
            <input
              type="number"
              value={precioMax}
              onChange={(e) => setPrecioMax(Number(e.target.value))}
              placeholder="Max"
            />
          </div>
        </div>

        {/* Talla */}
        <div className="filter-group">
          <label>TALLA DISPONIBLE</label>
          <div className="talla-grid">
            {tallas.map((talla) => (
              <button
                key={talla}
                className={`talla-btn ${tallaFilter === talla ? 'active' : ''}`}
                onClick={() => setTallaFilter(tallaFilter === talla ? '' : talla)}
              >
                {talla}
              </button>
            ))}
          </div>
        </div>

        {/* Ordenar */}
        <div className="filter-group">
          <label>ORDENAR POR</label>
          <select value={ordenar} onChange={(e) => setOrdenar(e.target.value)}>
            <option value="nombre">Nombre</option>
            <option value="precio_asc">Precio menor</option>
            <option value="precio_desc">Precio mayor</option>
            <option value="calificacion">Mas vendido</option>
          </select>
        </div>

        {/* Limpiar */}
        <button className="clear-filters-btn" onClick={limpiarFiltros}>
          Limpiar filtros
        </button>
      </aside>

      {/* Main Content */}
      <main className="products-content">
        <div className="search-bar">
          <input
            type="text"
            placeholder="Buscar productos..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="main-search"
          />
          <button className="search-btn">Buscar</button>
        </div>

        {error && <div className="error-message">{error}</div>}

        {loading ? (
          <div className="loading">Cargando productos...</div>
        ) : (
          <>
            <p className="results-count">{productos.length} resultados encontrados</p>
            <div className="products-grid">
              {productos.map((producto) => {
                const imagenPrincipal = fotos[producto.id_producto]?.find(
                  (foto) => foto.es_principal_foto_producto
                ) || fotos[producto.id_producto]?.[0]
                
                return (
                  <div key={producto.id_producto} className="product-card">
                    <div className="product-image">
                      <img 
                        src={imagenPrincipal?.url_foto_producto || "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Crect fill='%23333' width='300' height='300'/%3E%3Ctext x='50%25' y='50%25' font-size='18' fill='%23666' text-anchor='middle' dy='.3em'%3Eimagen%3C/text%3E%3C/svg%3E"} 
                        alt={producto.nombre_producto}
                        onError={(e) => {
                          e.target.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Crect fill='%23333' width='300' height='300'/%3E%3C/svg%3E"
                        }}
                      />
                    </div>
                    <div className="product-info">
                      <h4>{producto.nombre_producto}</h4>
                      <p className="category">{producto.categoria_producto}</p>
                      <p className="brand">{producto.marca_producto}</p>
                      <p className="price">₡{Number(producto.precio_producto).toLocaleString('es-CR')}</p>
                      
                      {/* Selector de talla */}
                      <div className="talla-selector">
                        <label>Talla:</label>
                        <select 
                          value={tallaSeleccionada[producto.id_producto] || ''}
                          onChange={(e) => setTallaSeleccionada({
                            ...tallaSeleccionada,
                            [producto.id_producto]: e.target.value
                          })}
                          className="talla-select"
                        >
                          <option value="">Selecciona una talla</option>
                          {tallas.map((talla) => (
                            <option key={talla} value={talla}>
                              {talla}
                            </option>
                          ))}
                        </select>
                      </div>
                      
                      <div className="product-buttons">
                        <button 
                          className="add-to-cart-btn"
                          onClick={() => handleAgregarAlCarrito(producto)}
                        >
                          Agregar al carrito
                        </button>
                        <button 
                          className={`wishlist-btn ${estaEnListaDeseos(producto.id_producto) ? 'active' : ''}`}
                          onClick={() => handleToggleWishlist(producto)}
                          title="Agregar a lista de deseos"
                        >
                          {estaEnListaDeseos(producto.id_producto) ? '❤️' : '🤍'}
                        </button>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          </>
        )}

        {/* Toast notification */}
        {toastVisible && (
          <div className="toast-notification">
            {toastMessage}
          </div>
        )}
      </main>
    </div>
  )
}

export default Products
