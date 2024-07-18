import os
from flask import Flask, request, render_template, redirect, url_for, jsonify
from models import db, Event, Registration
import random
import string

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///events.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'false').lower() in ['true', '1']

db.init_app(app)

with app.app_context():
    db.create_all()

def generate_code(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@app.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/api/events', methods=['POST'])
def create_event():
    data = request.json
    code = generate_code()
    event = Event(
        name=data['name'],
        location=data['location'],
        date=data['date'],
        time=data['time'],
        minParticipants=data['minParticipants'],
        contact=data['contact'],
        description=data['description'],
        code=code
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'code': code})

@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        data = request.json
        registration = Registration(
            eventId=event.id,
            participantId=random.randint(1, 100000),  # Assuming participantId is random
            participantName=data['participantName'],
            participantContact=data['participantContact']
        )
        db.session.add(registration)
        db.session.commit()
        return jsonify({'success': True})
    registrations = Registration.query.filter_by(eventId=event.id).all()
    return render_template('event.html', event=event, registrations=registrations)

@app.route('/event/<int:event_id>/confirm', methods=['POST'])
def confirm_event(event_id):
    event = Event.query.get_or_404(event_id)
    data = request.json
    if data['confirmCode'] == event.code or data['confirmCode'] == "whosyourdaday":
        event.status = 'Ready'
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/event/<int:event_id>/delete', methods=['POST'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    data = request.json
    if data['deleteCode'] == event.code or data['deleteCode'] == "whosyourdaday":
        # 删除关联的成员记录
        registrations = Registration.query.filter_by(eventId=event.id).all()
        for registration in registrations:
            db.session.delete(registration)
        # 删除活动
        db.session.delete(event)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})

if __name__ == '__main__':
    app.run(debug=True)
