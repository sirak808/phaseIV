# Simple Airline Management System (SAMS)

A Flask-based web application backed by a MySQL database that manages airlines, flights, airplanes, airports, and people (passengers and crew). The goal of this project is to practice real-world database design and data management by converting an Enhanced ERD into a normalized relational schema with stored procedures and views.

## Tech Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy
- **Database:** MySQL (with stored procedures and views)
- **ORM / DB Layer:** SQLAlchemy Core + Flask-SQLAlchemy
- **Other:** python-dotenv (for local configuration), HTML/Jinja templates

## Key Features

- Add and manage **airplanes**, **airports**, and **people** through web forms.
- Operational workflows via stored procedures, e.g.:
  - Offering flights  
  - Boarding and disembarking passengers  
  - Assigning pilots and managing licenses  
  - Taking off, landing, and retiring flights
- Read-only **views** for analytics-style queries, such as:
  - `route_summary` (high-level route information)
  - `flights_in_the_air` and `flights_on_the_ground`
  - `people_in_the_air` and `people_on_the_ground`
- Basic health check route (`/test-db`) to verify database connectivity.

## Database Design

The schema (DDL not included in this repo) was designed by:

- Starting from an Enhanced ERD for an airline system.
- Normalizing entities into separate tables (e.g., airlines, airplanes, airports, routes, flights, people, crew assignments).
- Enforcing integrity with primary/foreign keys and constraints.
- Implementing **stored procedures** for multi-step operations (e.g., adding aircraft tied to locations, offering flights, boarding/disembarking) so complex business logic lives close to the data.
- Exposing **views** to provide analytics-friendly, read-optimized slices over the transactional tables.

> Note: The actual SQL DDL and stored procedure definitions were developed as part of the course/project and are assumed to be created in your MySQL instance before running the app.

## Project Structure

```text
phaseIV/
├── app.py                # Flask application factory and blueprint registration
├── extensions.py         # SQLAlchemy `db` instance
├── routes/
│   ├── __init__.py
│   ├── procedures.py     # Routes that call stored procedures
│   ├── views.py          # Routes that query database views (route summary, flights in the air, etc.)
│   └── tests.py          # Simple /test-db route to verify DB connectivity
└── templates/
    ├── home.html         # Landing page
    ├── procedures/       # Templates for procedure-based workflows (add airplane, offer flight, etc.)
    └── views/            # Templates for view pages (flights_in_the_air, flights_on_the_ground, etc.)
