from flask import Blueprint, request, jsonify, session
from app.services.appointment_service import AppointmentService

bp = Blueprint('appointments', __name__)

@bp.before_request
def check_auth():
    if request.method == 'OPTIONS':
        return
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

@bp.route('/appointments', methods=['GET', 'POST'])
def appointments():
    user_id = session['user_id']

    if request.method == 'GET':
        apps = AppointmentService.get_appointments(user_id)
        return jsonify(apps)

    elif request.method == 'POST':
        data = request.get_json()
        AppointmentService.book_appointment(user_id, data)
        return jsonify({'message': 'Appointment booked'})

@bp.route('/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    AppointmentService.cancel_appointment(appointment_id)
    return jsonify({'message': 'Appointment cancelled'})

@bp.route('/search', methods=['GET'])
def search_records():
    user_id = session['user_id']
    results = AppointmentService.search_appointments(user_id, request.args)
    return jsonify(results)
