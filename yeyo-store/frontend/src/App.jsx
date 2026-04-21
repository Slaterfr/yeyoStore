import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
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
import Inventario from './pages/admin/Inventario'
import EditProduct from './pages/admin/EditProduct'
import './App.css'

function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <WishlistProvider>
          <Router>
            <Navigation />
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
