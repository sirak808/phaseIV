from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import text, exc
from extensions import db
import traceback
import datetime

procedures_bp = Blueprint('procedures', __name__, template_folder='../templates/procedures')

@procedures_bp.route('/add_airplane', methods=['GET', 'POST'])
def add_airplane():
    if request.method == 'POST':
        airline_id = request.form.get('airlineID')
        tail_num = request.form.get('tail_num')
        seat_capacity_str = request.form.get('seat_capacity')
        speed_str = request.form.get('speed')
        location_id = request.form.get('locationID')
        plane_type = request.form.get('plane_type')
        maintenanced_checkbox = request.form.get('maintenanced')
        model = request.form.get('model')
        neo_checkbox = request.form.get('neo')
        params = {}
        validation_error = False
        if not all([airline_id, tail_num, seat_capacity_str, speed_str, location_id]):
            flash('Missing required fields.', 'danger')
            validation_error = True
        try:
            if seat_capacity_str:
                 params['seat_capacity'] = int(seat_capacity_str)
                 if params['seat_capacity'] <= 0: raise ValueError("Seat capacity must be positive.")
            else: raise ValueError("Seat capacity is required.")
            if speed_str:
                 params['speed'] = int(speed_str)
                 if params['speed'] <= 0: raise ValueError("Speed must be positive.")
            else: raise ValueError("Speed is required.")
        except ValueError as ve:
            flash(f'Seat Capacity and Speed must be valid positive integers. Error: {ve}', 'danger')
            validation_error = True
        params['airlineID'] = airline_id
        params['tail_num'] = tail_num
        params['locationID'] = location_id
        params['plane_type'] = plane_type if plane_type else None
        params['maintenanced'] = True if maintenanced_checkbox == 'on' and params['plane_type'] == 'Boeing' else None
        params['model'] = model if model and params['plane_type'] == 'Boeing' else None
        params['neo'] = True if neo_checkbox == 'on' and params['plane_type'] == 'Airbus' else None
        if not validation_error:
            try:
                sql = text("""
                    CALL add_airplane(:airlineID, :tail_num, :seat_capacity, :speed, :locationID,:plane_type, :maintenanced, :model, :neo)
                """)
                db.session.execute(sql, params)
                loc_check_sql = text("SELECT 1 FROM location WHERE locationID = :loc_id LIMIT 1")
                plane_check_sql = text("SELECT 1 FROM airplane WHERE airlineID = :a_id AND tail_num = :t_num LIMIT 1")
                location_added = db.session.execute(loc_check_sql, {"loc_id": location_id}).fetchone()
                airplane_added = db.session.execute(plane_check_sql, {"a_id": airline_id, "t_num": tail_num}).fetchone()
                if location_added is not None and airplane_added is not None:
                    db.session.commit()
                    flash('Airplane added successfully!', 'success')
                else:
                    db.session.rollback()
                    flash('Operation failed: Airplane not added. Input may violate constraints or duplicate exists.', 'danger')
            except exc.SQLAlchemyError as e:
                db.session.rollback(); print(f"DB Error add_airplane: {e}"); print(traceback.format_exc()); flash(f'DB error: {e}', 'danger')
            except Exception as e:
                 db.session.rollback(); print(f"Unexpected Error add_airplane: {e}"); print(traceback.format_exc()); flash(f'App error: {e}', 'danger')
        return redirect(url_for('procedures.add_airplane'))
    return render_template('add_airplane.html')


