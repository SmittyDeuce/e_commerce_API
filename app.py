from flask import Flask, jsonify, request, abort  # Import necessary modules from Flask
from flask_marshmallow import Marshmallow  # Import Marshmallow for serialization/deserialization
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy for ORM
from marshmallow import ValidationError, fields  # Import validation error handling and fields from Marshmallow

app = Flask(__name__)  # Create Flask application instance
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://<user>:<password>@localhost/api_e_commerce"  # Configure the database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications to save resources

db = SQLAlchemy(app)  # Initialize SQLAlchemy with the Flask app
ma = Marshmallow(app)  # Initialize Marshmallow with the Flask app


# Define Customer schema for serialization/deserialization
class CustomerSchema(ma.Schema):
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)

    class Meta:
        fields = ("id", "name", "email", "phone")  # Specify fields to include in serialization

customer_schema = CustomerSchema()  # Create instance of CustomerSchema
customers_schema = CustomerSchema(many=True)  # Create instance of CustomerSchema for multiple customers


# Define CustomerAccount schema for serialization/deserialization
class CustomerAccountSchema(ma.Schema):
    username = fields.String(required=True, unique=True)
    password = fields.String(required=True, unique=True)

    class Meta:
        fields = ("id", "username", "password")  # Specify fields to include in serialization

customer_account_schema = CustomerAccountSchema()  # Create instance of CustomerAccountSchema
customer_accounts_schema = CustomerAccountSchema(many=True)  # Create instance of CustomerAccountSchema for multiple accounts


# Define Product schema for serialization/deserialization
class ProductSchema(ma.Schema):
    name = fields.String(required=True)
    price = fields.Float(required=True)

    class Meta:
        fields = ("id", "name", "price")  # Specify fields to include in serialization

product_schema = ProductSchema()  # Create instance of ProductSchema
products_schema = ProductSchema(many=True)  # Create instance of ProductSchema for multiple products


# Define Order schema for serialization/deserialization
class OrderSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    order_date = fields.DateTime(required=True)
    customer_id = fields.Integer(required=True)
    products = fields.List(fields.Integer(), required=True)

order_schema = OrderSchema()  # Create instance of OrderSchema
orders_schema = OrderSchema(many=True)  # Create instance of OrderSchema for multiple orders


# Define Customer model
class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)


# Define CustomerAccount model
class CustomerAccount(db.Model):
    __tablename__ = "customer_account"
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, unique=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)  # Foreign key to Customer
    customer = db.relationship("Customer", backref=db.backref("accounts", uselist=False, lazy=True))  # Define relationship


# Define Product model
class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)


# Define Order model
class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    order_date = db.Column(db.DateTime, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)  # Foreign key to Customer
    customer = db.relationship("Customer", backref=db.backref("orders", lazy=True))  # Define relationship
    products = db.relationship("Product", secondary="order_product")  # Many-to-many relationship with Product


@app.route("/")
def home():
    return "E Commerce API"  # Home route


@app.route("/customer", methods=["GET"])
def get_customer():
    customers = Customer.query.all()  # Retrieve all customers
    return customers_schema.jsonify(customers)  # Return serialized customers


@app.route("/customer", methods=["POST"])
def add_customer():
    try:
        customer_data = customer_schema.load(request.json)  # Deserialize request data

    except ValidationError as err:
        return jsonify(err.messages), 400  # Handle validation errors
    
    new_customer = Customer(
        name=customer_data["name"],
        email=customer_data["email"],
        phone=customer_data["phone"]
    )

    db.session.add(new_customer)  # Add new customer to the session
    db.session.commit()  # Commit the session
    return jsonify({"message": "customer added"})  # Return success message


@app.route("/customer/<int:id>", methods=["PUT"])
def update_customer(id):
    customer = Customer.query.get_or_404(id)  # Retrieve customer by ID or return 404

    try:
        customer_data = customer_schema.load(request.json)  # Deserialize request data

    except ValidationError as err:
        return jsonify(err.messages), 400  # Handle validation errors
    
    customer.name = customer_data["name"]
    customer.phone = customer_data["phone"]
    customer.email = customer_data["email"]
    db.session.commit()  # Commit the session
    return jsonify({"message": "Customer details updated"})  # Return success message


@app.route("/customers/<int:id>", methods=["DELETE"])
def delete_customer(id):
    customer = Customer.query.get(id)  # Retrieve customer by ID
    if not customer:
        abort(404, description=f"Customer {id} not found")  # Return 404 if not found
    
    db.session.delete(customer)  # Delete customer from the session
    db.session.commit()  # Commit the session
    return jsonify({"message": "Customer removed"}), 200  # Return success message


