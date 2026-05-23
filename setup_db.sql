-- ============================================================
-- KAYAKONNECT DATABASE SETUP SCRIPT
-- Run this in psql or pgAdmin to set up your database
-- ============================================================

-- Create customers table
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    password_hash VARCHAR(255) NOT NULL,
    profile_picture TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create couriers table
CREATE TABLE IF NOT EXISTS couriers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    password_hash VARCHAR(255) NOT NULL,
    profile_picture TEXT,
    vehicle_type VARCHAR(50),
    is_available BOOLEAN DEFAULT TRUE,
    rating NUMERIC(3,2) DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create delivery requests table
CREATE TABLE IF NOT EXISTS delivery_requests (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR(20) UNIQUE NOT NULL,
    customer_id INTEGER REFERENCES customers(id),
    courier_id INTEGER REFERENCES couriers(id),
    lead_size VARCHAR(20),         -- small, medium, large
    urgency_level VARCHAR(20),     -- low, normal, high
    pickup_location TEXT NOT NULL,
    destination TEXT NOT NULL,
    recommended_price NUMERIC(10,2),
    status VARCHAR(30) DEFAULT 'pending',  -- pending, accepted, in_progress, completed, cancelled
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    user_type VARCHAR(20) NOT NULL,  -- customer or courier
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- SAMPLE DATA (for testing)
-- ============================================================

-- Sample customers (password: 'password123' - hashed)
INSERT INTO customers (full_name, email, phone, address, password_hash)
VALUES
    ('Amara Kondé', 'amara@email.com', '+234 801 234 5678', '12 Lagos Street, Lagos', 'pbkdf2:sha256:sample_hash_1'),
    ('Chidi Okafor', 'chidi@email.com', '+234 802 345 6789', '45 Abuja Road, Abuja', 'pbkdf2:sha256:sample_hash_2')
ON CONFLICT DO NOTHING;

-- Sample couriers
INSERT INTO couriers (full_name, email, phone, address, password_hash, vehicle_type, rating)
VALUES
    ('Oluwaseun Adeyemi', 'seun@email.com', '+234 803 456 7890', '7 Courier Lane, Lagos', 'pbkdf2:sha256:sample_hash_3', 'Motorcycle', 4.5),
    ('Mansa Kondé', 'mansa@email.com', '+234 804 567 8901', '22 Express Road, Lagos', 'pbkdf2:sha256:sample_hash_4', 'Bicycle', 4.2)
ON CONFLICT DO NOTHING;

-- Sample delivery requests
INSERT INTO delivery_requests (request_id, customer_id, courier_id, lead_size, urgency_level, pickup_location, destination, recommended_price, status)
VALUES
    ('KAY00001', 1, 1, 'medium', 'high',   'Victoria Island, Lagos', 'Ikeja, Lagos',        1500.00, 'completed'),
    ('KAY00002', 1, 2, 'small',  'normal', 'Lekki Phase 1, Lagos',   'Surulere, Lagos',     800.00,  'completed'),
    ('KAY00003', 1, NULL, 'large', 'low',  'Yaba, Lagos',            'Ajah, Lagos',         2000.00, 'pending'),
    ('KAY00004', 2, 1, 'small',  'high',   'Apapa, Lagos',           'Maryland, Lagos',     1200.00, 'accepted'),
    ('KAY00005', 2, NULL, 'medium','normal','Gbagada, Lagos',         'Oshodi, Lagos',       950.00,  'pending')
ON CONFLICT DO NOTHING;