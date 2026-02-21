from website import create_app, db
from website.models import Admin, Walker, Walk, Active
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():

    # Reset DB (ONLY use in development)
    db.drop_all()
    db.create_all()

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
        schedule="Mon-Fri 9-5"
    )

    walker2 = Walker(
        ccid="walker2",
        email="walker2@test.com",
        f_name="Sarah",
        l_name="Lee",
        status="Available",
        schedule="Weekends"
    )

    walker3 = Walker(
        ccid="walker3",
        email="walker3@test.com",
        f_name="Mike",
        l_name="Brown",
        status="Available",
        schedule="Evenings"
    )

    db.session.add_all([walker1, walker2, walker3])

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