import { Link, useLocation, useParams } from 'react-router-dom'
import './PaymentConfirmation.css'

const PaymentConfirmation = () => {
  const { orderId } = useParams()
  const location = useLocation()

  const pago = location.state?.pago || {}

  const metodoLabel = pago.metodo || 'Tarjeta registrada'
  const montoTotal = pago.total || null

  return (
    <div className="payment-confirmation-container">
      <div className="payment-confirmation-card">
        <div className="confirmation-icon">Pago</div>
        <h1>Pago confirmado</h1>
        <p className="confirmation-subtitle">
          Tu compra fue procesada correctamente.
        </p>

        <div className="confirmation-summary">
          <div className="summary-row">
            <span>Orden:</span>
            <strong>#{orderId}</strong>
          </div>
          <div className="summary-row">
            <span>Metodo de pago:</span>
            <strong>{metodoLabel}</strong>
          </div>
          {montoTotal !== null && (
            <div className="summary-row">
              <span>Total pagado:</span>
              <strong>CRC {Number(montoTotal).toLocaleString('es-CR')}</strong>
            </div>
          )}
          <div className="summary-row status-row">
            <span>Estado:</span>
            <strong>Confirmado</strong>
          </div>
        </div>

        <div className="confirmation-actions">
          <Link to={`/orden/${orderId}`} className="btn-primary">
            Ver seguimiento
          </Link>
          <Link to="/productos" className="btn-secondary">
            Seguir comprando
          </Link>
        </div>
      </div>
    </div>
  )
}

export default PaymentConfirmation
