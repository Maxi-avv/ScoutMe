from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateField, IntegerField, FloatField, FileField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, URL, NumberRange
from flask_wtf.file import FileAllowed

# Country data with flags and phone codes
COUNTRIES = [
    ('', 'Seleccionar País'),
    ('AR', '🇦🇷 Argentina'),
    ('BR', '🇧🇷 Brasil'),
    ('CL', '🇨🇱 Chile'),
    ('CO', '🇨🇴 Colombia'),
    ('MX', '🇲🇽 México'),
    ('PE', '🇵🇪 Perú'),
    ('UY', '🇺🇾 Uruguay'),
    ('VE', '🇻🇪 Venezuela'),
    ('US', '🇺🇸 Estados Unidos'),
    ('ES', '🇪🇸 España'),
    ('FR', '🇫🇷 Francia'),
    ('IT', '🇮🇹 Italia'),
    ('DE', '🇩🇪 Alemania'),
    ('GB', '🇬🇧 Reino Unido'),
    ('PT', '🇵🇹 Portugal'),
    ('NL', '🇳🇱 Países Bajos'),
    ('BE', '🇧🇪 Bélgica'),
    ('CH', '🇨🇭 Suiza'),
    ('AT', '🇦🇹 Austria'),
    ('SE', '🇸🇪 Suecia'),
    ('NO', '🇳🇴 Noruega'),
    ('DK', '🇩🇰 Dinamarca'),
    ('FI', '🇫🇮 Finlandia'),
    ('PL', '🇵🇱 Polonia'),
    ('CZ', '🇨🇿 República Checa'),
    ('HU', '🇭🇺 Hungría'),
    ('RO', '🇷🇴 Rumania'),
    ('BG', '🇧🇬 Bulgaria'),
    ('GR', '🇬🇷 Grecia'),
    ('TR', '🇹🇷 Turquía'),
    ('RU', '🇷🇺 Rusia'),
    ('JP', '🇯🇵 Japón'),
    ('KR', '🇰🇷 Corea del Sur'),
    ('CN', '🇨🇳 China'),
    ('IN', '🇮🇳 India'),
    ('AU', '🇦🇺 Australia'),
    ('NZ', '🇳🇿 Nueva Zelanda'),
    ('ZA', '🇿🇦 Sudáfrica'),
    ('EG', '🇪🇬 Egipto'),
    ('MA', '🇲🇦 Marruecos'),
    ('TN', '🇹🇳 Túnez'),
    ('NG', '🇳🇬 Nigeria'),
    ('KE', '🇰🇪 Kenia'),
    ('GH', '🇬🇭 Ghana'),
    ('CM', '🇨🇲 Camerún'),
    ('CI', '🇨🇮 Costa de Marfil'),
    ('SN', '🇸🇳 Senegal'),
    ('other', '🇪🇺 Otro País')
]

PHONE_CODES = [
    ('', 'Seleccionar Código'),
    ('+54', '🇦🇷 +54 Argentina'),
    ('+55', '🇧🇷 +55 Brasil'),
    ('+56', '🇨🇱 +56 Chile'),
    ('+57', '🇨🇴 +57 Colombia'),
    ('+52', '🇲🇽 +52 México'),
    ('+51', '🇵🇪 +51 Perú'),
    ('+598', '🇺🇾 +598 Uruguay'),
    ('+58', '🇻🇪 +58 Venezuela'),
    ('+1', '🇺🇸 +1 Estados Unidos/Canadá'),
    ('+34', '🇪🇸 +34 España'),
    ('+33', '🇫🇷 +33 Francia'),
    ('+39', '🇮🇹 +39 Italia'),
    ('+49', '🇩🇪 +49 Alemania'),
    ('+44', '🇬🇧 +44 Reino Unido'),
    ('+351', '🇵🇹 +351 Portugal'),
    ('+31', '🇳🇱 +31 Países Bajos'),
    ('+32', '🇧🇪 +32 Bélgica'),
    ('+41', '🇨🇭 +41 Suiza'),
    ('+43', '🇦🇹 +43 Austria'),
    ('+46', '🇸🇪 +46 Suecia'),
    ('+47', '🇳🇴 +47 Noruega'),
    ('+45', '🇩🇰 +45 Dinamarca'),
    ('+358', '🇫🇮 +358 Finlandia'),
    ('+48', '🇵🇱 +48 Polonia'),
    ('+420', '🇨🇿 +420 República Checa'),
    ('+36', '🇭🇺 +36 Hungría'),
    ('+40', '🇷🇴 +40 Rumania'),
    ('+359', '🇧🇬 +359 Bulgaria'),
    ('+30', '🇬🇷 +30 Grecia'),
    ('+90', '🇹🇷 +90 Turquía'),
    ('+7', '🇷🇺 +7 Rusia'),
    ('+81', '🇯🇵 +81 Japón'),
    ('+82', '🇰🇷 +82 Corea del Sur'),
    ('+86', '🇨🇳 +86 China'),
    ('+91', '🇮🇳 +91 India'),
    ('+61', '🇦🇺 +61 Australia'),
    ('+64', '🇳🇿 +64 Nueva Zelanda'),
    ('+27', '🇿🇦 +27 Sudáfrica'),
    ('+20', '🇪🇬 +20 Egipto'),
    ('+212', '🇲🇦 +212 Marruecos'),
    ('+216', '🇹🇳 +216 Túnez'),
    ('+234', '🇳🇬 +234 Nigeria'),
    ('+254', '🇰🇪 +254 Kenia'),
    ('+233', '🇬🇭 +233 Ghana'),
    ('+237', '🇨🇲 +237 Camerún'),
    ('+225', '🇨🇮 +225 Costa de Marfil'),
    ('+221', '🇸🇳 +221 Senegal')
]