@procedures_bp.route('/add_airport', methods=['GET', 'POST'])
def add_airport():
    if request.method == 'POST':
        airport_id = request.form.get('airportID')
        airport_name = request.form.get('airport_name')
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')
        location_id = request.form.get('locationID')
        params = {}
        validation_error = False
        if not all([airport_id, city, state, country, location_id]):
            flash('Missing required fields (Airport ID, City, State, Country, Location ID).', 'danger'); validation_error = True
        elif len(airport_id) != 3:
             flash('Airport ID must be exactly 3 characters.', 'danger'); validation_error = True
        elif country and len(country) != 3:
             flash('Country Code must be exactly 3 characters.', 'danger'); validation_error = True
        if not validation_error:
            params['ip_airportID'] = airport_id
            params['ip_airport_name'] = airport_name if airport_name else None
            params['ip_city'] = city
            params['ip_state'] = state
            params['ip_country'] = country
            params['ip_locationID'] = location_id
            try:
                sql = text("CALL add_airport(:ip_airportID, :ip_airport_name, :ip_city, :ip_state, :ip_country, :ip_locationID)")
                db.session.execute(sql, params)
                loc_check_sql = text("SELECT 1 FROM location WHERE locationID = :loc_id LIMIT 1")
                airport_check_sql = text("SELECT 1 FROM airport WHERE airportID = :ap_id LIMIT 1")
                location_added = db.session.execute(loc_check_sql, {"loc_id": location_id}).fetchone()
                airport_added = db.session.execute(airport_check_sql, {"ap_id": airport_id}).fetchone()
                if location_added is not None and airport_added is not None:
                    db.session.commit(); flash(f'Airport {airport_id} added successfully!', 'success')
                else:
                    db.session.rollback(); flash(f'Operation failed: Airport {airport_id} not added. Input may violate constraints or duplicate exists.', 'danger')
            except exc.SQLAlchemyError as e:
                db.session.rollback(); print(f"DB Error add_airport: {e}"); print(traceback.format_exc()); flash(f'DB error: {e}', 'danger')
            except Exception as e:
                 db.session.rollback(); print(f"Unexpected Error add_airport: {e}"); print(traceback.format_exc()); flash(f'App error: {e}', 'danger')
        return redirect(url_for('procedures.add_airport'))
    return render_template('add_airport.html')


@procedures_bp.route('/add_person', methods=['GET', 'POST'])
def add_person():
    if request.method == 'POST':
        person_id = request.form.get('personID')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        location_id = request.form.get('locationID')
        tax_id = request.form.get('taxID')
        experience_str = request.form.get('experience')
        miles_str = request.form.get('miles')
        funds_str = request.form.get('funds')
        params = {}; person_type = None; validation_error = False
        if not all([person_id, first_name, location_id]): flash('Missing required fields (Person ID, First Name, Location ID).', 'danger'); validation_error = True
        is_pilot_attempt = bool(tax_id or experience_str); is_passenger_attempt = bool(miles_str or funds_str)
        if is_pilot_attempt and is_passenger_attempt: flash('Error: Provide details for EITHER Pilot OR Passenger, not both.', 'danger'); validation_error = True
        elif not is_pilot_attempt and not is_passenger_attempt: flash('Error: Must provide details for either Pilot (Tax ID, Experience) OR Passenger (Miles, Funds).', 'danger'); validation_error = True
        elif is_pilot_attempt:
            person_type = 'pilot'
            if not tax_id or not experience_str: flash('Error: For Pilot role, both Tax ID and Experience are required.', 'danger'); validation_error = True
            try:
                params['ip_experience'] = int(experience_str) if experience_str else None; params['ip_taxID'] = tax_id; params['ip_miles'] = None; params['ip_funds'] = None
                if params['ip_experience'] is not None and params['ip_experience'] < 0: flash('Pilot experience cannot be negative.', 'danger'); validation_error = True
            except ValueError: flash('Pilot experience must be a valid integer.', 'danger'); validation_error = True
        elif is_passenger_attempt:
            person_type = 'passenger'
            if not miles_str or not funds_str: flash('Error: For Passenger role, both Miles and Funds are required.', 'danger'); validation_error = True
            try:
                params['ip_miles'] = int(miles_str) if miles_str else None; params['ip_funds'] = int(funds_str) if funds_str else None; params['ip_taxID'] = None; params['ip_experience'] = None
                if (params['ip_miles'] is not None and params['ip_miles'] < 0) or \
                   (params['ip_funds'] is not None and params['ip_funds'] < 0): flash('Miles and Funds cannot be negative.', 'danger'); validation_error = True
            except ValueError: flash('Miles and Funds must be valid integers.', 'danger'); validation_error = True
        if not validation_error:
            params['ip_personID'] = person_id; params['ip_first_name'] = first_name; params['ip_last_name'] = last_name if last_name else None; params['ip_locationID'] = location_id
            try:
                sql = text("CALL add_person(:ip_personID, :ip_first_name, :ip_last_name, :ip_locationID, :ip_taxID, :ip_experience, :ip_miles, :ip_funds)")
                db.session.execute(sql, params)
                person_check_sql = text("SELECT 1 FROM person WHERE personID = :p_id LIMIT 1"); person_added = db.session.execute(person_check_sql, {"p_id": person_id}).fetchone()
                role_added = None
                if person_type == 'pilot': role_check_sql = text("SELECT 1 FROM pilot WHERE personID = :p_id LIMIT 1"); role_added = db.session.execute(role_check_sql, {"p_id": person_id}).fetchone()
                elif person_type == 'passenger': role_check_sql = text("SELECT 1 FROM passenger WHERE personID = :p_id LIMIT 1"); role_added = db.session.execute(role_check_sql, {"p_id": person_id}).fetchone()
                if person_added is not None and role_added is not None:
                    db.session.commit(); flash(f'{person_type.capitalize()} {first_name} ({person_id}) added successfully!', 'success')
                else:
                    db.session.rollback(); flash(f'Operation failed: Person {person_id} not added. Input may violate constraints, location may not exist, or duplicate ID.', 'danger')
            except exc.IntegrityError as ie: db.session.rollback(); print(f"DB Integrity Error add_person: {ie}"); print(traceback.format_exc()); flash(f'DB integrity error: {ie}', 'danger')
            except exc.SQLAlchemyError as e: db.session.rollback(); print(f"DB Error add_person: {e}"); print(traceback.format_exc()); flash(f'DB error: {e}', 'danger')
            except Exception as e: db.session.rollback(); print(f"Unexpected Error add_person: {e}"); print(traceback.format_exc()); flash(f'App error: {e}', 'danger')
        return redirect(url_for('procedures.add_person'))
    return render_template('add_person.html')


