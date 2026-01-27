from src.models import User
from src.auth import get_password_hash

def make_user(db, email, password, **kwargs):
    user = User(
        email=email,
        hashed_password=get_password_hash(password),
        full_name=kwargs.get("full_name", ""),
        is_active=kwargs.get("is_active", True),
        is_organizer=kwargs.get("is_organizer", False),
        is_admin=kwargs.get("is_admin", False)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