# Sport-specific positions
SPORT_POSITIONS = {
    'fútbol': [
        ('delantero', 'Delantero'),
        ('mediocampista', 'Mediocampista'),
        ('defensor', 'Defensor'),
        ('portero', 'Portero'),
        ('extremo', 'Extremo'),
        ('centrocampista', 'Centrocampista'),
        ('lateral', 'Lateral'),
        ('central', 'Central')
    ],
    'baloncesto': [
        ('base', 'Base'),
        ('escolta', 'Escolta'),
        ('alero', 'Alero'),
        ('ala-pivot', 'Ala-Pivot'),
        ('pivot', 'Pivot'),
        ('playmaker', 'Playmaker'),
        ('shooting-guard', 'Shooting Guard'),
        ('small-forward', 'Small Forward'),
        ('power-forward', 'Power Forward'),
        ('center', 'Center')
    ],
    'tenis': [
        ('individual', 'Individual'),
        ('dobles', 'Dobles'),
        ('mixto', 'Mixto')
    ],
    'voleibol': [
        ('punta', 'Punta'),
        ('libero', 'Libero'),
        ('central', 'Central'),
        ('opuesto', 'Opuesto'),
        ('colocador', 'Colocador'),
        ('receptor', 'Receptor'),
        ('levantador', 'Levantador'),
        ('defensor', 'Defensor')
    ],
    'natación': [
        ('estilo_libre', 'Estilo Libre'),
        ('pecho', 'Pecho'),
        ('espalda', 'Espalda'),
        ('mariposa', 'Mariposa'),
        ('combinado_individual', 'Combinado Individual'),
        ('relevos', 'Relevos'),
        ('relevos_mixtos', 'Relevos Mixtos')
    ],
    'atletismo': [
        ('velocista', 'Velocista (100m, 200m, 400m)'),
        ('medio_fondo', 'Medio Fondo (800m, 1500m)'),
        ('fondo', 'Fondo (5000m, 10000m, maratón)'),
        ('marcha', 'Marcha'),
        ('saltos', 'Saltos (altura, longitud, triple, pértiga)'),
        ('lanzamientos', 'Lanzamientos (jabalina, disco, martillo, bala)'),
        ('heptathlon', 'Heptathlon'),
        ('decathlon', 'Decathlon'),
        ('relevos', 'Relevos (4x100m, 4x400m)')
    ],
    'otro': [
        ('general', 'General'),
        ('especialista', 'Especialista'),
        ('multidisciplinario', 'Multidisciplinario')
    ]
}

from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, SelectField, TextAreaField,
    DateField, FloatField, IntegerField, FileField
)
from wtforms.validators import (
    DataRequired, Email, Length, Optional, EqualTo, NumberRange, URL
)
from flask_wtf.file import FileAllowed


# ----------------------
# FORMULARIO LOGIN
# ----------------------
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')


