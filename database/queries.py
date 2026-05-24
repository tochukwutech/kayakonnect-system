"""
database/queries.py
All database queries for KayaKonnect — customers, couriers, requests, profile, settings.
"""

from database.db_connection import get_connection


# ============================================================
# CUSTOMER QUERIES
# ============================================================

def get_customer_by_id(customer_id):
    """Fetch a single customer's full profile by ID."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return dict(result) if result else None


def get_customer_request_history(customer_id):
    """Fetch all past delivery requests for a customer."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            dr.request_id,
            dr.date_created,
            dr.recommended_price,
            dr.status,
            dr.pickup_location,
            dr.destination,
            dr.lead_size,
            dr.urgency_level,
            c.full_name AS courier_name
        FROM delivery_requests dr
        LEFT JOIN couriers c ON dr.courier_id = c.id
        WHERE dr.customer_id = %s
        ORDER BY dr.date_created DESC
    """, (customer_id,))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in results]


def get_customer_active_requests(customer_id):
    """Fetch active (pending/accepted/in_progress) requests for a customer."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            dr.request_id,
            dr.date_created,
            dr.recommended_price,
            dr.status,
            dr.pickup_location,
            dr.destination,
            dr.lead_size,
            dr.urgency_level,
            c.full_name AS courier_name
        FROM delivery_requests dr
        LEFT JOIN couriers c ON dr.courier_id = c.id
        WHERE dr.customer_id = %s
          AND dr.status IN ('pending', 'accepted', 'in_progress')
        ORDER BY dr.date_created DESC
    """, (customer_id,))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in results]


def create_delivery_request(customer_id, lead_size, urgency_level,
                             pickup_location, destination, recommended_price):
    """Insert a new delivery request for a customer."""
    conn = get_connection()
    cur = conn.cursor()

    # Generate a unique request ID like KAY00006
    cur.execute("SELECT COUNT(*) as total FROM delivery_requests")
    row = cur.fetchone()
    count = (row['total'] if row else 0) + 1
    request_id = f"KAY{str(count).zfill(5)}"

    cur.execute("""
        INSERT INTO delivery_requests
            (request_id, customer_id, lead_size, urgency_level,
             pickup_location, destination, recommended_price, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'pending')
        RETURNING request_id
    """, (request_id, customer_id, lead_size, urgency_level,
          pickup_location, destination, recommended_price))
    conn.commit()
    result = cur.fetchone()
    cur.close()
    conn.close()
    return dict(result)['request_id'] if result else None


def update_customer_profile(customer_id, full_name, phone, address):
    """Update a customer's profile details."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE customers
        SET full_name = %s, phone = %s, address = %s
        WHERE id = %s
    """, (full_name, phone, address, customer_id))
    conn.commit()
    cur.close()
    conn.close()


def update_customer_password(customer_id, new_password_hash):
    """Update a customer's password."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE customers SET password_hash = %s WHERE id = %s
    """, (new_password_hash, customer_id))
    conn.commit()
    cur.close()
    conn.close()


# ============================================================
# COURIER QUERIES
# ============================================================

def get_courier_by_id(courier_id):
    """Fetch a single courier's full profile by ID."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM couriers WHERE id = %s", (courier_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return dict(result) if result else None


def get_courier_accepted_jobs(courier_id):
    """Fetch accepted/in-progress jobs for a courier."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            dr.request_id,
            dr.date_created,
            dr.recommended_price AS price,
            dr.status,
            dr.pickup_location,
            dr.destination,
            dr.lead_size,
            dr.urgency_level,
            cu.full_name AS customer_name
        FROM delivery_requests dr
        LEFT JOIN customers cu ON dr.customer_id = cu.id
        WHERE dr.courier_id = %s
          AND dr.status IN ('accepted', 'in_progress', 'completed')
        ORDER BY dr.date_created DESC
    """, (courier_id,))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in results]


def get_available_jobs():
    """Fetch all pending jobs not yet assigned to a courier."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            dr.request_id,
            dr.date_created,
            dr.recommended_price AS price,
            dr.status,
            dr.pickup_location,
            dr.destination,
            dr.lead_size,
            dr.urgency_level,
            cu.full_name AS customer_name
        FROM delivery_requests dr
        LEFT JOIN customers cu ON dr.customer_id = cu.id
        WHERE dr.status = 'pending' AND dr.courier_id IS NULL
        ORDER BY dr.date_created DESC
    """)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in results]


def accept_job(courier_id, request_id):
    """Courier accepts a pending job."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE delivery_requests
        SET courier_id = %s, status = 'accepted', date_updated = CURRENT_TIMESTAMP
        WHERE request_id = %s AND status = 'pending'
    """, (courier_id, request_id))
    conn.commit()
    cur.close()
    conn.close()


def get_courier_earnings_summary(courier_id):
    """Returns total earnings and job count for a courier."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            COUNT(*) AS total_jobs,
            COALESCE(SUM(recommended_price), 0) AS total_earnings
        FROM delivery_requests
        WHERE courier_id = %s AND status = 'completed'
    """, (courier_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return dict(result) if result else {"total_jobs": 0, "total_earnings": 0}


def get_courier_monthly_earnings(courier_id):
    """Returns earnings grouped by month for the chart."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            TO_CHAR(date_created, 'Mon') AS month,
            COALESCE(SUM(recommended_price), 0) AS earnings
        FROM delivery_requests
        WHERE courier_id = %s AND status = 'completed'
        GROUP BY TO_CHAR(date_created, 'Mon'), EXTRACT(MONTH FROM date_created)
        ORDER BY EXTRACT(MONTH FROM date_created)
    """, (courier_id,))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in results]


def get_available_couriers():
    """Return all couriers marked as available (for customer to browse)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, full_name, phone, vehicle_type, rating
        FROM couriers
        WHERE is_available = TRUE
        ORDER BY rating DESC
    """)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in results]


def update_courier_profile(courier_id, full_name, phone, address, vehicle_type):
    """Update a courier's profile details."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE couriers
        SET full_name = %s, phone = %s, address = %s, vehicle_type = %s
        WHERE id = %s
    """, (full_name, phone, address, vehicle_type, courier_id))
    conn.commit()
    cur.close()
    conn.close()


def update_courier_password(courier_id, new_password_hash):
    """Update a courier's password."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE couriers SET password_hash = %s WHERE id = %s
    """, (new_password_hash, courier_id))
    conn.commit()
    cur.close()
    conn.close()


def toggle_courier_availability(courier_id, is_available):
    """Toggle a courier's availability status."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE couriers SET is_available = %s WHERE id = %s
    """, (is_available, courier_id))
    conn.commit()
    cur.close()
    conn.close()