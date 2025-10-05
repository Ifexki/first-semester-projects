import psycopg2
from datetime import datetime  # You forgot to import this earlier!

try:
    conn = psycopg2.connect(
        dbname="altschool_assignment",
        user="postgres",
        password="Optimus5050#",
        host="localhost",
        port=5432  
    )

    cur = conn.cursor()

    # --- Create customers table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100)
    );
    """)

    # --- Create sales table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id SERIAL PRIMARY KEY,
        customer_id INTEGER REFERENCES customers(id),
        product VARCHAR(100),
        amount NUMERIC(10, 2),
        sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # --- Insert 5 customers and capture their IDs
    customer_data = [
        ('Alice Johnson', 'alice.johnson@example.com'),
        ('Bob Smith', 'bob.smith@example.com'),
        ('Carol Davis', 'carol.davis@example.com'),
        ('David Nguyen', 'david.nguyen@example.com'),
        ('Eva Martinez', 'eva.martinez@example.com')
    ]

    customer_ids = []
    for customer in customer_data:
        cur.execute("""
            INSERT INTO customers (name, email)
            VALUES (%s, %s)
            RETURNING id;
        """, customer)
        customer_id = cur.fetchone()[0]
        customer_ids.append(customer_id)

    # --- Insert 5 sales linked to those customers
    sales_data = [
        (customer_ids[0], 'Laptop', 1299.99, datetime(2025, 10, 1)),
        (customer_ids[1], 'Smartphone', 799.49, datetime(2025, 10, 2)),
        (customer_ids[2], 'Tablet', 499.00, datetime(2025, 10, 3)),
        (customer_ids[3], 'Monitor', 199.99, datetime(2025, 10, 4)),
        (customer_ids[4], 'Keyboard', 89.99, datetime(2025, 10, 5))
    ]

    cur.executemany("""
        INSERT INTO sales (customer_id, product, amount, sale_date)
        VALUES (%s, %s, %s, %s);
    """, sales_data)

    # Commit the changes
    conn.commit()
    print("Tables created and data inserted successfully.")


     # --- Create products table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE
    );
    """)

    # Insert products (including 'Mouse' which is not sold)
    products = ['Laptop', 'Smartphone', 'Tablet', 'Monitor', 'Keyboard', 'Mouse']

    for product in products:
        cur.execute("""
            INSERT INTO products (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING;
        """, (product,))

    conn.commit()

    # --- 4. Total number of orders
    cur.execute("SELECT COUNT(*) FROM sales;")
    total_orders = cur.fetchone()[0]
    print(f"Total number of orders: {total_orders}")

    # --- 5. Total revenue from all orders
    cur.execute("SELECT SUM(amount) FROM sales;")
    total_revenue = cur.fetchone()[0]
    print(f"Total revenue from all orders: ${total_revenue:.2f}")

    # --- 6. INNER JOIN: order details with customer and product names
    cur.execute("""
        SELECT
            sales.id AS sale_id,
            customers.name AS customer_name,
            sales.product,
            sales.amount,
            sales.sale_date
        FROM sales
        INNER JOIN customers ON sales.customer_id = customers.id;
    """)
    orders = cur.fetchall()
    print("\nOrder Details (INNER JOIN):")
    for order in orders:
        print(order)

    # --- 7. LEFT JOIN: all products and related sales (even if no sale)
    cur.execute("""
        SELECT
            products.name AS product_name,
            sales.id AS sale_id,
            sales.amount,
            customers.name AS customer_name
        FROM products
        LEFT JOIN sales ON products.name = sales.product
        LEFT JOIN customers ON sales.customer_id = customers.id;
    """)
    product_sales = cur.fetchall()
    print("\nAll Products with related sales (LEFT JOIN):")
    for row in product_sales:
        print(row)

    # --- 8. Retrieve all orders made by a specific customer (e.g., Alice Johnson)
    customer_name = 'Alice Johnson'
    cur.execute("""
        SELECT sales.id, sales.product, sales.amount, sales.sale_date
        FROM sales
        JOIN customers ON sales.customer_id = customers.id
        WHERE customers.name = %s;
    """, (customer_name,))
    customer_orders = cur.fetchall()
    print(f"\nOrders by {customer_name}:")
    for order in customer_orders:
        print(order)

except Exception as error:
    print("An error occurred:", error)
finally:
    cur.close()
    conn.close()
