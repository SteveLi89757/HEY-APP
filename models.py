from flask_sqlalchemy import SQLAlchemy
import random
import string

db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(10), nullable=False)  # yyyy-mm-dd
    time = db.Column(db.String(5), nullable=False)  # hh:mm
    minParticipants = db.Column(db.Integer, nullable=False)
    contact = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    code = db.Column(db.String(10), nullable=False, default=''.join(random.choices(string.ascii_uppercase + string.digits, k=10)))
    status = db.Column(db.String(20), nullable=False, default='Pending')

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eventId = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    participantId = db.Column(db.Integer, nullable=False)
    participantName = db.Column(db.String(80), nullable=False)
    participantContact = db.Column(db.String(120), nullable=False)