# ----------------------
# FORMULARIO REGISTRO JUGADOR
# ----------------------
class RegisterPlayerForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Contraseña',
        validators=[DataRequired(), Length(min=6, message='La contraseña debe tener al menos 6 caracteres')]
    )
    confirm_password = PasswordField(
        'Confirmar Contraseña',
        validators=[DataRequired(), EqualTo('password', message='Las contraseñas no coinciden')]
    )

    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=100)])
    fecha_nacimiento = DateField('Fecha de Nacimiento', validators=[Optional()])
    
    pais = SelectField('País', choices=COUNTRIES, validators=[Optional()], coerce=str)
    ciudad = StringField('Ciudad', validators=[Optional(), Length(max=100)])

    deporte = SelectField(
        'Deporte',
        choices=[
            ('fútbol', 'Fútbol'),
            ('baloncesto', 'Baloncesto'),
            ('tenis', 'Tenis'),
            ('voleibol', 'Voleibol'),
            ('natación', 'Natación'),
            ('atletismo', 'Atletismo'),
            ('otro', 'Otro')
        ],
        validators=[DataRequired()],
        coerce=str
    )

    posicion = SelectField('Posición', choices=[('', 'Primero selecciona un deporte')], validators=[Optional()])

    nivel = SelectField(
        'Nivel',
        choices=[
            ('amateur', 'Amateur'),
            ('semi-profesional', 'Semi-profesional'),
            ('profesional', 'Profesional')
        ],
        validators=[Optional()],
        coerce=str
    )

    descripcion = TextAreaField('Descripción', validators=[Optional()])
    
    altura = FloatField('Altura (cm)', validators=[Optional(), NumberRange(min=0)])
    peso = FloatField('Peso (kg)', validators=[Optional(), NumberRange(min=0)])

    phone_code = SelectField('Código de País', choices=PHONE_CODES, validators=[Optional()], coerce=str)
    telefono = StringField('Teléfono', validators=[Optional(), Length(max=20)])
    sitio_web = StringField('Sitio Web', validators=[Optional(), URL()])

    submit = SubmitField('Registrarse como Jugador')


# ----------------------
# FORMULARIO REGISTRO SCOUT
# ----------------------
class RegisterScoutForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Contraseña',
        validators=[DataRequired(), Length(min=6, message='La contraseña debe tener al menos 6 caracteres')]
    )
    confirm_password = PasswordField(
        'Confirmar Contraseña',
        validators=[DataRequired(), EqualTo('password', message='Las contraseñas no coinciden')]
    )

    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=100)])
    empresa = StringField('Empresa', validators=[Optional(), Length(max=100)])

    pais = SelectField('País', choices=COUNTRIES, validators=[Optional()], coerce=str)
    ciudad = StringField('Ciudad', validators=[Optional(), Length(max=100)])

    especialidad = StringField('Especialidad', validators=[Optional(), Length(max=100)])
    descripcion = TextAreaField('Descripción', validators=[Optional()])

    phone_code = SelectField('Código de País', choices=PHONE_CODES, validators=[Optional()], coerce=str)
    telefono = StringField('Teléfono', validators=[Optional(), Length(max=20)])
    sitio_web = StringField('Sitio Web', validators=[Optional(), URL()])

    submit = SubmitField('Registrarse como Ojeador')


# ----------------------
# FORMULARIO PERFIL JUGADOR
# ----------------------
class PlayerProfileForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=100)])
    fecha_nacimiento = DateField('Fecha de Nacimiento', validators=[Optional()])
    pais = SelectField('País', choices=COUNTRIES, validators=[Optional()], coerce=str)
    ciudad = StringField('Ciudad', validators=[Optional(), Length(max=100)])

    deporte = SelectField(
        'Deporte',
        choices=[
            ('fútbol', 'Fútbol'),
            ('baloncesto', 'Baloncesto'),
            ('tenis', 'Tenis'),
            ('voleibol', 'Voleibol'),
            ('natación', 'Natación'),
            ('atletismo', 'Atletismo'),
            ('otro', 'Otro')
        ],
        validators=[DataRequired()],
        coerce=str
    )

    posicion = SelectField('Posición', choices=[('', 'Primero selecciona un deporte')], validators=[Optional()])

    nivel = SelectField(
        'Nivel',
        choices=[
            ('amateur', 'Amateur'),
            ('semi-profesional', 'Semi-profesional'),
            ('profesional', 'Profesional')
        ],
        validators=[Optional()],
        coerce=str
    )

    descripcion = TextAreaField('Descripción', validators=[Optional()])
    altura = FloatField('Altura (cm)', validators=[Optional(), NumberRange(min=0)])
    peso = FloatField('Peso (kg)', validators=[Optional(), NumberRange(min=0)])

    phone_code = SelectField('Código de País', choices=PHONE_CODES, validators=[Optional()], coerce=str)
    telefono = StringField('Teléfono', validators=[Optional(), Length(max=20)])
    sitio_web = StringField('Sitio Web', validators=[Optional(), URL()])
    
    submit = SubmitField('Actualizar Perfil')


