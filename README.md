# Modulo ERP

Modulo is a custom, modular Enterprise Resource Planning (ERP) system designed to manage inventory, sales, purchasing, and human resources. It provides a robust backend API and a modern, responsive frontend interface.

## Technology Stack

### Backend
- **Python 3**
- **FastAPI**: High-performance web framework for building APIs.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library.
- **SQLite**: Default relational database (can be easily swapped to PostgreSQL).
- **Passlib / Bcrypt**: Password hashing.
- **Python-JOSE**: JWT token generation and validation for authentication.
- **ReportLab**: PDF generation for invoices.

### Frontend
- **Vue 3 / Nuxt 3**: Modern framework for building Vue.js applications.
- **Tailwind CSS**: Utility-first CSS framework for rapid UI development.
- **Composition API**: For reusable and scalable state logic.

## Modules Overview

1. **Inventory Management (Upravljanje zalog)**
   - Track current stock levels for all articles.
   - View history of stock movements (incoming/outgoing).
   - Manually record inventory adjustments.

2. **Sales & Invoicing (Prodaja)**
   - Create and manage sales invoices.
   - Automatically deduct sold items from inventory upon invoice confirmation.
   - Generate and download PDF invoices.
   - Manage customer data.

3. **Purchasing (Nabava)**
   - Create purchase orders for suppliers.
   - Automatically increase stock levels and update purchase prices upon order delivery.
   - Filter available articles based on the selected supplier.

4. **Human Resources & Authentication (Kadri)**
   - Role-Based Access Control (RBAC): Admin, Salesperson (Prodajalec), Warehouse worker (Skladiščnik).
   - Secure login system using JWT.
   - Admins can manage employee accounts and assign roles.

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database and run migrations:
   ```bash
   python seed.py
   python migrate_dobavitelj.py
   python migrate_auth.py
   ```

5. Start the backend development server:
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the frontend development server:
   ```bash
   npm run dev
   ```
   The application will be available at `http://localhost:3000`.

## Default Credentials

A default administrator account is created during the database migration:
- **Email:** admin@erp.com
- **Password:** admin123

Please change this password in a production environment.

## License
Copyright 2026 Modulo. All rights reserved.