@procedures_bp.route('/grant_revoke_license', methods=['GET', 'POST'])
def grant_revoke_license():
    if request.method == 'POST':
        person_id = request.form.get('personID')
        license_name = request.form.get('license')
        params = {}
        validation_error = False

        if not all([person_id, license_name]):
            flash('Missing required fields (Person ID, License).', 'danger')
            validation_error = True

        if not validation_error:
            params['ip_personID'] = person_id
            params['ip_license'] = license_name

            pilot_check_sql = text("SELECT 1 FROM pilot WHERE personID = :p_id LIMIT 1")
            license_check_sql = text("SELECT 1 FROM pilot_licenses WHERE personID = :p_id AND license = :lic LIMIT 1")

            try:
                is_pilot = db.session.execute(pilot_check_sql, {"p_id": person_id}).fetchone()
                if is_pilot is None:
                    flash(f'Operation failed: Person ID {person_id} is not a valid pilot.', 'danger')
                    return redirect(url_for('procedures.grant_revoke_license'))

                lic_result_before = db.session.execute(license_check_sql, {"p_id": person_id, "lic": license_name}).fetchone()
                had_license_before = (lic_result_before is not None)

                sql = text("CALL grant_or_revoke_pilot_license(:ip_personID, :ip_license)")
                db.session.execute(sql, params)

                lic_result_after = db.session.execute(license_check_sql, {"p_id": person_id, "lic": license_name}).fetchone()
                has_license_now = (lic_result_after is not None)

                action_message = ""
                if not had_license_before and has_license_now:
                    action_message = f'License "{license_name}" GRANTED for pilot {person_id}.'
                    flash(action_message, 'success')
                    db.session.commit() 
                elif had_license_before and not has_license_now:
                    action_message = f'License "{license_name}" REVOKED for pilot {person_id}.'
                    flash(action_message, 'success')
                    db.session.commit() 
                else:
                    action_message = f'License "{license_name}" status UNCHANGED for pilot {person_id}. Check inputs or DB state.'
                    flash(action_message, 'warning')
                    db.session.rollback() 

            except exc.SQLAlchemyError as e: 
                db.session.rollback()
                print(f"Database Error during CALL grant_or_revoke_pilot_license or checks: {e}")
                print(traceback.format_exc())
                flash(f'Database error occurred: {e}', 'danger')
            except Exception as e:
                 db.session.rollback()
                 print(f"Unexpected Error: {e}")
                 print(traceback.format_exc())
                 flash(f'An unexpected error occurred: {e}', 'danger')

        return redirect(url_for('procedures.grant_revoke_license'))

    return render_template('grant_revoke_license.html')


