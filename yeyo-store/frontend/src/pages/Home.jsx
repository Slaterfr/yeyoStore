import { Link } from 'react-router-dom'
import './Home.css'

const Home = () => {
  return (
    <div className="home">
      <div className="hero">
        <h1>Bienvenido a YeYo Store</h1>
        <p>Los mejores zapatos con envío rápido</p>
        <Link to="/productos" className="cta-btn">
          Ver catálogo
        </Link>
      </div>

      <div className="features">
        <div className="feature-card">
          <h3>Envio rapido</h3>
          <p>Entrega en 24-48 horas</p>
        </div>
        <div className="feature-card">
          <h3>Seguro</h3>
          <p>Compras 100% protegidas</p>
        </div>
        <div className="feature-card">
          <h3>Calidad</h3>
          <p>Productos verificados</p>
        </div>
      </div>
    </div>
  )
}

export default Home
