from app.auth2.models import User


def create_users():
    from app.settings import settings
    from app.database import SessionLocal
    from app.auth2.service import pwd_context

    # check if default user exists
    db = SessionLocal()
    existing_user = db.query(User).filter(User.username == "admin").first()
    if existing_user:
        print(f"Default user already exists: {existing_user.username}")
        db.close()
        return

    user = User(
        username=settings.default_username,
        password_hash=pwd_context.hash(settings.default_password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"Default user created: {user.username}")

    db.close()