@procedures_bp.route('/offer_flight', methods=['GET', 'POST'])
def offer_flight():
    if request.method == 'POST':
        flight_id = request.form.get('flightID'); route_id = request.form.get('routeID')
        support_airline = request.form.get('support_airline'); support_tail = request.form.get('support_tail')
        progress_str = request.form.get('progress'); next_time_str = request.form.get('next_time'); cost_str = request.form.get('cost')
        params = {}; validation_error = False
        if not all([flight_id, route_id, progress_str, next_time_str, cost_str]): flash('Missing required fields (Flight ID, Route ID, Progress, Next Time, Cost).', 'danger'); validation_error = True
        try:
            if progress_str: params['ip_progress'] = int(progress_str); 
            else: raise ValueError("Progress is required.")
            if cost_str: params['ip_cost'] = int(cost_str); 
            else: raise ValueError("Cost is required.")
            if next_time_str:
                try:
                    parts = next_time_str.split(':')
                    params['ip_next_time'] = datetime.datetime.strptime(next_time_str, '%H:%M:%S').time()
                except ValueError:
                    raise ValueError("Next Time must be in HH:MM:SS format.")
            else:
                raise ValueError("Next Time is required.")
        except ValueError as ve: flash(f'Invalid numeric or time input. Error: {ve}', 'danger'); validation_error = True
        if not validation_error:
            params['ip_flightID'] = flight_id; params['ip_routeID'] = route_id
            params['ip_support_airline'] = support_airline if support_airline else None
            params['ip_support_tail'] = support_tail if support_tail else None
            try:
                sql = text("CALL offer_flight(:ip_flightID, :ip_routeID, :ip_support_airline, :ip_support_tail, :ip_progress, :ip_next_time, :ip_cost)")
                db.session.execute(sql, params)
                flight_check_sql = text("SELECT 1 FROM flight WHERE flightID = :f_id LIMIT 1"); flight_added = db.session.execute(flight_check_sql, {"f_id": flight_id}).fetchone()
                if flight_added is not None: db.session.commit(); flash(f'Flight {flight_id} offered successfully!', 'success')
                else: db.session.rollback(); flash(f'Operation failed: Flight {flight_id} not offered. Input may violate constraints (e.g., duplicate Flight ID, invalid Route/Airplane, progress invalid).', 'danger')
            except exc.SQLAlchemyError as e: db.session.rollback(); print(f"DB Error offer_flight: {e}"); print(traceback.format_exc()); flash(f'DB error: {e}', 'danger')
            except Exception as e: db.session.rollback(); print(f"Unexpected Error offer_flight: {e}"); print(traceback.format_exc()); flash(f'App error: {e}', 'danger')
        return redirect(url_for('procedures.offer_flight'))
    return render_template('offer_flight.html')


@procedures_bp.route('/flight_landing', methods=['GET', 'POST'])
def flight_landing():
    if request.method == 'POST':
        flight_id = request.form.get('flightID'); params = {}; validation_error = False
        if not flight_id: flash('Missing required field (Flight ID).', 'danger'); validation_error = True
        if not validation_error:
            params['ip_flightID'] = flight_id
            try:
                sql = text("CALL flight_landing(:ip_flightID)"); db.session.execute(sql, params)
                status_check_sql = text("SELECT airplane_status FROM flight WHERE flightID = :f_id"); result = db.session.execute(status_check_sql, {"f_id": flight_id}).fetchone()
                if result is not None and result[0] == 'on_ground': db.session.commit(); flash(f'Flight {flight_id} landing processed successfully.', 'success')
                else:
                    db.session.rollback(); status_msg = f"status '{result[0]}'" if result else "flight not found"
                    flash(f'Operation failed for flight {flight_id}. Expected status "on_ground" but found {status_msg}. Was it "in_flight"?', 'danger')
            except exc.SQLAlchemyError as e: db.session.rollback(); print(f"DB Error flight_landing: {e}"); print(traceback.format_exc()); flash(f'DB error for {flight_id}: {e}', 'danger')
            except Exception as e: db.session.rollback(); print(f"Unexpected Error flight_landing: {e}"); print(traceback.format_exc()); flash(f'App error: {e}', 'danger')
        return redirect(url_for('procedures.flight_landing'))
    return render_template('flight_landing.html')


