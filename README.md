# kayakonnect-system

Group 7's CA3 for COS 102

** Course: COS 102: Introduction to Problem Solving

** Institution: Pan Atlantic University

** Date: May 2026

KAYAKONNECT

** Prepared By:
 - David Offor
 - Sean Iriogbe
 - Alore Paul
 - Kachi Chukwuneke
 - Daniel Emezi
 - Dahunsi Yusuf

### project structure
    database/
    models/
    services/
    ui/
    assets/
    docs/

### setup instructions:
Installation:
- pip install customtkinter
- pip install pyscopg2
- pip install pillow

### Run instructions
- python main.py

KayaKonnect is a market courier coordination system designed to connect customers in Lagos markets with available kaya workers for transporting goods from shops to parking areas or loading points.

In many Lagos markets, customers experience difficulty transporting purchased goods due to the informal and unstructured nature of kaya services. Pricing inconsistencies, lack of accountability, and inefficient courier allocation create inconvenience for both customers and kaya workers.

Kaya workers also lack structured job opportunities and incentive systems that can improve their daily earnings and productivity.

KayaKonnect isnt just an app, but an ecosystem that transparently and effectively provides courier request management, fare negotiation, job tracking, incentive systems, and intelligent fare recommendation features. We aim to digitize and organize this process through a centralized courier coordination platform.

** Objectives:

General Objective:
- To design and implement a market courier coordination system

Specific Objective:
1. To allow customers to request courier services within markets.

2. To enable kaya workers to accept delivery jobs.

3. To provide a fare negotiation system between customers and couriers.

4. To implement a courier incentive and bonus system.

5. To store and manage courier and customer data securely.

6. To provide intelligent fare estimation based on delivery conditions.

** Target Users:
- Market Customers
- Kaya workers (couriers)
- Market administrators

** Functional Requirements:
The system shall:

- Allow users to register and log in.
- Allow customers to create delivery requests.
- Allow couriers to view available jobs.
- Allow fare negotiation between users.
- Track completed jobs.
- Calculate courier bonuses automatically.
- Store user records in PostgreSQL.
- Display courier earnings and statistics.

** Non-functional Requirements:
- The system should be easy to use.
- The interface should be responsive.
- User data should be stored securely.
- The system should support multiple users.
- The application should minimize processing delays.

** System Architecture
- Frontent: Python CustomTkinter GUI
- Backend Logic: Python
- Database: PostgreSQL
- Database Connectivity: pycopg2 library
- Collaboration Management: Git & Github
- UI Design - Figma

* Intelligent Component:
    This system incorporates an intelligent fare estimation module that recommends fair pricing based on delivery distance, load size and urgency.

* Future Improvements:
Future versions may include:
- Mobile application integration
- Real time GPS tracking
- SMS notifications
- Advanced machine learning prediction models

* Conclusion:
    - KayaKonnect provides a structured and technology-driven solution to improve market courier services in Lagos markets. The system enhances convenience, organization, accountability, and earning opportunities for kaya workers while improving customer experience.