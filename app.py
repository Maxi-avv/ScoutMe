from flask import (
    Flask, render_template, redirect, url_for, flash,
    request, jsonify, send_from_directory, abort
)
from flask_login import (
    LoginManager, login_user, login_required,
    logout_user, current_user
)
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from config import Config
from models import db, User, Player, Scout, Video, Event, Message
from forms import (
    LoginForm, RegisterPlayerForm, RegisterScoutForm,
    PlayerProfileForm, ScoutProfileForm, VideoForm,
    EventForm, MessageForm, ReplyForm, SearchForm
)

# --------------------------------------------------
# CONFIGURACIÓN BÁSICA
# --------------------------------------------------
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# --------------------------------------------------
# LOGIN MANAGER
# --------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in {"mp4", "mov", "webm", "mkv"}
    )


def calculate_age(birth_date):
    if birth_date:
        today = datetime.today()
        return today.year - birth_date.year - (
            (today.month, today.day) <
            (birth_date.month, birth_date.day)
        )
    return None


# --------------------------------------------------
# RUTAS PRINCIPALES
# --------------------------------------------------
@app.route("/")
def home():
    if current_user.is_authenticated:
        if current_user.role == "jugador":
            return redirect(url_for("perfil_jugador"))
        if current_user.role == "ojeador":
            return redirect(url_for("perfil_ojeador"))
        if current_user.role == "admin":
            return redirect(url_for("admin"))
    return render_template("home.html")


# --------------------------------------------------
# LOGIN
# --------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("home"))

        flash("Email o contraseña incorrectos.", "danger")

    return render_template("login.html", form=form)


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


