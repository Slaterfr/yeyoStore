import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './Navigation.css'

const Navigation = () => {
  const { user, logout, isAuthenticated, isAdmin } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          YeYo Store
        </Link>

        <ul className="nav-menu">
          <li className="nav-item">
            <Link to="/productos" className="nav-link">
              Productos
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/wishlist" className="nav-link">
              Favoritos
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/carrito" className="nav-link">
              Carrito
            </Link>
          </li>

          {isAdmin && (
            <li className="nav-item admin-divider">
              <span className="divider">|</span>
            </li>
          )}

          {isAdmin && (
            <>
              <li className="nav-item admin-item">
                <Link to="/admin/inventario" className="nav-link admin-link">
                  Inventario
                </Link>
              </li>
            </>
          )}

          {isAuthenticated ? (
            <>
              <li className="nav-item">
                <Link to="/perfil" className="nav-link">
                  Mi cuenta
                </Link>
              </li>
              <li className="nav-item">
                <button className="nav-btn logout-btn" onClick={handleLogout}>
                  Salir
                </button>
              </li>
            </>
          ) : (
            <>
              <li className="nav-item">
                <Link to="/login" className="nav-link">
                  Iniciar sesion
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/register" className="nav-btn register-btn">
                  Registrarse
                </Link>
              </li>
            </>
          )}
        </ul>
      </div>
    </nav>
  )
}

export default Navigation
