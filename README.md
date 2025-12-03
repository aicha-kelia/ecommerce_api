# E-Commerce API - ALX Capstone Project

A RESTful backend API for an e-commerce platform with product management, order tracking, customer reviews, and authentication.

## 🚀 Features

- Product Management with categories, filtering, and search
- Customer Management with order history
- Order Processing with status tracking
- Product Reviews with 1-5 star ratings
- Token-based Authentication
- Role-based Permissions (Admin vs Regular Users)
- Low Stock Alerts
- Automatic Inventory Management

## 🛠️ Tech Stack

- Django 4.x
- Django REST Framework
- PostgreSQL
- Token Authentication

## 📋 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and get token
- `POST /api/auth/logout/` - Logout

### Products
- `GET /api/products/` - List all products
- `POST /api/products/` - Create product (Admin only)
- `GET /api/products/{id}/` - Get product details
- `GET /api/products/low_stock/` - Low stock alerts

### Customers
- `GET /api/customers/` - List customers
- `GET /api/customers/{id}/orders/` - Customer order history

### Orders
- `GET /api/orders/` - List orders
- `POST /api/orders/` - Create order
- `PATCH /api/orders/{id}/update_status/` - Update status (Admin only)

### Reviews
- `GET /api/reviews/` - List reviews
- `POST /api/reviews/` - Create review

## 🔧 Installation
```bash
git clone https://github.com/aicha-kelia/ecommerce_api.git
cd ecommerce_api

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 👨‍💻 Author

Aicha Kelia - ALX Software Engineering Capstone Project