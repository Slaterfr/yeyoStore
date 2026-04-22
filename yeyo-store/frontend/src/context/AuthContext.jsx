import React, { createContext, useState, useCallback, useEffect } from 'react'
import axios from 'axios'

const AuthContext = createContext(null)

// Función para decodificar JWT y extraer el rol
const decodeToken = (token) => {
  try {
    const parts = token.split('.')
    if (parts.length !== 3) return null
    
    const decoded = JSON.parse(atob(parts[1]))
    return {
      user_id: parseInt(decoded.sub),
      rol: decoded.rol || 'cliente'
    }
  } catch (err) {
    console.error('Error decodificando token:', err)
    return null
  }
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [accessToken, setAccessToken] = useState(null)
  const [rol, setRol] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000')
    .replace(/\/$/, '')
    .replace(/\/api$/, '')
  const API_BASE = `${API_URL}/api`

  // Recuperar token de localStorage al montar el componente
  useEffect(() => {
    const token = localStorage.getItem('accessToken')
    if (token) {
      setAccessToken(token)
      // Extraer rol del token
      const tokenData = decodeToken(token)
      if (tokenData) {
        setRol(tokenData.rol)
      }
      // Intentar obtener info del usuario para verificar token válido
      verifyToken(token)
    } else {
      setLoading(false)
    }
  }, [])

  // Verificar si el token es válido
  const verifyToken = async (token) => {
    try {
      const response = await axios.get(`${API_BASE}/usuarios/me`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setUser(response.data)
      setLoading(false)
    } catch (err) {
      // Token inválido o expirado
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      setAccessToken(null)
      setUser(null)
      setRol(null)
      setLoading(false)
    }
  }

  // Registrar usuario
  const register = useCallback(async (nombre, email, password) => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.post(`${API_BASE}/auth/register`, {
        nombre_usuario: nombre,
        email_usuario: email,
        password_usuario: password
      })
      const { access_token, refresh_token } = response.data
      setAccessToken(access_token)
      
      // Extraer rol del token
      const tokenData = decodeToken(access_token)
      if (tokenData) {
        setRol(tokenData.rol)
      }
      
      setUser({ nombre, email })
      localStorage.setItem('accessToken', access_token)
      localStorage.setItem('refreshToken', refresh_token)
      return response.data
    } catch (err) {
      const message = err.response?.data?.detail || 'Error en el registro'
      setError(message)
      throw new Error(message)
    } finally {
      setLoading(false)
    }
  }, [])

  // Iniciar sesión
  const login = useCallback(async (email, password) => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.post(`${API_BASE}/auth/login`, {
        email_usuario: email,
        password_usuario: password
      })
      const { access_token, refresh_token } = response.data
      setAccessToken(access_token)
      
      // Extraer rol del token
      const tokenData = decodeToken(access_token)
      if (tokenData) {
        setRol(tokenData.rol)
      }
      
      localStorage.setItem('accessToken', access_token)
      localStorage.setItem('refreshToken', refresh_token)
      // Recuperar info del usuario
      const userResponse = await axios.get(`${API_BASE}/usuarios/me`, {
        headers: { Authorization: `Bearer ${access_token}` }
      })
      setUser(userResponse.data)
      return response.data
    } catch (err) {
      const message = err.response?.data?.detail || 'Error en el login'
      setError(message)
      throw new Error(message)
    } finally {
      setLoading(false)
    }
  }, [])

  // Cerrar sesión
  const logout = useCallback(() => {
    setUser(null)
    setAccessToken(null)
    setRol(null)
    setError(null)
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
  }, [])

  // Obtener headers con token (para fetch API)
  const getAuthHeaders = () => {
    if (!accessToken) {
      return {}
    }
    return {
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    }
  }

  // Verificar si el usuario tiene un rol específico
  const hasRole = useCallback((requiredRole) => {
    return rol === requiredRole
  }, [rol])

  // Verificar si el usuario tiene alguno de varios roles
  const hasAnyRole = useCallback((requiredRoles) => {
    return Array.isArray(requiredRoles) ? requiredRoles.includes(rol) : rol === requiredRoles
  }, [rol])

  return (
    <AuthContext.Provider
      value={{
        user,
        accessToken,
        rol,
        loading,
        error,
        register,
        login,
        logout,
        getAuthHeaders,
        hasRole,
        hasAnyRole,
        isAuthenticated: !!accessToken,
        isAdmin: rol === 'admin'
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = React.useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth debe ser usado dentro de AuthProvider')
  }
  return context
}

export default AuthContext
