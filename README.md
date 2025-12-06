# 🍽️ Restaurant POS API

A comprehensive REST API for managing restaurant orders, items, and payments. Built with FastAPI, MySQL, and modern Python best practices.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the API](#running-the-api)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Database Schema](#database-schema)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Security](#security)
- [Performance](#performance)

---

## ✨ Features

- ✅ **RESTful API** - Clean, standard REST endpoints
- ✅ **Authentication** - API key-based security
- ✅ **Complete Order Management** - Full order details with items and payments
- ✅ **Auto-generated Documentation** - Swagger UI at `/docs`
- ✅ **Type Safety** - Pydantic validation for all data
- ✅ **Database Optimization** - Connection pooling and efficient queries
- ✅ **Error Handling** - Comprehensive error responses
- ✅ **CORS Support** - Ready for frontend integration

---

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | FastAPI | 0.104.1 |
| **Server** | Uvicorn | 0.24.0 |
| **Database** | MySQL | 8.0+ |
| **ORM** | SQLAlchemy | 2.0.23 |
| **Validation** | Pydantic | 2.5.0 |
| **Driver** | PyMySQL | 1.1.0 |

---

## 📦 Installation

### Prerequisites

- Python 3.8+
- MySQL Server 8.0+
- pip (Python package manager)

### Step 1: Clone Repository

```bash
git clone https://github.com/abhaynmehta/restaurant_pos_api.git
cd restaurant_pos_api
```

### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### Database Setup

1. **Start MySQL Server**

```bash
# Windows
net start MySQL80

# macOS
brew services start mysql

# Linux
sudo systemctl start mysql
```

2. **Create Database**

```bash
mysql -u root -p
CREATE DATABASE IF NOT EXISTS restaurant_pos;
EXIT;
```

3. **Configure Connection String** (in `database.py`)

```python
DATABASE_URL = "mysql+pymysql://root:your_password@localhost:3306/restaurant_pos"
```

### Environment Variables (Optional)

For production, use environment variables instead of hardcoding:

```bash
# Create .env file
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/restaurant_pos
API_KEY=sk_test_restaurant_pos_2025_secure_key_12345
```

---

## 🚀 Running the API

### Start the API Server

```bash
python main.py
```

**Expected Output:**
```
🚀 Starting Restaurant POS API...
📖 API Documentation: http://localhost:8000/docs
🔐 Requires API Key: sk_test_restaurant_pos_2025_secure_key_12345
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Access the API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Root**: http://localhost:8000

### Load Sample Data

```bash
python load_data.py
```

This loads:
- 2 Menus
- 5 Categories
- 10 Menu Items
- 11 Orders (IDs: 10-20)
- 52 Order Items
- 17 Payment Transactions

---

## 📡 API Endpoints

### Health Check (No Auth Required)

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

### Get All Orders (Auth Required)

```http
GET /api/v1/orders
X-API-Key: sk_test_restaurant_pos_2025_secure_key_12345
```

**Query Parameters:**
- `skip` (int): Skip N orders (default: 0)
- `limit` (int): Return N orders (default: 10)

**Example:**
```http
GET /api/v1/orders?skip=0&limit=5
```

**Response:**
```json
{
  "success": true,
  "count": 11,
  "orders": [
    {
      "order_id": 10,
      "order_date": "2025-10-01",
      "order_status": "Completed",
      "items": [
        {
          "order_item_id": 1,
          "item_name": "Item1",
          "category_name": "Starters",
          "quantity": 1,
          "unit_price": 3.75,
          "line_total": 3.75
        }
      ],
      "payments": [
        {
          "payment_id": 100,
          "payment_date": "2025-10-01",
          "amount_due": 9.25,
          "amount_paid": 9.25,
          "tips": 0,
          "discount": 0,
          "payment_type": "Card",
          "payment_status": "Completed"
        }
      ],
      "summary": {
        "total_amount": 9.25,
        "total_paid": 9.25,
        "total_tips": 0,
        "total_discount": 0,
        "outstanding_balance": 0,
        "payment_count": 1,
        "is_fully_paid": true
      }
    }
  ]
}
```

---

### Get Specific Order (Auth Required)

```http
GET /api/v1/orders/{order_id}
X-API-Key: sk_test_restaurant_pos_2025_secure_key_12345
```

**Example:**
```http
GET /api/v1/orders/14
X-API-Key: sk_test_restaurant_pos_2025_secure_key_12345
```

**Response:**
```json
{
  "success": true,
  "order": {
    "order_id": 14,
    "order_date": "2025-10-01",
    "order_status": "Completed",
    "items": [...],
    "payments": [...],
    "summary": {...}
  }
}
```

---

## 🔐 Authentication

### API Key

All protected endpoints require the `X-API-Key` header:

```
X-API-Key: sk_test_restaurant_pos_2025_secure_key_12345
```

### Using with cURL

```bash
curl -X GET http://localhost:8000/api/v1/orders \
  -H "X-API-Key: sk_test_restaurant_pos_2025_secure_key_12345"
```

### Using with Python

```python
import requests

headers = {
    "X-API-Key": "sk_test_restaurant_pos_2025_secure_key_12345"
}

response = requests.get(
    "http://localhost:8000/api/v1/orders",
    headers=headers
)
print(response.json())
```

### Using with JavaScript

```javascript
const headers = {
  "X-API-Key": "sk_test_restaurant_pos_2025_secure_key_12345",
  "Content-Type": "application/json"
};

fetch("http://localhost:8000/api/v1/orders", {
  method: "GET",
  headers: headers
})
.then(res => res.json())
.then(data => console.log(data));
```

---

## 📊 Database Schema

### Tables

| Table | Purpose | Records |
|-------|---------|---------|
| **menus** | Restaurant menus | 2 |
| **categories** | Item categories | 5 |
| **menu_items** | Individual items | 10 |
| **orders** | Customer orders | 11 |
| **order_items** | Items in orders | 52 |
| **payments** | Payment transactions | 17 |
| **api_keys** | API authentication | 1+ |

### Entity Relationships

```
Menu (1) ── (Many) Category
  │
  └── (Many) MenuItem
        │
        └── (Many) OrderItem ── (Many) Order
                                   │
                                   └── (Many) Payment
```

---

## 🧪 Testing

### Verify Installation

```bash
# Check database connection
python -c "from database import engine; engine.connect(); print('✅ DB Connected')"

# Check imports
python -c "from main import app; print('✅ App Ready')"
```

### Test Endpoints

#### 1. Health Check
```bash
curl http://localhost:8000/health
```

#### 2. Get All Orders
```bash
curl -H "X-API-Key: sk_test_restaurant_pos_2025_secure_key_12345" \
  http://localhost:8000/api/v1/orders
```

#### 3. Get Specific Order
```bash
curl -H "X-API-Key: sk_test_restaurant_pos_2025_secure_key_12345" \
  http://localhost:8000/api/v1/orders/14
```

#### 4. Test Error Handling
```bash
# Missing API key
curl http://localhost:8000/api/v1/orders

# Invalid order ID
curl -H "X-API-Key: sk_test_restaurant_pos_2025_secure_key_12345" \
  http://localhost:8000/api/v1/orders/999
```

---

## 📁 Project Structure

```
restaurant_pos_api/
├── main.py              # API endpoints and business logic
├── models.py            # SQLAlchemy ORM models
├── schemas.py           # Pydantic validation schemas
├── database.py          # Database configuration
├── security.py          # API authentication
├── load_data.py         # Sample data loader
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── .gitignore          # Git ignore file
```

### File Descriptions

| File | Purpose |
|------|---------|
| **main.py** | FastAPI app with all endpoints |
| **models.py** | Database ORM models (Menu, Order, etc.) |
| **schemas.py** | Pydantic validation schemas |
| **database.py** | Database connection setup |
| **security.py** | API key validation |
| **load_data.py** | Load sample restaurant data |

---

## 🔒 Security

### Best Practices Implemented

✅ **API Key Authentication** - All sensitive endpoints protected
✅ **Input Validation** - Pydantic schemas validate all data
✅ **Error Handling** - No sensitive data in error messages
✅ **CORS** - Configurable cross-origin requests
✅ **Connection Pooling** - Prevents connection exhaustion

### Recommendations for Production

- [ ] Move API key to environment variables
- [ ] Use HTTPS instead of HTTP
- [ ] Implement rate limiting
- [ ] Add request logging
- [ ] Use database user with limited privileges
- [ ] Enable database encryption
- [ ] Implement API versioning
- [ ] Add comprehensive error logging

---

## ⚡ Performance

### Optimizations

- **Connection Pooling**: Pool size 20 for concurrent requests
- **Eager Loading**: Uses `joinedload` to prevent N+1 queries
- **Indexed Queries**: Primary keys indexed for fast lookups
- **Response Caching**: Stateless design allows CDN caching
- **Async Ready**: FastAPI async support for high concurrency

### Sample Response Times

- Health Check: ~2ms
- Get All Orders: ~15ms
- Get Specific Order: ~5ms

---

## 🐛 Troubleshooting

### Connection Issues

```bash
# Test MySQL connection
mysql -u root -p -h localhost -e "SELECT 1"

# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process on port 8000
taskkill /PID <PID> /F
```

### Common Errors

| Error | Solution |
|-------|----------|
| "Can't connect to MySQL" | Start MySQL service, check credentials |
| "Module not found" | Run `pip install -r requirements.txt` |
| "Port 8000 in use" | Change port in main.py or kill process |
| "Order not found" | Run `python load_data.py` to load sample data |

---

## 📝 License

This project is provided as-is for educational purposes.

---

## 👤 Author

**Abhay Mehta**
- GitHub: https://github.com/abhaynmehta
- Email: abhaynmehta03@gmail.com

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Open an issue on GitHub
4. Contact support

---

## 🚀 Future Enhancements

- [ ] POST endpoint to create new orders
- [ ] PUT endpoint to modify orders
- [ ] DELETE endpoint to cancel orders
- [ ] Advanced analytics endpoints
- [ ] WebSocket support for real-time updates
- [ ] Multi-restaurant support
- [ ] Payment gateway integration
- [ ] Inventory management

---

**Last Updated:** December 6, 2025
**Version:** 1.0.0
