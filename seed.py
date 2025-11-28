from app import app, db
from models import User, Player, Scout, Event, Video, Message
from datetime import datetime, timedelta
import random

def seed_database():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        print("Creando datos de prueba...")

        # Create admin user
        admin = User(email='admin@scoutme.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

        # Create scout users
        scouts_data = [
            {
                'email': 'ojeador1@scoutme.com',
                'password': 'ojeador123',
                'nombre': 'Carlos',
                'apellido': 'Rodríguez',
                'empresa': 'ScoutPro Agency',
                'pais': 'Argentina',
                'ciudad': 'Buenos Aires',
                'especialidad': 'Fútbol, Baloncesto',
                'descripcion': 'Ojeador profesional con más de 10 años de experiencia en el descubrimiento de talento juvenil.',
                'telefono': '+54 11 1234-5678',
                'sitio_web': 'https://scoutpro.com'
            },
            {
                'email': 'ojeador2@scoutme.com',
                'password': 'ojeador123',
                'nombre': 'María',
                'apellido': 'González',
                'empresa': 'Talent Hunters',
                'pais': 'Argentina',
                'ciudad': 'Córdoba',
                'especialidad': 'Tenis, Natación',
                'descripcion': 'Especialista en deportes individuales. He descubierto varios atletas olímpicos.',
                'telefono': '+54 351 987-6543',
                'sitio_web': 'https://talenthunters.com.ar'
            },
            {
                'email': 'ojeador3@scoutme.com',
                'password': 'ojeador123',
                'nombre': 'Javier',
                'apellido': 'López',
                'empresa': 'Elite Sports',
                'pais': 'Argentina',
                'ciudad': 'Rosario',
                'especialidad': 'Fútbol',
                'descripcion': 'Enfocado en el fútbol juvenil. Trabajo con clubes profesionales de Europa.',
                'telefono': '+54 341 555-1234',
                'sitio_web': 'https://elitesports.com.ar'
            }
        ]

        scouts = []
        for scout_data in scouts_data:
            user = User(email=scout_data['email'], role='ojeador')
            user.set_password(scout_data['password'])
            db.session.add(user)
            db.session.commit()

            scout = Scout(
                user_id=user.id,
                nombre=scout_data['nombre'],
                apellido=scout_data['apellido'],
                empresa=scout_data['empresa'],
                pais=scout_data['pais'],
                ciudad=scout_data['ciudad'],
                especialidad=scout_data['especialidad'],
                descripcion=scout_data['descripcion'],
                telefono=scout_data['telefono'],
                sitio_web=scout_data['sitio_web']
            )
            db.session.add(scout)
            scouts.append(scout)

        db.session.commit()

        # Create player users
        players_data = [
            {
                'email': 'jugador1@scoutme.com',
                'password': 'jugador123',
                'nombre': 'Lionel',
                'apellido': 'Pérez',
                'fecha_nacimiento': datetime(2000, 5, 15),
                'pais': 'Argentina',
                'ciudad': 'Buenos Aires',
                'deporte': 'fútbol',
                'posicion': 'delantero',
                'nivel': 'semi-profesional',
                'descripcion': 'Delantero rápido con excelente definición. He jugado en divisiones juveniles de Boca Juniors.',
                'altura': 178,
                'peso': 75,
                'telefono': '+54 11 2345-6789',
                'videos': [
                    {'titulo': 'Goles destacados', 'tipo': 'youtube', 'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'},
                    {'titulo': 'Entrenamiento técnico', 'tipo': 'youtube', 'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
                ]
            },
            {
                'email': 'jugador2@scoutme.com',
                'password': 'jugador123',
                'nombre': 'Diego',
                'apellido': 'Martínez',
                'fecha_nacimiento': datetime(1998, 8, 22),
                'pais': 'Argentina',
                'ciudad': 'Buenos Aires',
                'deporte': 'fútbol',
                'posicion': 'mediocampista',
                'nivel': 'profesional',
                'descripcion': 'Mediocampista creativo con gran visión de juego. Experiencia en Primera División.',
                'altura': 175,
                'peso': 70,
                'telefono': '+54 11 3456-7890',
                'videos': [
                    {'titulo': 'Pases y asistencias', 'tipo': 'youtube', 'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
                ]
            },
            {
                'email': 'jugador3@scoutme.com',
                'password': 'jugador123',
                'nombre': 'Ana',
                'apellido': 'Silva',
                'fecha_nacimiento': datetime(2002, 3, 10),
                'pais': 'Argentina',
                'ciudad': 'Córdoba',
                'deporte': 'tenis',
                'posicion': 'individual',
                'nivel': 'semi-profesional',
                'descripcion': 'Tenista con ranking nacional. Especialista en singles y dobles.',
                'altura': 165,
                'peso': 58,
                'telefono': '+54 351 456-7890',
                'videos': [
                    {'titulo': 'Partido final provincial', 'tipo': 'youtube', 'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
                ]
            },
            {
                'email': 'jugador4@scoutme.com',
                'password': 'jugador123',
                'nombre': 'Miguel',
                'apellido': 'Torres',
                'fecha_nacimiento': datetime(1999, 11, 5),
                'pais': 'Argentina',
                'ciudad': 'Rosario',
                'deporte': 'baloncesto',
                'posicion': 'base',
                'nivel': 'amateur',
                'descripcion': 'Base rápido con buen manejo de balón. Juego en liga local.',
                'altura': 185,
                'peso': 80,
                'telefono': '+54 341 567-8901',
                'videos': []
            },
            {
                'email': 'jugador5@scoutme.com',
                'password': 'jugador123',
                'nombre': 'Sofia',
                'apellido': 'Ramírez',
                'fecha_nacimiento': datetime(2001, 7, 18),
                'pais': 'Argentina',
                'ciudad': 'Buenos Aires',
                'deporte': 'natación',
                'posicion': 'estilo libre',
                'nivel': 'semi-profesional',
                'descripcion': 'Nadadora especializada en 400m libres. Récords provinciales.',
                'altura': 170,
                'peso': 62,
                'telefono': '+54 11 6789-0123',
                'videos': [
                    {'titulo': 'Competencia nacional', 'tipo': 'youtube', 'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
                ]
            },
            {
                'email': 'jugador6@scoutme.com',
                'password': 'jugador123',
                'nombre': 'Lucas',
                'apellido': 'Fernández',
                'fecha_nacimiento': datetime(1997, 12, 30),
                'pais': 'Argentina',
                'ciudad': 'Mendoza',
                'deporte': 'atletismo',
                'posicion': 'velocista',
                'nivel': 'profesional',
                'descripcion': 'Velocista de 100m y 200m. Participé en Juegos Olímpicos de la Juventud.',
                'altura': 180,
                'peso': 75,
                'telefono': '+54 261 789-0123',
                'videos': [
                    {'titulo': 'Final 100m', 'tipo': 'youtube', 'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'},
                    {'titulo': 'Entrenamiento de velocidad', 'tipo': 'youtube', 'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
                ]
            }
        ]

        players = []
        for player_data in players_data:
            user = User(email=player_data['email'], role='jugador')
            user.set_password(player_data['password'])
            db.session.add(user)
            db.session.commit()

            player = Player(
                user_id=user.id,
                nombre=player_data['nombre'],
                apellido=player_data['apellido'],
                fecha_nacimiento=player_data['fecha_nacimiento'],
                pais=player_data['pais'],
                ciudad=player_data['ciudad'],
                deporte=player_data['deporte'],
                posicion=player_data['posicion'],
                nivel=player_data['nivel'],
                descripcion=player_data['descripcion'],
                altura=player_data['altura'],
                peso=player_data['peso'],
                telefono=player_data['telefono']
            )
            if player.fecha_nacimiento:
                today = datetime.today()
                player.edad = today.year - player.fecha_nacimiento.year - ((today.month, today.day) < (player.fecha_nacimiento.month, player.fecha_nacimiento.day))
            db.session.add(player)
            db.session.commit()

            # Add videos
            for video_data in player_data['videos']:
                video = Video(
                    player_id=player.id,
                    titulo=video_data['titulo'],
                    tipo=video_data['tipo'],
                    url=video_data['url']
                )
                db.session.add(video)

            players.append(player)

        db.session.commit()

        # Create sample events
        events_data = [
            {
                'titulo': 'Torneo Juvenil de Fútbol',
                'descripcion': 'Torneo abierto para jugadores de fútbol entre 16 y 20 años. Excelente oportunidad para ser visto por ojeadores.',
                'fecha': datetime.now() + timedelta(days=30),
                'ubicacion': 'Estadio Municipal, Buenos Aires',
                'deporte': 'fútbol',
                'capacidad_maxima': 64,
                'scout': random.choice(scouts)
            },
            {
                'titulo': 'Clinica de Tenis Avanzado',
                'descripcion': 'Clínica intensiva de tenis para jugadores de nivel intermedio a avanzado. Instructores profesionales.',
                'fecha': datetime.now() + timedelta(days=45),
                'ubicacion': 'Club Náutico, Córdoba',
                'deporte': 'tenis',
                'capacidad_maxima': 20,
                'scout': random.choice(scouts)
            },
            {
                'titulo': 'Tryouts Baloncesto Elite',
                'descripcion': 'Pruebas para equipo juvenil de baloncesto. Buscamos talento para competir en ligas nacionales.',
                'fecha': datetime.now() + timedelta(days=60),
                'ubicacion': 'Polideportivo Central, Rosario',
                'deporte': 'baloncesto',
                'capacidad_maxima': 50,
                'scout': random.choice(scouts)
            }
        ]

        for event_data in events_data:
            event = Event(
                scout_id=event_data['scout'].id,
                titulo=event_data['titulo'],
                descripcion=event_data['descripcion'],
                fecha=event_data['fecha'],
                ubicacion=event_data['ubicacion'],
                deporte=event_data['deporte'],
                capacidad_maxima=event_data['capacidad_maxima']
            )
            db.session.add(event)

        db.session.commit()

        # Create sample messages
        users = User.query.all()
        for i in range(5):
            sender = random.choice(users)
            receiver = random.choice([u for u in users if u.id != sender.id])
            message = Message(
                sender_id=sender.id,
                receiver_id=receiver.id,
                subject=f"Mensaje de prueba {i+1}",
                content=f"Este es un mensaje de prueba número {i+1} para demostrar la funcionalidad del sistema de mensajería."
            )
            db.session.add(message)

        db.session.commit()

        print("Datos de prueba creados exitosamente!")
        print("\nUsuarios de prueba:")
        print("Administrador: admin@scoutme.com / admin123")
        print("Ojeadores: ojeador1@scoutme.com, ojeador2@scoutme.com, ojeador3@scoutme.com / ojeador123")
        print("Jugadores: jugador1@scoutme.com hasta jugador6@scoutme.com / jugador123")

if __name__ == '__main__':
    seed_database()