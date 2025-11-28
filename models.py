from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'jugador', 'ojeador', 'admin'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    player_profile = db.relationship('Player', backref='user', uselist=False)
    scout_profile = db.relationship('Scout', backref='user', uselist=False)
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic')
    messages_received = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date)
    edad = db.Column(db.Integer)
    pais = db.Column(db.String(50))
    ciudad = db.Column(db.String(100))
    deporte = db.Column(db.String(50), nullable=False)
    posicion = db.Column(db.String(50))
    nivel = db.Column(db.String(50))  # amateur, semi-profesional, profesional
    descripcion = db.Column(db.Text)
    altura = db.Column(db.Float)  # en cm
    peso = db.Column(db.Float)  # en kg
    phone_code = db.Column(db.String(10))  # código de país telefónico
    telefono = db.Column(db.String(20))
    sitio_web = db.Column(db.String(200))

    # Relationships
    videos = db.relationship('Video', backref='player', lazy='dynamic')

class Scout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    empresa = db.Column(db.String(100))
    pais = db.Column(db.String(50))
    ciudad = db.Column(db.String(100))
    especialidad = db.Column(db.String(100))  # deportes específicos
    descripcion = db.Column(db.Text)
    phone_code = db.Column(db.String(10))  # código de país telefónico
    telefono = db.Column(db.String(20))
    sitio_web = db.Column(db.String(200))

    # Relationships
    events = db.relationship('Event', backref='scout', lazy='dynamic')

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    tipo = db.Column(db.String(20), nullable=False)  # 'local', 'youtube'
    url = db.Column(db.String(500))  # para YouTube o path local
    filename = db.Column(db.String(200))  # para archivos locales
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scout_id = db.Column(db.Integer, db.ForeignKey('scout.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    fecha = db.Column(db.DateTime, nullable=False)
    ubicacion = db.Column(db.String(200))
    deporte = db.Column(db.String(50))
    capacidad_maxima = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)