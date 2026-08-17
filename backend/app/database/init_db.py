from app.database.database import engine
from app.database.base import Base

# Import models
from app.models.user import User
from app.models.profile import Profile
from app.models.clothing_item import ClothingItem
from app.models.ecommerce_product import EcommerceProduct
from app.models.favorite import FavoriteOutfit       
from app.models.chat_history import ChatHistory 

Base.metadata.create_all(bind=engine)

print("Tables created successfully.")