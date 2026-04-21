import { useState } from 'react'
import { useWishlist } from '../context/WishlistContext'
import { useCart } from '../context/CartContext'
import './Wishlist.css'

const Wishlist = () => {
  const { wishlist, eliminarDeListaDeseos, vaciarListaDeseos } = useWishlist()
  const { agregarAlCarrito } = useCart()
  const [toastMessage, setToastMessage] = useState('')
  const [toastVisible, setToastVisible] = useState(false)
  const [tallaSeleccionada, setTallaSeleccionada] = useState({})

  const tallas = ['36', '37', '38', '39', '40', '41', '42', '43', '44', '45']

  const mostrarToast = (mensaje) => {
    setToastMessage(mensaje)
    setToastVisible(true)
    setTimeout(() => setToastVisible(false), 3000)
  }

  const handleAgregarAlCarrito = (producto) => {
    const talla = tallaSeleccionada[producto.id_producto]
    
    if (!talla) {
      mostrarToast('⚠️ Por favor selecciona una talla')
      return
    }

    agregarAlCarrito(producto, talla)
    mostrarToast(`✅ ${producto.nombre_producto} (Talla ${talla}) agregado al carrito`)
    
    setTallaSeleccionada((prev) => ({
      ...prev,
      [producto.id_producto]: ''
    }))
  }

  const handleEliminar = (id_producto) => {
    eliminarDeListaDeseos(id_producto)
    mostrarToast('❌ Producto eliminado de lista de deseos')
  }

  return (
    <div className="wishlist-container">
      <h1>Mi Lista de Deseos</h1>

      {toastVisible && (
        <div className="toast-notification">
          {toastMessage}
        </div>
      )}

      {wishlist.length === 0 ? (
        <div className="empty-wishlist">
          <p>Tu lista de deseos está vacía</p>
          <a href="/productos" className="btn-continue">Ir a Productos</a>
        </div>
      ) : (
        <>
          <div className="wishlist-header">
            <p className="items-count">{wishlist.length} producto{wishlist.length !== 1 ? 's' : ''} en tu lista</p>
            <button className="btn-clear-all" onClick={vaciarListaDeseos}>
              Vaciar lista
            </button>
          </div>

          <div className="wishlist-grid">
            {wishlist.map((producto) => (
              <div key={producto.id_producto} className="wishlist-card">
                <div className="card-image">
                  {producto.imagen && (
                    <img src={producto.imagen} alt={producto.nombre_producto} />
                  )}
                </div>

                <div className="card-content">
                  <h3>{producto.nombre_producto}</h3>
                  <p className="marca">{producto.marca_producto}</p>
                  <p className="categoria">{producto.categoria_producto}</p>
                  <p className="precio">₡{Number(producto.precio_producto).toLocaleString('es-CR')}</p>

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

                  <div className="card-buttons">
                    <button 
                      className="btn-add-cart"
                      onClick={() => handleAgregarAlCarrito(producto)}
                    >
                      Agregar al carrito
                    </button>
                    <button 
                      className="btn-remove"
                      onClick={() => handleEliminar(producto.id_producto)}
                    >
                      Eliminar
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}

export default Wishlist