# CRUD Endpoints for CustomerAccount
@app.route("/customer/<int:customer_id>/account", methods=["POST"])
def create_customer_account(customer_id):
    customer = Customer.query.get_or_404(customer_id)  # Retrieve customer by ID or return 404
    try:
        account_data = customer_account_schema.load(request.json)  # Deserialize request data
    except ValidationError as err:
        return jsonify(err.messages), 400  # Handle validation errors

    new_account = CustomerAccount(
        username=account_data["username"],
        password=account_data["password"],
        customer_id=customer.id
    )

    db.session.add(new_account)  # Add new account to the session
    db.session.commit()  # Commit the session
    return customer_account_schema.jsonify(new_account), 201  # Return serialized new account


@app.route("/customer/<int:customer_id>/account", methods=["GET"])
def get_customer_accounts(customer_id):
    customer = Customer.query.get_or_404(customer_id)  # Retrieve customer by ID or return 404
    accounts = CustomerAccount.query.filter_by(customer_id=customer.id).all()  # Retrieve all accounts for the customer
    return customer_accounts_schema.jsonify(accounts)  # Return serialized accounts


@app.route("/customer/account/<int:id>", methods=["PUT"])
def update_customer_account(id):
    account = CustomerAccount.query.get_or_404(id)  # Retrieve account by ID or return 404
    try:
        account_data = customer_account_schema.load(request.json, partial=True)  # Deserialize request data
    except ValidationError as err:
        return jsonify(err.messages), 400  # Handle validation errors
    
    account.username = account_data.get("username", account.username)
    account.password = account_data.get("password", account.password)
    
    db.session.commit()  # Commit the session
    return customer_account_schema.jsonify(account)  # Return serialized updated account


@app.route("/customer/account/<int:id>", methods=["DELETE"])
def delete_customer_account(id):
    account = CustomerAccount.query.get_or_404(id)  # Retrieve account by ID or return 404
    db.session.delete(account)  # Delete account from the session
    db.session.commit()  # Commit the session
    return jsonify({"message": "Customer account deleted successfully"}), 200  # Return success message


# CRUD Endpoints for Product
@app.route("/product", methods=["POST"])
def add_product():
    try:
        product_data = product_schema.load(request.json)  # Deserialize request data
    except ValidationError as err:
        return jsonify(err.messages), 400  # Handle validation errors
    
    new_product = Product(
        name=product_data["name"],
        price=product_data["price"]
    )

    db.session.add(new_product)  # Add new product to the session
    db.session.commit()  # Commit the session
    return product_schema.jsonify(new_product), 201  # Return serialized new product


@app.route("/product", methods=["GET"])
def get_products():
    products = Product.query.all()  # Retrieve all products
    return products_schema.jsonify(products)  # Return serialized products


@app.route("/product/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get_or_404(id)  # Retrieve product by ID or return 404
    return product_schema.jsonify(product)  # Return serialized product


@app.route("/product/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get_or_404(id)  # Retrieve product by ID or return 404
    try:
        product_data = product_schema.load(request.json, partial=True)  # Deserialize request data
    except ValidationError as err:
        return jsonify(err.messages), 400  # Handle validation errors
    
    product.name = product_data.get("name", product.name)
    product.price = product_data.get("price", product.price)
    
    db.session.commit()  # Commit the session
    return product_schema.jsonify(product)  # Return serialized updated product


@app.route("/product/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get_or_404(id)  # Retrieve product by ID or return 404
    db.session.delete(product)  # Delete product from the session
    db.session.commit()  # Commit the session
    return jsonify({"message": "Product deleted successfully"}), 200  # Return success message


# CRUD Endpoints for Orders
@app.route("/orders", methods=["POST"])
def place_order():
    try:
        order_data = request.json
        validated_data = order_schema.load(order_data)  # Deserialize request data

        new_order = Order(
            order_date=validated_data["order_date"],
            customer_id=validated_data["customer_id"],
            products=validated_data["products"]
        )

        db.session.add(new_order)  # Add new order to the session
        db.session.commit()  # Commit the session

        return jsonify({"message": "Order placed successfully"}), 201  # Return success message

    except ValidationError as err:
        return jsonify(err.messages), 400  # Handle validation errors


@app.route("/orders/<int:id>", methods=["GET"])
def get_order(id):
    order = Order.query.get_or_404(id)  # Retrieve order by ID or return 404
    return order_schema.jsonify(order)  # Return serialized order


@app.route("/orders/<int:id>/track", methods=["GET"])
def track_order(id):
    order = Order.query.get_or_404(id)  # Retrieve order by ID or return 404
    return jsonify({
        "order_id": order.id,
        "order_date": order.order_date,
        "status": order.status,  # Add order status field
        "expected_delivery_date": order.expected_delivery_date  # Add expected delivery date field
    })


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)  # Run the Flask application in debug mode
