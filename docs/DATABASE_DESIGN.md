# KayaKonnect Database Design

## What We're Using
We chose PostgreSQL as our database because it's reliable, supports complex queries, and works well with Python through the psycopg2 library. The database runs locally on each developer's machine during development.

Our connection details are stored in a .env file (not pushed to GitHub for security reasons). The database name is kayakonnect and it runs on port 5433.

---

## The Tables

### customers
This table holds the information of every customer that registers on the platform. When someone signs up as a customer, a new row is added here. The email column is unique so no two customers can use the same email address.

The columns are: id, full_name, email, phone, address, password_hash, profile_picture, and created_at.

The password is never stored in plain text — we hash it using SHA-256 before saving it.


### couriers
Similar to the customers table but for couriers (Kayas). Couriers have a few extra fields that customers don't have, like vehicle_type, is_available (whether they're currently accepting jobs), and rating.

The columns are: id, full_name, email, phone, address, password_hash, profile_picture, vehicle_type, is_available, rating, and created_at.


### delivery_requests
This is the most important table in the system. Every time a customer creates a delivery request, a row is added here. The request_id is a human-readable ID like KAY00001, KAY00002, and so on.

When a request is first created, the courier_id is empty because no courier has accepted it yet. Once a courier accepts the job, their ID is recorded here.

The columns are: id, request_id, customer_id, courier_id, lead_size, urgency_level, pickup_location, destination, recommended_price, status, date_created, and date_updated.

The status column tracks where the request is in its lifecycle. It starts as pending, then moves to accepted when a courier picks it up, then in_progress, and finally completed. It can also be cancelled.


### notifications
This table stores notifications for both customers and couriers. The user_type column tells us whether the notification belongs to a customer or a courier, and user_id tells us which specific person it belongs to.

The columns are: id, user_id, user_type, message, is_read, and created_at.


## How the Tables Relate to Each Other

A customer can create many delivery requests, but each request belongs to only one customer. A courier can accept many requests over time, but each request can only be assigned to one courier at a time.

The delivery_requests table sits in the middle — it connects customers and couriers through the customer_id and courier_id columns.


## How Pricing Works

The price for each delivery is calculated automatically by our pricing engine (written by Sean). It takes three things into account: the size of the load, the urgency level, and the distance between the pickup and destination.

The base fare starts at 500 naira. From there, multipliers are applied based on the load size and urgency. The distance is estimated from the pickup and destination text and costs 150 naira per kilometre.

So for example, a large load with high urgency over a long distance would cost significantly more than a small load with low urgency going a short distance. The final price is shown to the customer before they submit their request so there are no surprises.


## Security

Passwords are hashed before being stored so even if someone accessed the database directly, they wouldn't be able to read any passwords. Database credentials are stored in a .env file that is listed in .gitignore so it never gets pushed to GitHub.