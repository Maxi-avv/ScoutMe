from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, send_from_directory, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from config import Config
from models import db, User, Player, Scout, Video, Event, Message
from forms import (
    LoginForm, RegisterPlayerForm, RegisterScoutForm, PlayerProfileForm,
    ScoutProfileForm, VideoForm, EventForm, MessageForm, SearchForm
)

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp4', 'mov', 'webm', 'mkv'}

def calculate_age(birth_date):
    if birth_date:
        today = datetime.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return None

# Routes
@app.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.role == 'jugador':
            return redirect(url_for('perfil_jugador'))
        elif current_user.role == 'ojeador':
            return redirect(url_for('perfil_ojeador'))
        elif current_user.role == 'admin':
            return redirect(url_for('admin'))
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        flash('Email o contraseña incorrectos.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register/jugador', methods=['GET', 'POST'])
def register_jugador():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterPlayerForm()
    if form.validate_on_submit():
        try:
            user = User(email=form.email.data, role='jugador')
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            player = Player(
                user_id=user.id,
                nombre=form.nombre.data,
                apellido=form.apellido.data,
                fecha_nacimiento=form.fecha_nacimiento.data,
                pais=form.pais.data,
                ciudad=form.ciudad.data,
                deporte=form.deporte.data,
                posicion=form.posicion.data,
                nivel=form.nivel.data,
                descripcion=form.descripcion.data,
                altura=form.altura.data,
                peso=form.peso.data,
                phone_code=form.phone_code.data,
                telefono=form.telefono.data,
                sitio_web=form.sitio_web.data
            )
            if player.fecha_nacimiento:
                player.edad = calculate_age(player.fecha_nacimiento)
            db.session.add(player)
            db.session.commit()

            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error en el registro: {str(e)}', 'danger')
            print(f'Registration error: {str(e)}')  # Debug log
    else:
        # Debug: print form errors
        if request.method == 'POST':
            print("Form validation errors:")
            for field, errors in form.errors.items():
                print(f"{field}: {errors}")
            flash('Por favor corrige los errores en el formulario.', 'warning')
    return render_template('register_jugador.html', form=form)

@app.route('/register/ojeador', methods=['GET', 'POST'])
def register_ojeador():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterScoutForm()
    if form.validate_on_submit():
        try:
            user = User(email=form.email.data, role='ojeador')
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            scout = Scout(
                user_id=user.id,
                nombre=form.nombre.data,
                apellido=form.apellido.data,
                empresa=form.empresa.data,
                pais=form.pais.data,
                ciudad=form.ciudad.data,
                especialidad=form.especialidad.data,
                descripcion=form.descripcion.data,
                phone_code=form.phone_code.data,
                telefono=form.telefono.data,
                sitio_web=form.sitio_web.data
            )
            db.session.add(scout)
            db.session.commit()

            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error en el registro: {str(e)}', 'danger')
            print(f'Registration error: {str(e)}')  # Debug log
    else:
        # Debug: print form errors
        if request.method == 'POST':
            print("Form validation errors:")
            for field, errors in form.errors.items():
                print(f"{field}: {errors}")
            flash('Por favor corrige los errores en el formulario.', 'warning')
    return render_template('register_ojeador.html', form=form)

@app.route('/perfil/jugador', methods=['GET', 'POST'])
@login_required
def perfil_jugador():
    if current_user.role != 'jugador':
        abort(403)
    player = current_user.player_profile
    form = PlayerProfileForm(obj=player)
    if form.validate_on_submit():
        form.populate_obj(player)
        if player.fecha_nacimiento:
            player.edad = calculate_age(player.fecha_nacimiento)
        db.session.commit()
        flash('Perfil actualizado exitosamente.', 'success')
        return redirect(url_for('perfil_jugador'))
    return render_template('perfil_jugador.html', form=form, player=player)

@app.route('/perfil/ojeador', methods=['GET', 'POST'])
@login_required
def perfil_ojeador():
    if current_user.role != 'ojeador':
        abort(403)
    scout = current_user.scout_profile
    form = ScoutProfileForm(obj=scout)
    if form.validate_on_submit():
        form.populate_obj(scout)
        db.session.commit()
        flash('Perfil actualizado exitosamente.', 'success')
        return redirect(url_for('perfil_ojeador'))
    return render_template('perfil_ojeador.html', form=form, scout=scout)

