# KayaKonnect API Flow

## Overview
KayaKonnect is a desktop application built with Python and CustomTkinter. Instead of a traditional web API, the app communicates directly with a PostgreSQL database through a database query layer. This document explains how data flows through the system from the user interface down to the database and back.

---

## How It Works

When a user interacts with a screen, the screen calls a function from our queries module which handles all communication with the database. The result comes back and is displayed on the screen. There is no server in between — everything runs locally.

The flow looks like this:

User does something on screen → Screen calls a query function → Query function connects to PostgreSQL → Data is fetched or saved → Result is returned to the screen → Screen updates what the user sees


## Customer Flows

### Registration
The customer fills in their details on the signup screen. The screen calls the database directly and inserts a new row into the customers table. If the email already exists, an error is shown. On success, the customer is redirected to the login screen.

### Login
The customer enters their email and password. The system looks up the email in the customers table. If found, the customer is taken to their dashboard. The customer's ID is passed along and used throughout the session to fetch their specific data.

### Creating a Delivery Request
The customer fills in the pickup location, destination, lead size, and urgency level on the Create Request screen. The pricing engine (services/pricing_engine.py) automatically calculates the recommended price based on these inputs. When submitted, a new row is inserted into the delivery_requests table with a status of pending and a unique request ID like KAY00001.

### Viewing Request History
The customer dashboard fetches all past delivery requests linked to the logged-in customer's ID from the delivery_requests table. Each request shows the request ID, date, price, status, pickup, and destination.

### Viewing Active Requests
The dashboard fetches requests with a status of pending, accepted, or in_progress. The customer can filter by status using the toggle buttons.


## Courier Flows

### Registration
Same as customer registration but inserts into the couriers table instead. Couriers also provide their vehicle type during registration.

### Login
Same as customer login but queries the couriers table.

### Viewing Available Jobs
The courier dashboard fetches all delivery requests with a status of pending and no courier assigned yet. These are shown in the Available Jobs tab.

### Accepting a Job
When a courier clicks Accept on a job, the delivery_requests table is updated — the courier's ID is recorded and the status changes from pending to accepted.

### Marking a Job as Complete
When a courier marks a job as complete, the status in the delivery_requests table is updated to completed. This also affects the courier's earnings summary which is recalculated from all completed jobs.

### Earnings Summary
The courier dashboard calculates total earnings and total jobs completed by summing up all delivery_requests rows where the courier is assigned and the status is completed.


## Shared Flows

### Profile Update
Both customers and couriers can update their name, phone, and address from the profile screen. The relevant row in either the customers or couriers table is updated directly.

### Password Change
The new password is hashed using SHA-256 before being saved to the database. The old password field is replaced with the new hash.

### Courier Availability Toggle
Couriers can toggle their availability from the settings screen. This updates the is_available column in the couriers table. Only available couriers appear in the customer's Connect with Couriers section.

### Sign Out
Signing out destroys the current screen and returns the user to the splash screen. No session data is stored — the next login starts fresh.


## Database Query Layer
All database operations go through database/queries.py. This file contains one function per operation, each of which opens a connection, runs the query, commits if needed, closes the connection, and returns the result. The connection itself is managed by database/db_connection.py which reads credentials from the .env file.