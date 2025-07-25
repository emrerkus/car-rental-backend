# 🚗 Car Rental Backend API

A backend application for a car rental platform, built with **Flask**, **PostgreSQL**, and **SQLAlchemy**.  
Supports multiple user roles, authentication, car management, and rental operations.

---

## 🔧 Tech Stack

- 🐍 Flask (Python)
- 🐘 PostgreSQL (via Docker)
- ⚙️ SQLAlchemy (ORM)
- 🔐 Basic Auth
- 🧪 Postman (API testing)
- 🐳 Docker (PostgreSQL container)

---

## 📁 Features

- User registration & login (User / Merchant / Admin roles)
- Role-based authorization
- CRUD operations for cars
- Car filtering (brand, color, engine, type)
- Rental operations (start, end, payment calculation)
- Admin: View and manage users
- Account deletion
- Swagger/Postman Collection available

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/car-rental-backend.git
cd car-rental-backend
```

### 2. Install dependencies (in venv recommended)
```bash
pip install -r requirements.txt
```

### 3. Run PostgreSQL via Docker
```bash
docker run -d \
  --name <your_image_name> \
  -e POSTGRES_USER=<your_username> \
  -e POSTGRES_PASSWORD=<your_password> \
  -e POSTGRES_DB=<your_db_name> \
  -p 5432:5432 \
  postgres:<your_postgresql_version_ex_17>
```

### 4. Run the Flask app
```bash
python run.py <your_username> <your_password> 5432 <your_db_name>
```

## 🧪 Usage with Postman
Her endpoint için:
- Method
- URL örneği
- Authorization tipi
- Body örneği (JSON)

## Important Keywords
- POST /register for registering a new user
- GET /profile for getting information about that user (for all)
- POST /profile/my-cars for adding a new car (merchant users only)
- GET /profile/my-cars for listing the cars (merchant users only)
- PATCH /profile/my-cars/<car_id> for updating a car (merchant users only)
- DELETE /profile/my-cars/<car_id> for deleting a car (merchant users only)
- POST /rent for renting an available car (for customers only)
- POST /return/<rental_id> for returning the rented car. (for customers only)
- GET /cars for filtering and browsing cars on the platform. If you want to filter, you can test it using color, brand, engine, car_type. ex: /cars?color=red (for all)
- DELETE /profile for deleting the account (for all)
- GET /profile/rentals for seeing rental history for the user (for all)