@procedures_bp.route('/flight_takeoff', methods=['GET', 'POST'])
def flight_takeoff():
    if request.method == 'POST':
        flight_id = request.form.get('flightID'); params = {}; validation_error = False
        if not flight_id: flash('Missing required field (Flight ID).', 'danger'); validation_error = True
        if not validation_error:
            params['ip_flightID'] = flight_id
            try:
                sql = text("CALL flight_takeoff(:ip_flightID)"); db.session.execute(sql, params)
                status_check_sql = text("SELECT airplane_status, progress, next_time FROM flight WHERE flightID = :f_id"); post_result = db.session.execute(status_check_sql, {"f_id": flight_id}).fetchone()
                if post_result is None: db.session.rollback(); flash(f'Operation failed: Flight {flight_id} not found.', 'danger')
                elif post_result[0] == 'in_flight': db.session.commit(); flash(f'Flight {flight_id} takeoff processed successfully.', 'success')
                elif post_result[0] == 'on_ground': db.session.commit(); flash(f'Flight {flight_id} takeoff processed, but flight remains "on_ground". Check pilot count or route status.', 'warning')
                else: db.session.rollback(); flash(f'Operation failed for flight {flight_id}: Unexpected status "{post_result[0]}" after takeoff attempt.', 'danger')
            except exc.SQLAlchemyError as e: db.session.rollback(); print(f"DB Error flight_takeoff: {e}"); print(traceback.format_exc()); flash(f'DB error for {flight_id}: {e}', 'danger')
            except Exception as e: db.session.rollback(); print(f"Unexpected Error flight_takeoff: {e}"); print(traceback.format_exc()); flash(f'App error: {e}', 'danger')
        return redirect(url_for('procedures.flight_takeoff'))
    return render_template('flight_takeoff.html')

@procedures_bp.route('/passengers_board', methods=['GET', 'POST'])
def passengers_board():
    if request.method == 'POST':
        flight_id = request.form.get('flightID'); params = {}; validation_error = False
        if not flight_id: flash('Missing required field (Flight ID).', 'danger'); validation_error = True
        if not validation_error:
            params['ip_flightID'] = flight_id
            try:
                sql = text("CALL passengers_board(:ip_flightID)"); db.session.execute(sql, params)
                status_check_sql = text("SELECT airplane_status, progress, next_time FROM flight WHERE flightID = :f_id"); post_result = db.session.execute(status_check_sql, {"f_id": flight_id}).fetchone()
                if post_result is None: db.session.rollback(); flash(f'Operation failed: Flight {flight_id} not found.', 'danger')
                elif post_result[0] == 'in_flight': db.session.commit(); flash(f'Flight {flight_id} still in flight, cannot board at this time.', 'failure')
                #elif post_result[0] == 'on_ground': db.session.commit(); flash(f'Flight {flight_id} takeoff processed, but flight remains "on_ground". Check pilot count or route status.', 'warning')
                #lse: db.session.rollback(); flash(f'Operation failed for flight {flight_id}: Unexpected status "{post_result[0]}" after takeoff attempt.', 'danger')
            except exc.SQLAlchemyError as e: db.session.rollback(); print(f"DB Error passengers_board: {e}"); print(traceback.format_exc()); flash(f'DB error for {flight_id}: {e}', 'danger')
            except Exception as e: db.session.rollback(); print(f"Unexpected Error passengers_board: {e}"); print(traceback.format_exc()); flash(f'App error: {e}', 'danger')
        return redirect(url_for('procedures.passengers_board'))
    return render_template('passengers_board.html')

@procedures_bp.route('/passengers_disembark', methods=['GET', 'POST'])
def passengers_disembark():
    if request.method == 'POST':
        flight_id = request.form.get('flightID'); params = {}; validation_error = False
        if not flight_id: flash('Missing required field (Flight ID).', 'danger'); validation_error = True
        if not validation_error:
            params['ip_flightID'] = flight_id
            try:
                sql = text("CALL passengers_disembark(:ip_flightID)"); db.session.execute(sql, params)
                status_check_sql = text("SELECT airplane_status, progress, next_time FROM flight WHERE flightID = :f_id"); post_result = db.session.execute(status_check_sql, {"f_id": flight_id}).fetchone()
                if post_result is None: db.session.rollback(); flash(f'Operation failed: Flight {flight_id} not found.', 'danger')
                elif post_result[0] == 'in_flight': db.session.commit(); flash(f'Flight {flight_id} still in flight, cannot disembark at this time.', 'failure')
                #elif post_result[0] == 'on_ground': db.session.commit(); flash(f'Flight {flight_id} takeoff processed, but flight remains "on_ground". Check pilot count or route status.', 'warning')
                #lse: db.session.rollback(); flash(f'Operation failed for flight {flight_id}: Unexpected status "{post_result[0]}" after takeoff attempt.', 'danger')
            except exc.SQLAlchemyError as e: db.session.rollback(); print(f"DB Error passengers_disembark: {e}"); print(traceback.format_exc()); flash(f'DB error for {flight_id}: {e}', 'danger')
            except Exception as e: db.session.rollback(); print(f"Unexpected Error passengers_disembark: {e}"); print(traceback.format_exc()); flash(f'App error: {e}', 'danger')
        return redirect(url_for('procedures.passengers_disembark'))
    return render_template('passengers_disembark.html')
