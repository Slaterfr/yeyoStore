import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { Link } from 'react-router-dom'
import './Profile.css'

const Profile = () => {
  const { user, isAuthenticated, getAuthHeaders } = useAuth()
  const API_BASE = (import.meta.env.VITE_API_URL || 'http://localhost:8000')
    .replace(/\/$/, '')
    .replace(/\/api$/, '')
  const [tab, setTab] = useState('datos')
  const [userData, setUserData] = useState(null)
  const [pedidos, setPedidos] = useState([])
  const [direcciones, setDirecciones] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [isEditing, setIsEditing] = useState(false)
  const [editFormData, setEditFormData] = useState({ nombre_usuario: '', email_usuario: '' })
  const [isAddingAddress, setIsAddingAddress] = useState(false)
  const [newAddressData, setNewAddressData] = useState({
    provincia_direccion: '',
    canton_direccion: '',
    distrito_direccion: '',
    direccion_exacta_direccion: '',
    es_principal_direccion: false
  }) 

  useEffect(() => {
    if (isAuthenticated) {
      cargarDatosUsuario()
      cargarPedidos()
      cargarDirecciones()
    }
  }, [isAuthenticated])

  const cargarDatosUsuario = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/usuarios/me`, {
        headers: getAuthHeaders()
      })
      if (response.ok) {
        const data = await response.json()
        setUserData(data)
        setEditFormData({
          nombre_usuario: data.nombre_usuario,
          email_usuario: data.email_usuario
        })
      } else if (response.status === 403) {
        setError('Sesión inválida. Por favor, inicia sesión nuevamente.')
      }
    } catch (err) {
      setError('Error cargando datos del usuario: ' + err.message)
    }
  }

  const cargarPedidos = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE}/api/ordenes`, {
        headers: getAuthHeaders()
      })
      if (response.ok) {
        const data = await response.json()
        setPedidos(Array.isArray(data) ? data : data.ordenes || [])
      }
    } catch (err) {
      setError('Error cargando pedidos')
    } finally {
      setLoading(false)
    }
  }

  const guardarCambios = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/usuarios/me`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        },
        body: JSON.stringify(editFormData)
      })
      if (response.ok) {
        const data = await response.json()
        setUserData(data)
        setIsEditing(false)
        setError('')
      } else {
        setError('Error al actualizar los datos')
      }
    } catch (err) {
      setError('Error actualizando datos: ' + err.message)
    }
  }

  const cargarDirecciones = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/usuarios/me/direcciones`, {
        headers: getAuthHeaders()
      })
      if (response.ok) {
        const data = await response.json()
        setDirecciones(Array.isArray(data) ? data : [])
      }
    } catch (err) {
      console.error('Error cargando direcciones:', err)
    }
  }

  const agregarDireccion = async () => {
    if (!newAddressData.provincia_direccion || !newAddressData.canton_direccion ||
        !newAddressData.distrito_direccion || !newAddressData.direccion_exacta_direccion) {
      setError('Por favor completa todos los campos')
      return
    }

    try {
      const response = await fetch(`${API_BASE}/api/usuarios/me/direcciones`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        },
        body: JSON.stringify(newAddressData)
      })
      if (response.ok) {
        await cargarDirecciones()
        setNewAddressData({
          provincia_direccion: '',
          canton_direccion: '',
          distrito_direccion: '',
          direccion_exacta_direccion: '',
          es_principal_direccion: false
        })
        setIsAddingAddress(false)
        setError('')
      } else {
        setError('Error al agregar la dirección')
      }
    } catch (err) {
      setError('Error agregando dirección: ' + err.message)
    }
  }

  const eliminarDireccion = async (direccionId) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar esta dirección?')) {
      try {
        const response = await fetch(`${API_BASE}/api/usuarios/me/direcciones/${direccionId}`, {
          method: 'DELETE',
          headers: getAuthHeaders()
        })
        if (response.ok) {
          await cargarDirecciones()
          setError('')
        } else {
          setError('Error al eliminar la dirección')
        }
      } catch (err) {
        setError('Error eliminando dirección: ' + err.message)
      }
    }
  }

  if (!isAuthenticated) {
    return <div className="profile-welcome">Debes iniciar sesion para ver tu perfil</div>
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'entregado':
        return '#0ea5e9'
      case 'en_transito':
        return '#99ccff'
      case 'confirmado':
        return '#ffcc99'
      default:
        return '#999'
    }
  }

  const formatFecha = (fecha) => {
    if (!fecha) return '-'
    return new Date(fecha).toLocaleDateString('es-CR')
  }

  return (
    <div className="profile-container">
      {/* Sidebar */}
      <aside className="profile-sidebar">
        <div className="user-avatar">
          {userData?.nombre_usuario ? userData.nombre_usuario[0].toUpperCase() : 'U'}
        </div>
        <h3>{userData?.nombre_usuario || 'Usuario'}</h3>
        <p className="user-email">{userData?.email_usuario || ''}</p>

        <nav className="profile-menu">
          <button
            className={`menu-item ${tab === 'datos' ? 'active' : ''}`}
            onClick={() => setTab('datos')}
          >
            Mis datos
          </button>
          <button
            className={`menu-item ${tab === 'ordenes' ? 'active' : ''}`}
            onClick={() => setTab('ordenes')}
          >
            Historial de pedidos
          </button>
          <button
            className={`menu-item ${tab === 'direcciones' ? 'active' : ''}`}
            onClick={() => setTab('direcciones')}
          >
            Direcciones
          </button>
          <button
            className={`menu-item ${tab === 'contraseña' ? 'active' : ''}`}
            onClick={() => setTab('contraseña')}
          >
            Cambiar contraseña
          </button>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="profile-content">
        {error && <div className="error-message">{error}</div>}

        {/* Tab: Mis Datos */}
        {tab === 'datos' && (
          <section className="profile-section">
            <h2>Mis datos</h2>
            {!isEditing ? (
              <>
                <div className="data-grid">
                  <div className="data-item">
                    <label>Nombre de usuario:</label>
                    <p>{userData?.nombre_usuario || '-'}</p>
                  </div>
                  <div className="data-item">
                    <label>Email:</label>
                    <p>{userData?.email_usuario || '-'}</p>
                  </div>
                  <div className="data-item">
                    <label>Fecha de registro:</label>
                    <p>{userData?.fecha_registro_usuario ? formatFecha(userData.fecha_registro_usuario) : '-'}</p>
                  </div>
                  <div className="data-item">
                    <label>Estado de cuenta:</label>
                    <p className="status-badge" style={{ color: '#0ea5e9' }}>Activa</p>
                  </div>
                </div>
                <button className="edit-btn" onClick={() => setIsEditing(true)}>
                  Editar datos
                </button>
              </>
            ) : (
              <form className="edit-form" onSubmit={(e) => { e.preventDefault(); guardarCambios() }}>
                <div className="form-group">
                  <label>Nombre de usuario:</label>
                  <input
                    type="text"
                    value={editFormData.nombre_usuario}
                    onChange={(e) => setEditFormData({ ...editFormData, nombre_usuario: e.target.value })}
                    placeholder="Nombre de usuario"
                  />
                </div>
                <div className="form-group">
                  <label>Email:</label>
                  <input
                    type="email"
                    value={editFormData.email_usuario}
                    onChange={(e) => setEditFormData({ ...editFormData, email_usuario: e.target.value })}
                    placeholder="Email"
                  />
                </div>
                <div className="form-actions">
                  <button type="submit" className="submit-btn">
                    Guardar cambios
                  </button>
                  <button
                    type="button"
                    className="cancel-btn"
                    onClick={() => setIsEditing(false)}
                  >
                    Cancelar
                  </button>
                </div>
              </form>
            )}
          </section>
        )}

        {/* Tab: Historial de Pedidos */}
        {tab === 'ordenes' && (
          <section className="profile-section">
            <h2>Historial de pedidos</h2>
            {loading ? (
              <p className="loading">Cargando pedidos...</p>
            ) : pedidos.length === 0 ? (
              <p>No tienes pedidos aun</p>
            ) : (
              <div className="orders-list">
                {pedidos.map((pedido) => (
                  <div key={pedido.id_pedido} className="order-item">
                    <div className="order-header">
                      <h4>ORD-{String(pedido.id_pedido).padStart(4, '0')}</h4>
                      <span className="order-date">{formatFecha(pedido.fecha_pedido_pedido)}</span>
                      <span
                        className="order-status"
                        style={{ color: getStatusColor(pedido.estado_pedido_pedido) }}
                      >
                        {pedido.estado_pedido_pedido === 'entregado' ? 'Entregado' :
                         pedido.estado_pedido_pedido === 'en_transito' ? 'En camino' :
                         pedido.estado_pedido_pedido === 'confirmado' ? 'Confirmado' :
                         'Pendiente'}
                      </span>
                    </div>
                    <div className="order-body">
                      <p className="order-items">
                        {pedido.detalles?.length || 0} item(s)
                      </p>
                      <p className="order-total">
                        ₡{Number(pedido.monto_total_pedido).toLocaleString('es-CR')}
                      </p>
                    </div>
                    <Link to={`/orden/${pedido.id_pedido}`} className="order-details-btn">
                      Ver detalle
                    </Link>
                  </div>
                ))}
              </div>
            )}
          </section>
        )}

        {/* Tab: Direcciones */}
        {tab === 'direcciones' && (
          <section className="profile-section">
            <h2>Mis direcciones</h2>
            
            {direcciones.length === 0 ? (
              <p style={{ color: '#999', marginTop: '20px' }}>
                No tienes direcciones registradas
              </p>
            ) : (
              <div className="addresses-list">
                {direcciones.map((dir) => (
                  <div key={dir.id_direccion} className="address-item">
                    <div className="address-content">
                      <h4>{dir.provincia_direccion}, {dir.canton_direccion}</h4>
                      <p>{dir.direccion_exacta_direccion}</p>
                      <small>{dir.distrito_direccion}</small>
                      {dir.es_principal_direccion && (
                        <span className="principal-badge">Principal</span>
                      )}
                    </div>
                    <button
                      className="delete-btn"
                      onClick={() => eliminarDireccion(dir.id_direccion)}
                    >
                      Eliminar
                    </button>
                  </div>
                ))}
              </div>
            )}

            {!isAddingAddress ? (
              <button
                className="add-btn"
                style={{ marginTop: '20px' }}
                onClick={() => setIsAddingAddress(true)}
              >
                Agregar nueva dirección
              </button>
            ) : (
              <form className="add-address-form" onSubmit={(e) => { e.preventDefault(); agregarDireccion() }}>
                <div className="form-row">
                  <div className="form-group">
                    <label>Provincia:</label>
                    <input
                      type="text"
                      value={newAddressData.provincia_direccion}
                      onChange={(e) => setNewAddressData({ ...newAddressData, provincia_direccion: e.target.value })}
                      placeholder="Ej: San José"
                    />
                  </div>
                  <div className="form-group">
                    <label>Cantón:</label>
                    <input
                      type="text"
                      value={newAddressData.canton_direccion}
                      onChange={(e) => setNewAddressData({ ...newAddressData, canton_direccion: e.target.value })}
                      placeholder="Ej: San José"
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Distrito:</label>
                    <input
                      type="text"
                      value={newAddressData.distrito_direccion}
                      onChange={(e) => setNewAddressData({ ...newAddressData, distrito_direccion: e.target.value })}
                      placeholder="Ej: San José"
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label>Dirección exacta:</label>
                  <textarea
                    value={newAddressData.direccion_exacta_direccion}
                    onChange={(e) => setNewAddressData({ ...newAddressData, direccion_exacta_direccion: e.target.value })}
                    placeholder="Ej: Calle 5, Avenida 10, Edificio 25, Apartamento 301"
                    rows="3"
                  />
                </div>

                <div className="form-group checkbox">
                  <input
                    type="checkbox"
                    id="es_principal"
                    checked={newAddressData.es_principal_direccion}
                    onChange={(e) => setNewAddressData({ ...newAddressData, es_principal_direccion: e.target.checked })}
                  />
                  <label htmlFor="es_principal">Establecer como direccion principal</label>
                </div>

                <div className="form-actions">
                  <button type="submit" className="submit-btn">
                    Guardar dirección
                  </button>
                  <button
                    type="button"
                    className="cancel-btn"
                    onClick={() => setIsAddingAddress(false)}
                  >
                    Cancelar
                  </button>
                </div>
              </form>
            )}
          </section>
        )}

        {/* Tab: Cambiar Contraseña */}
        {tab === 'contraseña' && (
          <section className="profile-section">
            <h2>Cambiar contraseña</h2>
            <form className="password-form">
              <div className="form-group">
                <label>Contraseña actual:</label>
                <input type="password" placeholder="••••••••" />
              </div>
              <div className="form-group">
                <label>Nueva contraseña:</label>
                <input type="password" placeholder="••••••••" minLength="8" />
              </div>
              <div className="form-group">
                <label>Confirmar contraseña:</label>
                <input type="password" placeholder="••••••••" minLength="8" />
              </div>
              <button type="submit" className="submit-btn">
                Cambiar contraseña
              </button>
            </form>
          </section>
        )}
      </main>
    </div>
  )
}

export default Profile
