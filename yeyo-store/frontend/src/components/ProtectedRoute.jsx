import React from 'react'
import { useAuth } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'
import './ProtectedRoute.css'

/**
 * ProtectedRoute - Componente para proteger rutas por rol
 * 
 * Uso:
 * <ProtectedRoute requiredRole="admin">
 *   <AdminPage />
 * </ProtectedRoute>
 */
const ProtectedRoute = ({ children, requiredRole = 'admin' }) => {
  const { isAuthenticated, loading, hasRole, rol } = useAuth()
  const navigate = useNavigate()

  if (loading) {
    return (
      <div className="protected-route-loading">
        <p>Cargando...</p>
      </div>
    )
  }

  if (!isAuthenticated) {
    return (
      <div className="protected-route-container">
        <div className="error-box">
          <h2>Acceso Denegado</h2>
          <p>Debes estar autenticado para acceder a esta página.</p>
          <button onClick={() => navigate('/login')} className="btn-primary">
            Ir a Login
          </button>
        </div>
      </div>
    )
  }

  if (!hasRole(requiredRole)) {
    return (
      <div className="protected-route-container">
        <div className="error-box">
          <h2>No Autorizado</h2>
          <p>Se requiere rol <strong>{requiredRole}</strong> para acceder a esta página.</p>
          <p>Tu rol actual: <strong>{rol}</strong></p>
          <button onClick={() => navigate('/')} className="btn-primary">
            Volver al Inicio
          </button>
        </div>
      </div>
    )
  }

  return children
}

export default ProtectedRoute