# --------------------------------------------------
# REGISTRO JUGADOR
# --------------------------------------------------
@app.route("/register/jugador", methods=["GET", "POST"])
def register_jugador():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegisterPlayerForm()

    if form.validate_on_submit():
        try:
            # Crear usuario
            user = User(email=form.email.data, role="jugador")
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            # Crear perfil de jugador
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
                sitio_web=form.sitio_web.data,
            )

            if player.fecha_nacimiento:
                player.edad = calculate_age(player.fecha_nacimiento)

            db.session.add(player)
            db.session.commit()

            flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for("login"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error en el registro: {str(e)}", "danger")
            print("Registro jugador error:", e)

    return render_template("register_jugador.html", form=form)


# --------------------------------------------------
# REGISTRO OJEADOR
# --------------------------------------------------
@app.route("/register/ojeador", methods=["GET", "POST"])
def register_ojeador():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegisterScoutForm()

    if form.validate_on_submit():
        try:
            user = User(email=form.email.data, role="ojeador")
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
                sitio_web=form.sitio_web.data,
            )

            db.session.add(scout)
            db.session.commit()

            flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for("login"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error en el registro: {str(e)}", "danger")
            print("Registro ojeador error:", e)

    return render_template("register_ojeador.html", form=form)


# --------------------------------------------------
# PERFIL JUGADOR
# --------------------------------------------------
@app.route("/perfil/jugador", methods=["GET", "POST"])
@login_required
def perfil_jugador():
    if current_user.role != "jugador":
        abort(403)

    player = current_user.player_profile
    form = PlayerProfileForm(obj=player)

    if form.validate_on_submit():
        form.populate_obj(player)

        if player.fecha_nacimiento:
            player.edad = calculate_age(player.fecha_nacimiento)

        db.session.commit()
        flash("Perfil actualizado exitosamente.", "success")
        return redirect(url_for("perfil_jugador"))

    return render_template("perfil_jugador.html", form=form, player=player)


# --------------------------------------------------
# PERFIL OJEADOR
# --------------------------------------------------
@app.route("/perfil/ojeador", methods=["GET", "POST"])
@login_required
def perfil_ojeador():
    if current_user.role != "ojeador":
        abort(403)

    scout = current_user.scout_profile
    form = ScoutProfileForm(obj=scout)

    if form.validate_on_submit():
        form.populate_obj(scout)
        db.session.commit()

        flash("Perfil actualizado exitosamente.", "success")
        return redirect(url_for("perfil_ojeador"))

    return render_template("perfil_ojeador.html", form=form, scout=scout)


# --------------------------------------------------
# BUSCADOR
# --------------------------------------------------
@app.route("/buscar", methods=["GET", "POST"])
@login_required
def buscar():
    form = SearchForm()

    # Populate form with request args for GET requests
    if request.method == 'GET' and request.args:
        form.deporte.data = request.args.get('deporte', '')
        form.posicion.data = request.args.get('posicion', '')
        form.edad_min.data = request.args.get('edad_min', '')
        form.edad_max.data = request.args.get('edad_max', '')
        form.pais.data = request.args.get('pais', '')
        form.ciudad.data = request.args.get('ciudad', '')
        form.nivel.data = request.args.get('nivel', '')
    players = Player.query

    # Apply filters
    if form.deporte.data and form.deporte.data != '':
        players = players.filter_by(deporte=form.deporte.data)

    if form.posicion.data and form.posicion.data != '':
        players = players.filter(Player.posicion.contains(form.posicion.data))

    if form.edad_min.data and form.edad_min.data != '':
        try:
            edad_min = int(form.edad_min.data)
            players = players.filter(Player.edad >= edad_min)
        except ValueError:
            pass

    if form.edad_max.data and form.edad_max.data != '':
        try:
            edad_max = int(form.edad_max.data)
            players = players.filter(Player.edad <= edad_max)
        except ValueError:
            pass

    if form.pais.data and form.pais.data != '':
        players = players.filter(Player.pais.contains(form.pais.data))

    if form.ciudad.data and form.ciudad.data != '':
        players = players.filter(Player.ciudad.contains(form.ciudad.data))

    if form.nivel.data and form.nivel.data != '':
        players = players.filter_by(nivel=form.nivel.data)

    players = players.all()
    return render_template("buscar.html", form=form, players=players)


# --------------------------------------------------
# EVENTOS
# --------------------------------------------------
@app.route("/eventos")
@login_required
def eventos():
    events = Event.query.order_by(Event.fecha.desc()).all()
    return render_template("eventos.html", events=events)


@app.route("/evento/<int:event_id>")
@login_required
def evento_detalle(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template("evento_detalle.html", event=event)


@app.route("/evento/crear", methods=["GET", "POST"])
@login_required
def crear_evento():
    if current_user.role != "ojeador":
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
            capacidad_maxima=form.capacidad_maxima.data,
        )
        db.session.add(event)
        db.session.commit()

        flash("Evento creado exitosamente.", "success")
        return redirect(url_for("eventos"))

    return render_template("crear_evento.html", form=form)


# --------------------------------------------------
# MENSAJES
# --------------------------------------------------
@app.route("/mensajes")
@login_required
def mensajes():
    # Get all conversation IDs where current user is involved
    sent_conversations = db.session.query(Message.conversation_id).filter_by(sender_id=current_user.id).distinct()
    received_conversations = db.session.query(Message.conversation_id).filter_by(receiver_id=current_user.id).distinct()

    # Combine and get unique conversation IDs
    all_conversation_ids = set()
    for conv in sent_conversations:
        all_conversation_ids.add(conv[0])
    for conv in received_conversations:
        all_conversation_ids.add(conv[0])

    # Get the latest message from each conversation
    conversations = []
    for conv_id in all_conversation_ids:
        latest_message = Message.query.filter_by(conversation_id=conv_id).order_by(Message.sent_at.desc()).first()
        if latest_message:
            # Get the other participant
            other_user_id = latest_message.sender_id if latest_message.receiver_id == current_user.id else latest_message.receiver_id
            other_user = User.query.get(other_user_id)

            conversations.append({
                'conversation_id': conv_id,
                'latest_message': latest_message,
                'other_user': other_user,
                'unread_count': Message.query.filter_by(
                    conversation_id=conv_id,
                    receiver_id=current_user.id,
                    is_read=False
                ).count()
            })

    # Sort conversations by latest message date
    conversations.sort(key=lambda x: x['latest_message'].sent_at, reverse=True)

    return render_template("mensajes.html", conversations=conversations)


@app.route("/mensaje/enviar", methods=["GET", "POST"])
@login_required
def enviar_mensaje():
    form = MessageForm()

    # Choices dinámicos
    users = User.query.filter(User.id != current_user.id).all()
    form.receiver_id.choices = [
        (u.id, f"{u.email} ({u.role})") for u in users
    ]

    # Pre-select receiver if provided in query parameter
    receiver_id = request.args.get('receiver')
    if receiver_id and receiver_id.isdigit():
        form.receiver_id.data = int(receiver_id)

    if form.validate_on_submit():
        # Generate conversation ID based on sender and receiver
        conversation_id = f"{min(current_user.id, form.receiver_id.data)}_{max(current_user.id, form.receiver_id.data)}_{form.subject.data.replace(' ', '_')}"

        msg = Message(
            sender_id=current_user.id,
            receiver_id=form.receiver_id.data,
            subject=form.subject.data,
            content=form.content.data,
            conversation_id=conversation_id
        )
        db.session.add(msg)
        db.session.commit()

        return redirect(url_for("mensajes"))

    return render_template("enviar_mensaje.html", form=form)

@app.route('/conversacion/<conversation_id>', methods=['GET', 'POST'])
@login_required
def conversacion(conversation_id):
    # Get all messages in this conversation
    messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.sent_at).all()

    # Check if user is part of this conversation
    if not messages:
        abort(404)

    message = messages[0]  # Get the first message to check participants
    if current_user.id not in [message.sender_id, message.receiver_id]:
        abort(403)

    # Mark messages as read if current user is the receiver
    for msg in messages:
        if msg.receiver_id == current_user.id and not msg.is_read:
            msg.is_read = True
    db.session.commit()

    # Get the other participant
    other_user_id = message.sender_id if message.receiver_id == current_user.id else message.receiver_id
    other_user = User.query.get(other_user_id)

    form = ReplyForm()
    if form.validate_on_submit():
        reply = Message(
            sender_id=current_user.id,
            receiver_id=other_user_id,
            subject=message.subject,  # Keep the same subject
            content=form.content.data,
            conversation_id=conversation_id
        )
        db.session.add(reply)
        db.session.commit()
        return redirect(url_for('conversacion', conversation_id=conversation_id))

    return render_template('conversacion.html', messages=messages, other_user=other_user, form=form, conversation_id=conversation_id)


