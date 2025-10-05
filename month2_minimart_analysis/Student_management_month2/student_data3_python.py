# Simulated new order data: list of dicts
new_orders = [
    {"customer": "Alice Johnson", "product": "Laptop", "price": "1299.99", "quantity": 1},
    {"customer": "Bob Smith", "product": "Smartphone", "price": "799.49", "quantity": 2},
    {"customer": "Carol Davis", "product": "Tablet", "price": "499.00", "quantity": 3},
    {"customer": "David Nguyen", "product": "Monitor", "price": "199.99", "quantity": 1},
    {"customer": "Eva Martinez", "product": "Keyboard", "price": "89.99", "quantity": 4},
    {"customer": "Alice Johnson", "product": "Mouse", "price": "25.50", "quantity": 5},
]

# Apply discount function: 10% off if price > $500
def apply_discount(price_float):
    if price_float > 500:
        return price_float * 0.9  # 10% discount
    return price_float

# Identify customers who placed large orders (quantity >=3 or total order > $1000)
large_order_customers = set()

# Track total products sold & revenue per customer
total_products_sold = 0
revenue_per_customer = {}

# Track product popularity (count)
product_sales_count = {}

for order in new_orders:
    # Convert price from string to float and apply discount
    price = float(order["price"])
    discounted_price = apply_discount(price)
    
    total_price = discounted_price * order["quantity"]
    
    # Update total products sold
    total_products_sold += order["quantity"]
    
    # Update revenue per customer
    customer = order["customer"]
    revenue_per_customer[customer] = revenue_per_customer.get(customer, 0) + total_price
    
    # Update product sales count
    product = order["product"]
    product_sales_count[product] = product_sales_count.get(product, 0) + order["quantity"]
    
    # Check if this is a large order
    if order["quantity"] >= 3 or total_price > 1000:
        large_order_customers.add(customer)

# Find most popular product
most_popular_product = max(product_sales_count, key=product_sales_count.get)

# Create summary report dictionary
report = {
    "total_products_sold": total_products_sold,
    "most_popular_product": most_popular_product,
    "revenue_per_customer": revenue_per_customer,
    "large_order_customers": list(large_order_customers)
}

# Print report
print("Summary Report:")
print(f"Total products sold: {report['total_products_sold']}")
print(f"Most popular product: {report['most_popular_product']}")
print("Revenue per customer:")
for cust, rev in report["revenue_per_customer"].items():
    print(f"  {cust}: ${rev:.2f}")
print("Customers with large orders:", report["large_order_customers"])
