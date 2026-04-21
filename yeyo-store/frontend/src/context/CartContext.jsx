import { createContext, useContext, useState, useEffect, useCallback } from 'react'

const CartContext = createContext()

// Función para inicializar el carrito desde localStorage
const initializeCart = () => {
  try {
    const carritoGuardado = localStorage.getItem('carrito')
    return carritoGuardado ? JSON.parse(carritoGuardado) : []
  } catch (err) {
    console.error('Error al inicializar carrito:', err)
    return []
  }
}

export const CartProvider = ({ children }) => {
  const [carrito, setCarrito] = useState(initializeCart)

  // IMPORTANTE: Guardar carrito en localStorage SIEMPRE que cambia
  useEffect(() => {
    if (carrito.length > 0 || localStorage.getItem('carrito')) {
      localStorage.setItem('carrito', JSON.stringify(carrito))
    }
  }, [carrito])

  // Agregar producto al carrito (useCallback para evitar recreación)
  const agregarAlCarrito = useCallback((producto, talla) => {
    setCarrito((carritoActual) => {
      const itemExistente = carritoActual.find(
        (item) => item.id_producto === producto.id_producto && item.talla === talla
      )

      if (itemExistente) {
        // Si ya existe, aumentar cantidad
        return carritoActual.map((item) =>
          item.id_producto === producto.id_producto && item.talla === talla
            ? { ...item, cantidad: item.cantidad + 1 }
            : item
        )
      } else {
        // Si no existe, agregar nuevo item
        return [
          ...carritoActual,
          {
            id_producto: producto.id_producto,
            nombre_producto: producto.nombre_producto,
            precio_producto: producto.precio_producto,
            talla,
            cantidad: 1,
            imagen: producto.imagen,
          },
        ]
      }
    })
  }, [])

  // Eliminar producto del carrito
  const eliminarDelCarrito = useCallback((id_producto, talla) => {
    setCarrito((carritoActual) =>
      carritoActual.filter(
        (item) => !(item.id_producto === id_producto && item.talla === talla)
      )
    )
  }, [])

  // Actualizar cantidad
  const actualizarCantidad = useCallback((id_producto, talla, cantidad) => {
    if (cantidad <= 0) {
      eliminarDelCarrito(id_producto, talla)
    } else {
      setCarrito((carritoActual) =>
        carritoActual.map((item) =>
          item.id_producto === id_producto && item.talla === talla
            ? { ...item, cantidad }
            : item
        )
      )
    }
  }, [eliminarDelCarrito])

  // Vaciar carrito
  const vaciarCarrito = useCallback(() => {
    setCarrito([])
    localStorage.removeItem('carrito')
  }, [])

  // Calcular total
  const calcularTotal = useCallback(() => {
    return carrito.reduce(
      (total, item) => total + item.precio_producto * item.cantidad,
      0
    )
  }, [carrito])

  const valor = {
    carrito,
    agregarAlCarrito,
    eliminarDelCarrito,
    actualizarCantidad,
    vaciarCarrito,
    calcularTotal,
  }

  return <CartContext.Provider value={valor}>{children}</CartContext.Provider>
}

export const useCart = () => {
  const contexto = useContext(CartContext)
  if (!contexto) {
    throw new Error('useCart debe usarse dentro de CartProvider')
  }
  return contexto
}
