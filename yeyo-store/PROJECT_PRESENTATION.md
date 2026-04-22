# YeYo Store - Project Presentation

## 1. Executive Summary
YeYo Store is a full-stack e-commerce platform specialized in footwear sales, built with a modern architecture focused on scalability, maintainability, and user experience.

The project includes:
- Customer and admin role-based access
- Product catalog with sizes, filters, and images
- Shopping cart and checkout flow
- Wishlist system
- Order tracking interface
- Inventory and product management for admins
- JWT authentication and protected endpoints
- Production-ready deployment configuration

## 2. Problem
Traditional small-store workflows usually face these issues:
- Fragmented inventory updates
- Lack of visibility on order status
- No personalization for users
- Limited internal control for business owners

## 3. Solution
YeYo Store centralizes the complete online sales process in one platform:
- Customers browse products, save favorites, add to cart, and place orders
- Admins control stock and product data from a dedicated interface
- Orders can be tracked with a clear status timeline
- Authentication and role-based permissions secure the workflow

## 4. Core Features
### Customer Features
- User registration and login
- Product browsing with filters
- Product images and details
- Cart with quantity and size handling
- Coupon field at checkout
- Order history and order detail page
- Wishlist management

### Admin Features
- Admin-only protected routes
- Inventory dashboard
- Product editing form
- Quick stock actions
- Role-aware navigation menu

## 5. Technical Architecture
### Frontend
- React 18
- Vite
- React Router
- Context API for auth and state sharing

### Backend
- FastAPI
- SQLModel / SQLAlchemy
- PostgreSQL (Supabase)
- JWT authentication

### Deployment
- Dockerized backend and frontend services
- Render-ready configuration
- Environment-driven API URLs for production

## 6. Security and Access Control
- Password hashing and token-based authentication
- Access and refresh token flow
- Role included in JWT payload
- Backend role enforcement on admin endpoints
- Frontend route protection and conditional menu rendering

## 7. Data Model Highlights
The domain includes key entities for commerce:
- Users and addresses
- Products, sizes, and product images
- Orders and order details
- Wishlist
- Coupons
- Shipping and tracking states

## 8. User Experience Highlights
- Dark, modern UI aligned with a sports/shoes brand identity
- Responsive layouts for desktop and mobile
- Clear visual feedback (toasts, badges, statuses)
- Timeline-style order tracking view

## 9. Deployment Readiness
The project is prepared for cloud deployment:
- Dockerfiles per service
- .dockerignore files
- Compose orchestration for local development
- Environment variable strategy for staging and production
- Frontend configured to consume dynamic API base URL

## 10. Business Value
YeYo Store provides:
- Better purchase flow for customers
- Better operational control for admins
- Reduced manual inventory friction
- Scalable base for future payment and logistics integrations

## 11. Future Roadmap
- Real-time shipping provider integration
- Stripe payment integration
- Admin analytics dashboard
- Product recommendation engine
- Notification system (email / push)

## 12. Conclusion
YeYo Store demonstrates a complete full-stack commerce implementation with production-oriented decisions in architecture, security, and deployment. It is positioned as a strong foundation for a real footwear retail operation.
