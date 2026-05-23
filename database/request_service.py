from database.db_connection import get_connection


def create_request(load_size, urgency, pickup, destination, price):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO requests
        (load_size, urgency_level, pickup_location, destination, price)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            load_size,
            urgency,
            pickup,
            destination,
            price
        )

        cursor.execute(query, values)

        conn.commit()

        cursor.close()
        conn.close()

        return True

    except Exception as e:
        print("Database insertion error:")
        print(e)
        return False