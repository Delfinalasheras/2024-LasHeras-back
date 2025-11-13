from app.service.category_service import create_category, get_user_categories, update_category, delete_category_service
from app.models.category import Category
from app.controllers.food_controller import get_foods
from app.service.plate_service import get_plates
from app.service.drink_service import drinks
from app.config import db
from fastapi import HTTPException
import re

icons = ['Apple', 'Carrot', 'Fish', 'Pizza', 'Ice Cream', 'Bread', 'Egg', 'Cheese', 'Drumstick', 'Hotdog',
         'Hamburger', 'Pepper', 'Cookie', 'Bacon', 'Leaf', 'Seedling', 'Lemon', 'Wine Bottle', 'Mug', "Seedling"]


def validate_name(campo, label):
    if not campo.strip():
        raise HTTPException(
            status_code=400, detail=f"{label} cannot be empty or blank")
    if type(campo) is not str:
        raise HTTPException(
            status_code=400, detail=f"{label} must be a string")
    if not re.match(r'^[a-zA-Z\s]+$', campo):
        raise HTTPException(
            status_code=400, detail=f"Invalid format for {label}. Only letters and spaces allowed.")


def validate_category_data(category: Category):
    if not category.name.strip():
        raise HTTPException(status_code=400, detail="Category name cannot be empty.")
    if not category.icon.strip():
        raise HTTPException(status_code=400, detail="Category icon cannot be empty.")
    if not category.foods:
        raise HTTPException(status_code=400, detail="Category must have at least one food.")



def userCategoryLog(user_id: str, category):
    validate_category_data(category)  # Ensure this is defined or remove if not needed
    
    category_data = category if isinstance(category, dict) else category.dict()
    category_data["id_User"] = user_id
    
    print("📦 Category to save:", category_data)
    response = create_category(category_data)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return response



def get_category(user_id: str):
    response = get_user_categories(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}

def update_category_controller(user_id: str, category_id: str, updated_category_data: Category):
      # Fetch the specific category
      try:
          category_ref = db.collection('Category').document(category_id)
          category_doc = category_ref.get()
          if not category_doc.exists:
              raise HTTPException(status_code=400, detail=f"Category with ID {category_id} not found")
          category = category_doc.to_dict()
          if category.get('id_User') != user_id:
              raise HTTPException(status_code=403, detail="You can only update your own categories")
      except Exception as e:
          raise HTTPException(status_code=500, detail=f"Error fetching category: {str(e)}")
      
      # Validate
      validate_category_data(updated_category_data)
      
      # Update
      response = update_category(category_id, updated_category_data)
      if "error" in response:
          raise HTTPException(status_code=500, detail=response["error"])
      return {"message": response}

def delete_category(id_user: str, category_id: str):
    categories = get_category(id_user)
    if not category_id:
        raise HTTPException(
            status_code=400, detail="The category id is empty")
    if not categories:
        raise HTTPException(
            status_code=400, detail="The current user has no categories")
    print(categories['message']['categories'])
    existing_categories_ids = [category["id"]
                               for category in categories['message']['categories']]
    if category_id not in existing_categories_ids:
        raise HTTPException(
            status_code=400, detail=f"Invalid category ID: {category_id}")
    response = delete_category_service(category_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