# ----------------------
# PERFIL SCOUT
# ----------------------
class ScoutProfileForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=100)])
    empresa = StringField('Empresa', validators=[Optional(), Length(max=100)])
    pais = SelectField('País', choices=COUNTRIES, validators=[Optional()], coerce=str)
    ciudad = StringField('Ciudad', validators=[Optional(), Length(max=100)])
    especialidad = StringField('Especialidad', validators=[Optional(), Length(max=100)])
    descripcion = TextAreaField('Descripción', validators=[Optional()])
    phone_code = SelectField('Código de País', choices=PHONE_CODES, validators=[Optional()], coerce=str)
    telefono = StringField('Teléfono', validators=[Optional(), Length(max=20)])
    sitio_web = StringField('Sitio Web', validators=[Optional(), URL()])
    submit = SubmitField('Actualizar Perfil')


# ----------------------
# FORMULARIO VIDEOS
# ----------------------
class VideoForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(max=200)])
    descripcion = TextAreaField('Descripción', validators=[Optional()])
    
    tipo = SelectField(
        'Tipo',
        choices=[('local', 'Subir Archivo'), ('youtube', 'Enlace YouTube')],
        validators=[DataRequired()],
        coerce=str
    )

    url = StringField('URL de YouTube', validators=[Optional(), URL()])
    archivo = FileField('Archivo de Video', validators=[Optional(), FileAllowed(['mp4', 'mov', 'webm', 'mkv'], 'Solo videos permitidos')])

    submit = SubmitField('Subir Video')


# ----------------------
# FORMULARIO EVENTOS
# ----------------------
class EventForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(max=200)])
    descripcion = TextAreaField('Descripción', validators=[Optional()])
    fecha = DateField('Fecha', validators=[DataRequired()])
    ubicacion = StringField('Ubicación', validators=[Optional(), Length(max=200)])

    deporte = SelectField(
        'Deporte',
        choices=[
            ('fútbol', 'Fútbol'),
            ('baloncesto', 'Baloncesto'),
            ('tenis', 'Tenis'),
            ('voleibol', 'Voleibol'),
            ('natación', 'Natación'),
            ('atletismo', 'Atletismo'),
            ('otro', 'Otro')
        ],
        validators=[Optional()],
        coerce=str
    )

    capacidad_maxima = IntegerField('Capacidad Máxima', validators=[Optional(), NumberRange(min=1)])
    submit = SubmitField('Crear Evento')


# ----------------------
# FORMULARIO MENSAJES
# ----------------------
class MessageForm(FlaskForm):
    receiver_id = SelectField('Destinatario', coerce=int, validators=[DataRequired()])
    subject = StringField('Asunto', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Mensaje', validators=[DataRequired()])
    conversation_id = StringField('Conversation ID')  # Hidden field for conversation threads
    submit = SubmitField('Enviar Mensaje')

class ReplyForm(FlaskForm):
    content = TextAreaField('Mensaje', validators=[DataRequired()])
    submit = SubmitField('Enviar Respuesta')


# ----------------------
# FORMULARIO BÚSQUEDA
# ----------------------
class SearchForm(FlaskForm):
    deporte = SelectField(
        'Deporte',
        choices=[
            ('', 'Todos'),
            ('fútbol', 'Fútbol'),
            ('baloncesto', 'Baloncesto'),
            ('tenis', 'Tenis'),
            ('voleibol', 'Voleibol'),
            ('natación', 'Natación'),
            ('atletismo', 'Atletismo'),
            ('otro', 'Otro')
        ],
        validators=[Optional()],
        coerce=str
    )

    posicion = SelectField('Posición', choices=[('', 'Todas las posiciones')], validators=[Optional()])
    edad_min = IntegerField('Edad Mínima', validators=[Optional(), NumberRange(min=0)])
    edad_max = IntegerField('Edad Máxima', validators=[Optional(), NumberRange(min=0)])
    pais = StringField('País', validators=[Optional()])
    ciudad = StringField('Ciudad', validators=[Optional()])
    
    nivel = SelectField(
        'Nivel',
        choices=[
            ('', 'Todos'),
            ('amateur', 'Amateur'),
            ('semi-profesional', 'Semi-profesional'),
            ('profesional', 'Profesional')
        ],
        validators=[Optional()],
        coerce=str
    )

    submit = SubmitField('Buscar')
