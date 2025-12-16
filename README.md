

# Shopzy - E-Commerce Platform

Shopzy is a full-featured **e-commerce web application** built with **Django**, designed to connect buyers and sellers efficiently. The platform supports multiple user roles, product management with multiple images, reviews, search, and order management. The UI is modern, responsive, and styled with **Tailwind CSS**.  

This project is ideal for learning **full-stack web development** concepts, including user roles, file uploads, dynamic queries, and payment simulation.

---

## Features

### User Roles

- **Buyer**
  - Can browse products and search using keywords
  - Add reviews and ratings for purchased products
  - Manage personal profile and address
  - Place orders and track their status
- **Seller**
  - Can manage their shop and products
  - Add, edit, or delete products
  - Upload **multiple images per product**
  - Track product orders and see buyer reviews
  - View shop rating (cannot update manually)

---

### Product Management

- Sellers can add products with:
  - Name, description, price, category, stock
  - Multiple images per product
- Products can be **edited** or **deleted**
- Upload new images while editing
- Products display **average rating** and **total reviews** dynamically

---

### Search Feature

- Buyers can search for products using a **keyword**  
- Search is performed on:
  - Product name
  - Product description
  - Product category name
- Returns matching results ordered by creation date
- Supports partial and case-insensitive matches

---

### Reviews & Ratings

- Buyers can rate products from **1 to 5 stars** and add textual feedback
- Each product dynamically calculates:
  - Average rating
  - Total number of reviews
- Prevents duplicate reviews from the same user

---

### Order Management & Status Tracking

- Buyers can place orders for products
- Each order tracks:
  - Payment status (Pending, Successful, Failed)
  - Delivery status (Shipped, Out for Delivery, Delivered)
- Orders have a **timeline view** with timestamps for every status update
- Sellers can view **incoming orders** and update statuses

---

### Mock Payment Integration

- Payments are simulated for testing without a real payment gateway
- Users can click “Pay” to simulate:
  - **Successful payment**
  - **Failed payment**
  - **Pending payment**
- Payment status updates are reflected in order history immediately
- Useful for development and testing without integrating real APIs

---

### Product Images

- Supports **image uploads** 
- Sellers can add additional images when editing
- Images are stored and displayed in the product detail page
- Uses **Pillow** for image handling

---

### Responsive UI

- Built with **Tailwind CSS**
- Modern layout with forms, buttons, and cards
- Hover effects and transitions for better UX
- Mobile-friendly and responsive across screen sizes

---

### Chatbot - RAG
- Build with vectorstore FAISS and used hugging face embeddings to convert the text of manual
- Also used product and other details as context for better responses
- Also maintains some history of previous messages to store the context.

## Tech Stack

- **Backend**: Django, Django ORM
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Database**: SQLite (default, can switch to PostgreSQL/MySQL)
- **Others**:
  - Pillow (image handling)
  - Django messages framework
  - Django authentication and user roles

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-username/shopzy.git
cd myshop
````

2. **Create and activate a virtual environment**

```bash
python -m venv env
source env/bin/activate    # Linux/Mac
env\Scripts\activate       # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Apply migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser (admin access)**

```bash
python manage.py createsuperuser
```

6. **Run the development server**

```bash
python manage.py runserver
```

7. Open `http://127.0.0.1:8000/` in your browser.

---


## Project Structure

```
myshop/
├─ products/
│  ├─ models.py      # Product, ProductImage, Review
│  ├─ forms.py       # ProductForm, ProductImageForm, ReviewForm
│  ├─ views.py       # Product CRUD, reviews, search, orders
│  
├─ accounts/
│  ├─ models.py      # User, BuyerProfile, SellerProfile
│  └─ views.py
├─ templates/
│  ├─ base.html
│  └─ ...
├─ static/
├─ manage.py
└─ requirements.txt
```

---


---


29e4" />

<img width="1345" height="683" alt="image" src="https://github.com/user-attachments/assets/08ad8133-c1fa-4b45-bc09-f9d6517fc649" />

<img width="1363" height="715" alt="Screenshot 2025-12-14 103247" src="https://github.com/user-attachments/assets/c9dff470-82bc-4f74-b229-322be5564e16" />

<img width="1361" height="663" alt="Screenshot 2025-12-14 103308" src="https://github.com/user-attachments/assets/0479b998-aaeb-4255-9a81-c3826107f88e" />



