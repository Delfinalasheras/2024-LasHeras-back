from ..config import db


def create_category(category_data: dict):
    try:
        print("Attempting to save to Firestore:", category_data)
        new_Usercategory_ref = db.collection('Category').document()
        new_Usercategory_ref.set(category_data)
        print("Category saved successfully with ID:", new_Usercategory_ref.id)
        return {"message": "Category added successfully", "id": new_Usercategory_ref.id}
    except Exception as e:
        print("Firestore error:", str(e))
        return {"error": f"Failed to create category: {str(e)}"}


def get_user_categories(user_id):
    try:
        user_categories_query = db.collection(
            'Category').where('id_User', '==', user_id)
        user_categories = user_categories_query.stream()

        categorie_list = []
        for categorie in user_categories:
            categorie_dict = categorie.to_dict()
            categorie_dict['id'] = categorie.id
            categorie_list.append(categorie_dict)

        return {"message": "List fetched successfully", "categories": categorie_list}
    except Exception as e:
        return {"error": str(e)}


def update_category(category_id, updated_category_data):
      try:
          updated_data = updated_category_data.dict()
          print("📦 Updating with:", updated_data)
          category_ref = db.collection('Category').document(category_id)
          category_ref.update(updated_data)
          return {"message": "Category updated successfully"}
      except Exception as e:
          print("❌ Update error:", str(e))
          return {"error": str(e)}


def delete_category_service(id_category):
    try:
        food_ref = db.collection('Category').document(id_category)
        food_ref.delete()
        return {"message": "user food  delete successful"}
    except Exception as e:
        return {"error": str(e)}