# 🍔 FoodHub — Food Delivery Web Application

> A full-stack food delivery platform built as a portfolio project, simulating a real-world system like Pathao Food or Foodpanda.

![FoodHub](https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=1200&h=400&fit=crop&q=80)

---

## 🚀 Live Demo

| Role     | Email                  | Password      |
|----------|------------------------|---------------|
| Admin    | admin@foodhub.com      | admin123      |
| Customer | rahim@example.com      | customer123   |

---

## 📋 Features

### Customer
- ✅ Register & log in with JWT authentication
- ✅ Browse restaurants with search, filter by category, and sort by rating
- ✅ View restaurant menus grouped by category
- ✅ Add items to cart with quantity control (persisted in localStorage)
- ✅ Checkout with delivery address and Cash on Delivery
- ✅ View order history with live status progress tracker
- ✅ Update profile and default delivery address

### Admin
- ✅ Full dashboard with order/restaurant stats
- ✅ Create, edit, delete restaurants
- ✅ Create, edit, delete food menu items
- ✅ View all orders and update order status (Pending → Accepted → Preparing → On the way → Delivered)

---

## 🗄️ Database Schema

```
users          → user_id, name, email, password_hash, phone, address, role
restaurants    → restaurant_id, name, location, category, rating, image_url, description, is_open
food_items     → food_id, restaurant_id (FK), name, price, description, image_url, category, is_available
orders         → order_id, user_id (FK), total_price, status, delivery_address, payment_method, created_at
order_items    → order_item_id, order_id (FK), food_id (FK), quantity, unit_price
```

**Relationships:**
- `users` → `orders` (1:N)
- `restaurants` → `food_items` (1:N)
- `orders` → `order_items` (1:N)
- `food_items` → `order_items` (1:N)

---

## ⚙️ Tech Stack

| Layer      | Technology                             |
|------------|----------------------------------------|
| Frontend   | HTML5, CSS3, Vanilla JavaScript (ES6+) |
| Backend    | Python 3, Flask 3                      |
| Auth       | Flask-JWT-Extended (JWT tokens)        |
| ORM        | SQLAlchemy + Flask-Migrate             |
| Database   | SQLite (dev) / PostgreSQL (prod)       |
| Passwords  | bcrypt hashing                         |
| CORS       | Flask-CORS                             |

---

## 📁 Project Structure

```
foodhub/
├── backend/
│   ├── app.py              # Flask app factory + seed data
│   ├── config.py           # Configuration class
│   ├── models.py           # SQLAlchemy models
│   ├── requirements.txt
│   ├── .env.example
│   └── routes/
│       ├── auth.py         # /api/v1/auth/*
│       ├── restaurants.py  # /api/v1/restaurants/*
│       └── orders.py       # /api/v1/orders/*
├── frontend/
│   ├── css/
│   │   └── style.css       # Design system + all component styles
│   ├── js/
│   │   └── api.js          # API client, auth helpers, cart, toast, navbar
│   └── pages/
│       ├── login.html
│       ├── signup.html
│       ├── restaurant.html
│       ├── cart.html
│       ├── orders.html
│       ├── profile.html
│       └── admin.html
├── index.html              # Home page (restaurant listing)
├── start.sh                # One-command launcher
└── README.md
```

---

## 🛠️ Quick Start

### Prerequisites
- Python 3.10+
- A modern web browser

### Option A — One-command start (macOS / Linux)

```bash
git clone https://github.com/SoulReapeer/foodhub.git
cd foodhub
chmod +x start.sh
./start.sh
```

### Option B — Manual setup

```bash
# 1. Backend
cd backend
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py                     # Starts on http://localhost:5000

# 2. Frontend
# Open index.html in your browser directly, or use any static server:
npx serve .                       # http://localhost:3000
# or: python3 -m http.server 8080
```

> **Note:** The frontend makes API calls to `http://localhost:5000`. Make sure the Flask backend is running before opening the browser.

---

## 🔌 API Reference

All endpoints are prefixed with `/api/v1`.

### Auth
| Method | Endpoint          | Description              | Auth |
|--------|-------------------|--------------------------|------|
| POST   | /auth/register    | Create account           | —    |
| POST   | /auth/login       | Login, returns JWT token | —    |
| GET    | /auth/me          | Get current user         | ✅   |
| PUT    | /auth/me          | Update profile           | ✅   |

### Restaurants
| Method | Endpoint                    | Description              | Auth    |
|--------|-----------------------------|--------------------------|---------|
| GET    | /restaurants                | List (search, filter)    | —       |
| GET    | /restaurants/:id            | Single + menu            | —       |
| POST   | /restaurants                | Create                   | Admin   |
| PUT    | /restaurants/:id            | Update                   | Admin   |
| DELETE | /restaurants/:id            | Delete                   | Admin   |
| GET    | /restaurants/:id/items      | Menu items               | —       |
| POST   | /restaurants/:id/items      | Add item                 | Admin   |
| PUT    | /restaurants/items/:id      | Update item              | Admin   |
| DELETE | /restaurants/items/:id      | Delete item              | Admin   |

### Orders
| Method | Endpoint             | Description           | Auth     |
|--------|----------------------|-----------------------|----------|
| POST   | /orders              | Place order           | Customer |
| GET    | /orders/my           | My order history      | Customer |
| GET    | /orders/:id          | Single order detail   | Customer |
| GET    | /orders              | All orders            | Admin    |
| PUT    | /orders/:id/status   | Update status         | Admin    |

---

## 🎨 Design System

- **Fonts:** Playfair Display (headings) + DM Sans (body)
- **Primary color:** `#E8441A` (warm coral-orange)
- **Surface:** Off-white `#FBF8F5` for warmth
- **Design philosophy:** Editorial warmth — like a premium food magazine

