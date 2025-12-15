# Shopzy – Website Manual & Knowledge Base

## 1. Introduction

Shopzy is a full-stack e-commerce web application built using Django. It allows users to browse products, manage carts, place orders, and simulate payments using a mock payment gateway. The platform supports both buyers and sellers, each with role-specific features.

This document serves two purposes:

* A **user/admin manual** for understanding how the website works
* A **knowledge source** that can be ingested into an AI chatbot (RAG-based) to answer user queries

---

## 2. User Roles

### 2.1 Buyer (Customer)

Buyers can:

* Register and log in
* Browse available products
* View product details (price, description, images, stock)
* Add products to cart
* Place orders
* Make payments using a mock payment gateway
* View order history and payment status in their profile

### 2.2 Seller

Sellers can:

* Log in to their seller account
* Add new products
* Update product details (price, stock, description)
* View orders placed for their products
* Track order and payment status

---

## 3. Authentication & Accounts

* Shopzy uses Django’s built-in authentication system
* Users must be logged in to place orders or access profile-related features
* Each order and payment is linked to a specific authenticated user

---

## 4. Product Management

### 4.1 Product Listing

Each product contains:

* Product name
* Price
* Description
* Stock quantity
* Product image
* Seller information

Products are displayed on the main store page and can be accessed individually via a product detail page.

### 4.2 Stock Handling

* Stock is reduced automatically when an order is successfully placed
* If stock reaches zero, the product is shown as out of stock

---

## 5. Cart & Order Flow

### 5.1 Cart

* Users can add products to their cart
* Cart displays selected items, quantity, and total price

### 5.2 Order Creation

* When a user proceeds to checkout, an order is created
* Each order contains:

  * Order ID
  * User details
  * Ordered products
  * Total amount
  * Order status

Order statuses include:

* PENDING
* CONFIRMED
* CANCELLED

---

## 6. Mock Payment Gateway

Shopzy uses a **mock payment system** for demonstration and testing purposes.

### 6.1 Why Mock Payment?

* No real money is involved
* No third-party payment gateway integration required
* Useful for learning, demos, and hackathons

### 6.2 Payment Flow

1. User proceeds to payment after checkout
2. A unique payment ID is generated
3. User selects success or failure (simulated)
4. Payment status is updated accordingly

### 6.3 Payment Statuses

* PENDING – Payment initiated but not completed
* SUCCESS – Payment successful
* FAILED – Payment failed

Payment status directly affects order confirmation.

---

## 7. Order History & Profile

Users can view:

* Past orders
* Purchased products
* Payment status (success, failed, pending)
* Order dates and total amounts

This information is accessible from the user profile page.

---

## 8. Data Storage

### 8.1 Database

* Shopzy uses SQLite as the default database during development
* Data stored includes:

  * User accounts
  * Products
  * Orders
  * Order items
  * Payments

### 8.2 GitHub & Database Files

* The SQLite database file should **not** be pushed to GitHub
* Database files are environment-specific and regenerated locally

---

## 9. Chatbot Integration (Planned Feature)

Shopzy includes a floating chatbot UI designed to assist users.

The chatbot will be capable of answering:

* Product-related queries (price, availability, description)
* Order-related questions (order status, order history)
* Payment-related queries (payment success, failure, pending)
* General FAQs (delivery, returns, cancellations)

The chatbot will use:

* Retrieval-Augmented Generation (RAG)
* LangChain for orchestration
* Website documentation and database data as the knowledge base

---

## 10. FAQs

### Q1: Is real payment involved?

No. Shopzy uses a mock payment gateway for testing and demonstration.

### Q2: Is my data stored permanently?

Yes, data is stored in the database during runtime. However, this is a development setup.

### Q3: Can sellers see customer payment details?

Sellers can only view order and payment status, not sensitive user information.

### Q4: Will the chatbot access my personal data?

The chatbot will only access authenticated user data securely and contextually.

---

## 11. Future Enhancements

* Real payment gateway integration (Razorpay/Stripe)
* AI-powered chatbot with full RAG support
* Recommendation system
* Admin analytics dashboard

---

## 12. Conclusion

Shopzy is designed as a modular, scalable e-commerce platform suitable for learning, demos, and hackathons. This document acts as both a functional guide and a structured knowledge base for AI-powered features.
