# E-Commerce API

## Description
This project is an E-Commerce API built using Flask. It allows managing customers, customer accounts, products, and orders through various CRUD endpoints.

## Installation
Follow these steps to set up and run the project:

1. Clone the repository: `git clone https://github.com/yourusername/ecommerce-api.git` and navigate to the project directory.
2. Install dependencies by running `pip install -r requirements.txt`.
3. Ensure you have MySQL installed and running. Create a database named `api_e_commerce`.
4. Update the `SQLALCHEMY_DATABASE_URI` in `app.py` with your MySQL username and password.
5. Run the application using `python app.py`.

## Usage
You can interact with the API using tools like Postman or cURL.

### API Endpoints

#### Customers
- **Create Customer**
  - **Endpoint:** `/customer`
  - **Method:** `POST`
  - **Description:** Adds a new customer to the database.
  - **Request Body:**
    - `name`: String (required)
    - `email`: String (required)
    - `phone`: String (required)
  - **Response:**
    - `message`: "customer added"

- **Read Customers**
  - **Endpoint:** `/customer`
  - **Method:** `GET`
  - **Description:** Retrieves all customers.
  - **Response:** List of customers.

- **Update Customer**
  - **Endpoint:** `/customer/<int:id>`
  - **Method:** `PUT`
  - **Description:** Updates customer details by ID.
  - **Request Body:**
    - `name`: String
    - `email`: String
    - `phone`: String
  - **Response:**
    - `message`: "Customer details updated"

- **Delete Customer**
  - **Endpoint:** `/customers/<int:id>`
  - **Method:** `DELETE`
  - **Description:** Deletes a customer by ID.
  - **Response:**
    - `message`: "Customer removed"

#### Customer Accounts
- **Create Customer Account**
  - **Endpoint:** `/customer/<int:customer_id>/account`
  - **Method:** `POST`
  - **Description:** Creates a new account for a customer.
  - **Request Body:**
    - `username`: String (required, unique)
    - `password`: String (required)
  - **Response:** Customer account details.

- **Read Customer Accounts**
  - **Endpoint:** `/customer/<int:customer_id>/account`
  - **Method:** `GET`
  - **Description:** Retrieves all accounts for a specific customer.
  - **Response:** List of customer accounts.

- **Update Customer Account**
  - **Endpoint:** `/customer/account/<int:id>`
  - **Method:** `PUT`
  - **Description:** Updates customer account details by ID.
  - **Request Body:**
    - `username`: String
    - `password`: String
  - **Response:** Updated customer account details.

- **Delete Customer Account**
  - **Endpoint:** `/customer/account/<int:id>`
  - **Method:** `DELETE`
  - **Description:** Deletes a customer account by ID.
  - **Response:**
    - `message`: "Customer account deleted successfully"

#### Products
- **Create Product**
  - **Endpoint:** `/product`
  - **Method:** `POST`
  - **Description:** Adds a new product to the database.
  - **Request Body:**
    - `name`: String
    - `price`: Float
  - **Response:** Product details.

- **Read Products**
  - **Endpoint:** `/product`
  - **Method:** `GET`
  - **Description:** Retrieves all products.
  - **Response:** List of products.

- **Read Product**
  - **Endpoint:** `/product/<int:id>`
  - **Method:** `GET`
  - **Description:** Retrieves product details by ID.
  - **Response:** Product details.

- **Update Product**
  - **Endpoint:** `/product/<int:id>`
  - **Method:** `PUT`
  - **Description:** Updates product details by ID.
  - **Request Body:**
    - `name`: String
    - `price`: Float
  - **Response:** Updated product details.

- **Delete Product**
  - **Endpoint:** `/product/<int:id>`
  - **Method:** `DELETE`
  - **Description:** Deletes a product by ID.
  - **Response:**
    - `message`: "Product deleted successfully"

#### Orders
- **Place Order**
  - **Endpoint:** `/orders`
  - **Method:** `POST`
  - **Description:** Places a new order.
  - **Request Body:**
    - `order_date`: DateTime (required)
    - `customer_id`: Integer (required)
    - `products`: List of product IDs (required)
  - **Response:**
    - `message`: "Order placed successfully"

- **Retrieve Order**
  - **Endpoint:** `/orders/<int:id>`
  - **Method:** `GET`
  - **Description:** Retrieves order details by ID.
  - **Response:** Order details.

- **Track Order**
  - **Endpoint:** `/orders/<int:id>/track`
  - **Method:** `GET`
  - **Description:** Tracks the status and progress of an order.
  - **Response:** Order status and expected delivery date.