@app.route('/buscar', methods=['GET', 'POST'])
@login_required
def buscar():
    form = SearchForm(request.args)
    players = Player.query

    if form.deporte.data:
        players = players.filter_by(deporte=form.deporte.data)
    if form.posicion.data:
        players = players.filter(Player.posicion.contains(form.posicion.data))
    if form.edad_min.data:
        players = players.filter(Player.edad >= form.edad_min.data)
    if form.edad_max.data:
        players = players.filter(Player.edad <= form.edad_max.data)
    if form.pais.data:
        players = players.filter(Player.pais.contains(form.pais.data))
    if form.ciudad.data:
        players = players.filter(Player.ciudad.contains(form.ciudad.data))
    if form.nivel.data:
        players = players.filter_by(nivel=form.nivel.data)

    players = players.all()
    return render_template('buscar.html', form=form, players=players)

@app.route('/eventos')
@login_required
def eventos():
    events = Event.query.order_by(Event.fecha.desc()).all()
    return render_template('eventos.html', events=events)

@app.route('/evento/<int:event_id>')
@login_required
def evento_detalle(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('evento_detalle.html', event=event)

@app.route('/evento/crear', methods=['GET', 'POST'])
@login_required
def crear_evento():
    if current_user.role != 'ojeador':
        abort(403)
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            scout_id=current_user.scout_profile.id,
            titulo=form.titulo.data,
            descripcion=form.descripcion.data,
            fecha=form.fecha.data,
            ubicacion=form.ubicacion.data,
            deporte=form.deporte.data,
            capacidad_maxima=form.capacidad_maxima.data
        )
        db.session.add(event)
        db.session.commit()
        flash('Evento creado exitosamente.', 'success')
        return redirect(url_for('eventos'))
    return render_template('crear_evento.html', form=form)

@app.route('/mensajes')
@login_required
def mensajes():
    received_messages = current_user.messages_received.order_by(Message.sent_at.desc()).all()
    return render_template('mensajes.html', messages=received_messages)

@app.route('/mensaje/enviar', methods=['GET', 'POST'])
@login_required
def enviar_mensaje():
    form = MessageForm()
    # Populate receiver choices
    users = User.query.filter(User.id != current_user.id).all()
    form.receiver_id.choices = [(u.id, f"{u.email} ({u.role})") for u in users]

    if form.validate_on_submit():
        message = Message(
            sender_id=current_user.id,
            receiver_id=form.receiver_id.data,
            subject=form.subject.data,
            content=form.content.data
        )
        db.session.add(message)
        db.session.commit()
        flash('Mensaje enviado exitosamente.', 'success')
        return redirect(url_for('mensajes'))
    return render_template('enviar_mensaje.html', form=form)

@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin':
        abort(403)
    users = User.query.all()
    return render_template('admin.html', users=users)

# API Routes
@app.route('/api/buscar')
def api_buscar():
    deporte = request.args.get('deporte')
    ciudad = request.args.get('ciudad')
    players = Player.query
    if deporte:
        players = players.filter_by(deporte=deporte)
    if ciudad:
        players = players.filter(Player.ciudad.contains(ciudad))
    players = players.all()
    result = {
        'jugadores': [{
            'id': p.id,
            'nombre': f"{p.nombre} {p.apellido}",
            'deporte': p.deporte,
            'posicion': p.posicion,
            'edad': p.edad,
            'pais': p.pais,
            'ciudad': p.ciudad,
            'nivel': p.nivel,
            'descripcion': p.descripcion
        } for p in players],
        'total': len(players),
        'pagina': 1,
        'por_pagina': 20
    }
    return jsonify(result)

# Video upload
@app.route('/video/subir', methods=['GET', 'POST'])
@login_required
def subir_video():
    if current_user.role != 'jugador':
        abort(403)
    form = VideoForm()
    if form.validate_on_submit():
        if form.tipo.data == 'youtube':
            video = Video(
                player_id=current_user.player_profile.id,
                titulo=form.titulo.data,
                descripcion=form.descripcion.data,
                tipo='youtube',
                url=form.url.data
            )
        else:
            if 'archivo' not in request.files:
                flash('No se seleccionó archivo', 'danger')
                return redirect(request.url)
            file = request.files['archivo']
            if file.filename == '':
                flash('No se seleccionó archivo', 'danger')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = app.config['UPLOAD_FOLDER']
                os.makedirs(upload_folder, exist_ok=True)
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                video = Video(
                    player_id=current_user.player_profile.id,
                    titulo=form.titulo.data,
                    descripcion=form.descripcion.data,
                    tipo='local',
                    filename=filename
                )
        db.session.add(video)
        db.session.commit()
        flash('Video subido exitosamente.', 'success')
        return redirect(url_for('perfil_jugador'))
    return render_template('subir_video.html', form=form)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run()