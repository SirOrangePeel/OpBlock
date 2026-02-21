from werkzeug.security import generate_password_hash
from .models import Walk, Active, History, Walker, Location, Admin
from . import db
import os


def seed_db(app):
    with app.app_context():
        # -----------------------
        # Create Admin
        # -----------------------
        admin = Admin(
            email="admin@test.com",
            first_name="Main",
            password=generate_password_hash("admin123", method="pbkdf2:sha256")
        )

        db.session.add(admin)
        # -----------------------
        # Create 3 Walkers
        # -----------------------
        walker1 = Walker(
            ccid="walker1",
            email="walker1@test.com",
            f_name="John",
            l_name="Smith",
            status="Available",
            schedule="00900-1700;10900-1700;20900-1700;30900-1700;40900-1700;50900-1700;60900-1700"
        )

        walker2 = Walker(
            ccid="walker2",
            email="walker2@test.com",
            f_name="Sarah",
            l_name="Lee",
            status="Available",
            schedule="50900-1700;60900-1700"
        )

        walker3 = Walker(
            ccid="walker3",
            email="walker3@test.com",
            f_name="Mike",
            l_name="Brown",
            status="Available",
            schedule="01700-2359;11700-2359;21700-2359;31700-2359;41700-2359;51700-2359;61700-2359"
        )

        walker4 = Walker(
            ccid="srclose",
            email="seth@sethclose.au",
            f_name="Seth",
            l_name="Close",
            status="Available",
            schedule="00900-1700;10900-1700;20900-1700;30900-1700;40900-1700;50900-1700;60900-1700"
        )

        db.session.add_all([walker1, walker2, walker3, walker4])

        # -----------------------
        # Create Walk Request
        # -----------------------
        walk = Walk(
            ccid="student1",
            email="student@test.com",
            f_name="Alice",
            l_name="Johnson"
        )

        db.session.add(walk)
        db.session.commit()  # commit so walk.id exists

        # -----------------------
        # Create Active (Pending)
        # -----------------------
        active_request = Active(
            walk_id=walk.id,
            status="Pending"
        )

        db.session.add(active_request)
        db.session.commit()

        print("Database seeded successfully!")

        if not Location.query.first() is None:
            return

        data_folder = "website/data"

        FILE_FLAGS = {
            "pickup_locations.txt": {"pickup": True,  "dropoff_20_min_dist": False},
            "stations_20m.txt":      {"pickup": False, "dropoff_20_min_dist": True},
            "stations_non20m.txt":   {"pickup": False, "dropoff_20_min_dist": False},
        }

        for file in os.scandir(data_folder):

            if not file.is_file():
                continue

            print("Seeding:", file.name)

            flags = FILE_FLAGS.get(file.name)
            if not flags:
                continue

            with open(file.path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(",")
                    if len(parts) != 3:
                        print("Skipping bad line:", line)
                        continue
                    name, lat, lng = parts
                    location = Location(
                        name=name.strip(),
                        lat=float(lat.strip()),
                        lng=float(lng.strip()),
                        pickup=flags["pickup"],
                        dropoff_20_min_dist=flags["dropoff_20_min_dist"]
                    )
                    db.session.add(location)

        db.session.commit()
        print("Seeded location data.")