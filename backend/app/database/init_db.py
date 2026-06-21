from app.database.database import engine
from app.database.base import Base

# Import models
from app.models.user import User
from app.models.profile import Profile
from app.models.clothing_item import ClothingItem

Base.metadata.create_all(bind=engine)

print("Tables created successfully.")