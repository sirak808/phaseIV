from flask import Blueprint, render_template, request 
from sqlalchemy import text
from extensions import db  # import db instance

views_bp = Blueprint('views', __name__)

@views_bp.route('/route_summary') #no need for methods param because view only needs GET request
def route_summary():
    try:
        result = db.session.execute(text("SELECT * FROM route_summary"))
        routes = result.fetchall()

        #print(f"DEBUG: routes = {routes}")
        return render_template('views/route_summary.html', routes=routes)
    except Exception as e:
        return f"Failed to load upcoming routes: {e}"
    
@views_bp.route('/alternative_airports') #no need for methods param because view only needs GET request
def alternative_airports():
    try:
        result = db.session.execute(text("SELECT * FROM alternative_airports"))
        airports = result.fetchall()

        #print(f"DEBUG: airports = {airports}")
        return render_template('views/alternative_airports.html', airports=airports)
    except Exception as e:
        return f"Failed to load alternative airports: {e}"
    
@views_bp.route('/people_on_the_ground') #no need for methods param because view only needs GET request
def people_on_the_ground():
    try:
        result = db.session.execute(text("SELECT * FROM people_on_the_ground"))
        people = result.fetchall()

        #print(f"DEBUG: airports = {airports}")
        return render_template('views/people_on_the_ground.html', people=people)
    except Exception as e:
        return f"Failed to load people on the ground: {e}"
    
@views_bp.route('/people_in_the_air') #no need for methods param because view only needs GET request
def people_in_the_air():
    try:
        result = db.session.execute(text("SELECT * FROM people_in_the_air"))
        people = result.fetchall()

        #print(f"DEBUG: airports = {airports}")
        return render_template('views/people_in_the_air.html', people=people)
    except Exception as e:
        return f"Failed to load people in the air: {e}"
    
@views_bp.route('/flights_on_the_ground') #no need for methods param because view only needs GET request
def flights_on_the_ground():
    try:
        result = db.session.execute(text("SELECT * FROM flights_on_the_ground"))
        flights = result.fetchall()

        #print(f"DEBUG: airports = {airports}")
        return render_template('views/flights_on_the_ground.html', flights=flights)
    except Exception as e:
        return f"Failed to load flights on the ground: {e}"
    
@views_bp.route('/flights_in_the_air') #no need for methods param because view only needs GET request
def flights_in_the_air():
    try:
        result = db.session.execute(text("SELECT * FROM flights_in_the_air"))
        flights = result.fetchall()

        #print(f"DEBUG: airports = {airports}")
        return render_template('views/flights_in_the_air.html', flights=flights)
    except Exception as e:
        return f"Failed to load flights in the air: {e}"