---

## 🔑 Authentication Flow

```
User submits email + password
         ↓
Flask verifies with bcrypt
         ↓
JWT token issued (24h expiry) with { user_id, role } claims
         ↓
Frontend stores token in localStorage
         ↓
Every protected API request sends: Authorization: Bearer <token>
         ↓
Flask-JWT-Extended verifies + extracts claims
         ↓
@admin_required decorator checks role claim
```


---

## 📌 Possible Extensions

- [ ] Stripe / SSLCommerz payment integration
- [ ] Real-time order tracking with WebSockets (Flask-SocketIO)
- [ ] Push notifications (Web Push API)
- [ ] Restaurant owner role (third user type)
- [ ] Food item reviews and ratings
- [ ] Delivery distance / ETA calculation
- [ ] Order invoice PDF download
- [ ] Image upload to Cloudinary

---

# FoodHub — Setup & Run Guide

Here's everything you need to get FoodHub running on your machine, from zero to working app.

---

## What you need first

- **Python 3.10 or newer** — download from [python.org](https://python.org) if you don't have it
- **A modern browser** (Chrome, Firefox, Edge)
- **A terminal** (Terminal on Mac/Linux, Command Prompt or PowerShell on Windows)

Check your Python version by running:
```bash
python3 --version 
```
If it shows 3.10 or higher, you're good.

---

## Step 1 — Download and extract the project

Download the `FoodHub.zip` file from [https://github.com/SoulReapeer/foodhub.git](https://github.com/SoulReapeer/foodhub.git), then extract it. You'll get a folder called `foodhub`. Move it somewhere convenient, like your Desktop or Documents.

---

## Step 2 — Open a terminal in the project folder

**On Mac/Linux:**
Right-click the `foodhub` folder and choose "Open Terminal Here", or run:
```bash
cd ~/Desktop/foodhub
```

**On Windows:**
Open the `foodhub` folder in File Explorer, click the address bar, type `cmd`, and press Enter. Or in PowerShell:
```powershell
cd C:\Users\YourName\Desktop\foodhub
```

---

## Step 3 — Create a virtual environment

A virtual environment keeps the project's Python packages isolated from the rest of your system. Run this inside the `foodhub` folder:

```bash
cd backend
python3 -m venv venv
```

On Windows:
```powershell
cd backend
python -m venv venv
```

You'll see a new folder called `venv` appear inside `backend/`. That's correct.

---

## Step 4 — Activate the virtual environment

**Mac/Linux:**
```bash
source venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

Your terminal prompt will change to show `(venv)` at the start — that means it's active.

---

## Step 5 — Install dependencies

With the virtual environment active, install all the required Python packages:

```bash
pip install -r requirements.txt
```

This installs Flask, SQLAlchemy, JWT, bcrypt, and everything else the backend needs. It takes about 30–60 seconds. You'll see a list of packages being downloaded.

---

## Step 6 — Start the Flask backend

Still inside the `backend/` folder with `(venv)` active, run:

```bash
python app.py
```

You should see output like this:
```
✅ Seed data loaded
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

**The backend is now running.** The seed data line means 6 restaurants and their menus were automatically created in the database. Leave this terminal window open — the server must keep running while you use the app.

---

## Step 7 — Open the frontend

Open a **new** terminal or file explorer window (don't close the Flask terminal). Navigate to the main `foodhub/` folder and open `index.html` in your browser.

**The easiest way:** just double-click `index.html` in your file explorer. It will open in your default browser.

Alternatively, right-click `index.html` → Open With → Chrome (or your browser of choice).

The URL in your browser will look something like:
```
file:///C:/Users/YourName/Desktop/foodhub/index.html
```

---

## Step 8 — Log in and explore

The app comes with two pre-made accounts:

| Role | Email | Password |
|---|---|---|
| Admin | admin@foodhub.com | admin123 |
| Customer | rahim@example.com | customer123 |

**To test the full flow as a customer:**
1. Go to Login → sign in as `rahim@example.com`
2. Click any restaurant on the home page
3. Add a few items to your cart
4. Click the cart button → Proceed to Checkout
5. Enter a delivery address → Place Order
6. Go to My Orders to see the order with its status tracker

**To test the admin panel:**
1. Log out, then sign in as `admin@foodhub.com`
2. Click your name in the top right → Admin Panel
3. You can add/edit/delete restaurants and food items
4. Under the Orders tab, change any order's status using the dropdown

---

## Stopping the server

When you're done, go back to the Flask terminal and press `Ctrl + C`. Then deactivate the virtual environment:

```bash
deactivate
```

Next time you want to run it, you only need Steps 4 and 6 — the packages are already installed.

---

## Troubleshooting

**"Port 5000 is already in use"**
Something else is running on port 5000. On Mac, AirPlay Receiver uses it. Go to System Settings → General → AirDrop & Handoff → turn off AirPlay Receiver. Or on any OS, change the port in `backend/app.py` on the last line:
```python
app.run(debug=True, port=5001)
```
Then also update the `API_BASE` line in `frontend/js/api.js` to match:
```javascript
const API_BASE = 'http://localhost:5001/api/v1';
```

**"No restaurants showing / fetch error"**
The Flask backend isn't running. Make sure you completed Step 6 and the terminal still shows the Flask server running.

**"Module not found" error**
The virtual environment isn't active. Go back to Step 4 and activate it before running `python app.py`.

**Windows: "running scripts is disabled"**
Run this in PowerShell once to allow local scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try activating the venv again.

---

## 👤 Author

Built as a portfolio project to demonstrate full-stack development skills.

- GitHub: [@SoulReapeer](https://github.com/SoulReapeer)

---

## 📄 License

MIT License — free to use for learning and portfolio purposes.
