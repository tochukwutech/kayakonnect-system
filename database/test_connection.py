from db_connection import get_connection

try:
    conn = get_connection()
    print("✅ Database connected successfully!")

    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) as total FROM customers")
    result = cur.fetchone()
    print(f"✅ Customers in DB: {result['total']}")

    cur.execute("SELECT COUNT(*) as total FROM couriers")
    result = cur.fetchone()
    print(f"✅ Couriers in DB: {result['total']}")

    cur.execute("SELECT COUNT(*) as total FROM delivery_requests")
    result = cur.fetchone()
    print(f"✅ Delivery requests in DB: {result['total']}")

    cur.close()
    conn.close()

except Exception as e:
    print("❌ Connection failed:")
    print(e)