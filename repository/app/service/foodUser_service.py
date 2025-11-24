from ..config import db
from datetime import datetime, timedelta


def create_food_user_service(food_data):
    try:
        # Convert the Pydantic model to a dictionary
        food_data_dict = food_data.dict()

        # Add the document to Firestore
        new_Userfood_ref = db.collection('UserFood').document()
        new_Userfood_ref.set(food_data_dict)

        return {"message": "Food added successfully to user", "id": new_Userfood_ref.id}
    except Exception as e:
        return {"error": str(e)}


def get_user_meals(id_user):
    try:
        user_foods_query = db.collection(
            'UserFood').where('id_User', '==', id_user)
        user_foods = user_foods_query.stream()

        food_list = []
        for food in user_foods:
            food_dict = food.to_dict()
            food_dict['id'] = food.id
            food_list.append(food_dict)
        sorted_food_list = sorted(food_list, key=lambda x: x['date_ingested'])
        return {"message": "List fetched successfully", "foods": sorted_food_list}
    except Exception as e:
        return {"error": str(e)}


def get_meal_by_id(id):
    try:
        meal_ref = db.collection('UserFood').document(id)
        meal_doc = meal_ref.get()

        if meal_doc.exists:
            return meal_doc.to_dict()
        else:
            return None
    except Exception as e:
        return {"error": str(e)}


def delete_food_user_service(userFood_id):
    try:
        food_ref = db.collection('UserFood').document(userFood_id)
        food_ref.delete()
        return {"message": "user food  delete successful"}
    except Exception as e:
        return {"error": str(e)}


def update_food_user(userFood_id, userFood_data):
    try:
        updated_data = userFood_data.dict()
        userFood_ref = db.collection('UserFood').document(userFood_id)
        userFood_ref.update(updated_data)

        return {"message": "UserFood updated successfully"}
    except Exception as e:
        return {"error": str(e)}