import { createContext, useContext, useState, useEffect } from 'react'

const WishlistContext = createContext()

export const WishlistProvider = ({ children }) => {
  const [wishlist, setWishlist] = useState([])

  // Cargar wishlist desde localStorage al iniciar
  useEffect(() => {
    const wishlistGuardada = localStorage.getItem('wishlist')
    if (wishlistGuardada) {
      try {
        setWishlist(JSON.parse(wishlistGuardada))
      } catch (err) {
        console.error('Error al cargar wishlist:', err)
      }
    }
  }, [])

  // Guardar wishlist en localStorage cada vez que cambia
  useEffect(() => {
    localStorage.setItem('wishlist', JSON.stringify(wishlist))
  }, [wishlist])

  // Agregar producto a la lista de deseos
  const agregarAListaDeseos = (producto) => {
    const productoExistente = wishlist.find(
      (item) => item.id_producto === producto.id_producto
    )

    if (!productoExistente) {
      setWishlist([
        ...wishlist,
        {
          id_producto: producto.id_producto,
          nombre_producto: producto.nombre_producto,
          precio_producto: producto.precio_producto,
          categoria_producto: producto.categoria_producto,
          marca_producto: producto.marca_producto,
          imagen: producto.imagen,
          fecha_agregado: new Date().toISOString(),
        },
      ])
    }
  }

  // Eliminar producto de la lista de deseos
  const eliminarDeListaDeseos = (id_producto) => {
    setWishlist(
      wishlist.filter((item) => item.id_producto !== id_producto)
    )
  }

  // Verificar si un producto está en la lista de deseos
  const estaEnListaDeseos = (id_producto) => {
    return wishlist.some((item) => item.id_producto === id_producto)
  }

  // Vaciar lista de deseos
  const vaciarListaDeseos = () => {
    setWishlist([])
  }

  const valor = {
    wishlist,
    agregarAListaDeseos,
    eliminarDeListaDeseos,
    estaEnListaDeseos,
    vaciarListaDeseos,
  }

  return (
    <WishlistContext.Provider value={valor}>
      {children}
    </WishlistContext.Provider>
  )
}

export const useWishlist = () => {
  const contexto = useContext(WishlistContext)
  if (!contexto) {
    throw new Error('useWishlist debe usarse dentro de WishlistProvider')
  }
  return contexto
}
