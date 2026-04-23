import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { AuthProvider } from './context/AuthContext'
import { CartProvider } from './context/CartContext'
import { WishlistProvider } from './context/WishlistContext'
import Navigation from './components/Navigation'
import ProtectedRoute from './components/ProtectedRoute'
import Home from './pages/Home'
import Products from './pages/Products'
import ProductDetail from './pages/ProductDetail'
import Login from './pages/Login'
import Register from './pages/Register'
import Wishlist from './pages/Wishlist'
import Cart from './pages/Cart'
import Profile from './pages/Profile'
import OrderDetail from './pages/OrderDetail'
import PaymentConfirmation from './pages/PaymentConfirmation'
import Inventario from './pages/admin/Inventario'
import EditProduct from './pages/admin/EditProduct'
import './App.css'

function App() {
  const [theme, setTheme] = useState('light')

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme === 'dark' || savedTheme === 'light') {
      setTheme(savedTheme)
      return
    }

    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
    setTheme(prefersDark ? 'dark' : 'light')
  }, [])

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('theme', theme)
  }, [theme])

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'))
  }

  return (
    <AuthProvider>
      <CartProvider>
        <WishlistProvider>
          <Router>
            <Navigation theme={theme} onToggleTheme={toggleTheme} />
            <main className="main-content">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/productos" element={<Products />} />
                <Route path="/productos/:id" element={<ProductDetail />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/wishlist" element={<Wishlist />} />
                <Route path="/carrito" element={<Cart />} />
                <Route path="/perfil" element={<Profile />} />
                <Route path="/orden/:id" element={<OrderDetail />} />
                <Route path="/pago/confirmacion/:orderId" element={<PaymentConfirmation />} />
                
                {/* Admin Routes */}
                <Route 
                  path="/admin/inventario" 
                  element={
                    <ProtectedRoute requiredRole="admin">
                      <Inventario />
                    </ProtectedRoute>
                  } 
                />
                <Route 
                  path="/admin/productos/:id/editar" 
                  element={
                    <ProtectedRoute requiredRole="admin">
                      <EditProduct />
                    </ProtectedRoute>
                  } 
                />
              </Routes>
            </main>
          </Router>
        </WishlistProvider>
      </CartProvider>
    </AuthProvider>
  )
}

export default App