# --------------------------------------------------
# ADMIN
# --------------------------------------------------
@app.route("/admin")
@login_required
def admin():
    if current_user.role != "admin":
        abort(403)

    users = User.query.all()
    return render_template("admin.html", users=users)


# --------------------------------------------------
# API BUSCADOR
# --------------------------------------------------
@app.route("/api/buscar")
def api_buscar():
    deporte = request.args.get("deporte")
    ciudad = request.args.get("ciudad")

    players = Player.query

    if deporte:
        players = players.filter_by(deporte=deporte)

    if ciudad:
        players = players.filter(Player.ciudad.contains(ciudad))

    players = players.all()

    return jsonify({
        "jugadores": [{
            "id": p.id,
            "nombre": f"{p.nombre} {p.apellido}",
            "deporte": p.deporte,
            "posicion": p.posicion,
            "edad": p.edad,
            "pais": p.pais,
            "ciudad": p.ciudad,
            "nivel": p.nivel,
            "descripcion": p.descripcion,
        } for p in players],
        "total": len(players),
        "pagina": 1,
        "por_pagina": 20,
    })


# --------------------------------------------------
# SUBIR VIDEO
# --------------------------------------------------
@app.route("/video/subir", methods=["GET", "POST"])
@login_required
def subir_video():
    if current_user.role != "jugador":
        abort(403)

    form = VideoForm()

    if form.validate_on_submit():

        # Video de YouTube
        if form.tipo.data == "youtube":
            video = Video(
                player_id=current_user.player_profile.id,
                titulo=form.titulo.data,
                descripcion=form.descripcion.data,
                tipo="youtube",
                url=form.url.data,
            )

        # Video local
        else:
            if "archivo" not in request.files:
                flash("No se seleccionó archivo", "danger")
                return redirect(request.url)

            file = request.files["archivo"]

            if file.filename == "":
                flash("No se seleccionó archivo", "danger")
                return redirect(request.url)

            if allowed_file(file.filename):
                filename = secure_filename(file.filename)

                upload_folder = app.config["UPLOAD_FOLDER"]
                os.makedirs(upload_folder, exist_ok=True)

                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)

                video = Video(
                    player_id=current_user.player_profile.id,
                    titulo=form.titulo.data,
                    descripcion=form.descripcion.data,
                    tipo="local",
                    filename=filename,
                )

        db.session.add(video)
        db.session.commit()

        flash("Video subido exitosamente.", "success")
        return redirect(url_for("perfil_jugador"))

    return render_template("subir_video.html", form=form)


# --------------------------------------------------
# ARCHIVOS SUBIDOS
# --------------------------------------------------
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# --------------------------------------------------
# ARRANQUE DEL SERVIDOR
# --------------------------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run()
