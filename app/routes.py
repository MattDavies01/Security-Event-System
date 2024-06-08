from flask import Blueprint, request, jsonify
from .models import SecurityEvent, db

main = Blueprint('main', __name__)

@main.route('/events', nethods=['POST'])
def log_event():
    data = request.get_json()
    new_event = SecurityEvent(
        event_type=data['event_type'],
        description=data['description']
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'message': 'Event logged successfully!'}), 201

@main.route('/events', methods=['GET'])
def get_events():
    events = SecurityEvent.query.all()
    result = [{'id': event.id, 'event_type': event.event_type, 'description': event.description, 'timestamp': event.timestamp} for event in events]
    return jsonify(result)

@main.route('/events/<int:id>', methods=['GET'])
def get_event(id):
    event = SecurityEvent.query.get_or_404(id)
    result = {'id': event.id, 'event_type': event.event_type, 'description': event.description, 'timestamp': event.timestamp}
    return jsonify(result)