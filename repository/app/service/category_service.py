from ..config import db


def create_category(category):
    try:
        category_data_dict = category.dict()
        new_Usercategory_ref = db.collection('Category').document()
        new_Usercategory_ref.set(category_data_dict)

        return {"message": "category added successfully to user", "id": new_Usercategory_ref.id}
    except Exception as e:
        return {"error": str(e)}


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
        category_ref = db.collection('Category').document(category_id)
        category_ref.update(updated_data)

        return {"message": "Category updated successfully"}
    except Exception as e:
        return {"error": str(e)}


def delete_category_service(id_category):
    try:
        food_ref = db.collection('Category').document(id_category)
        food_ref.delete()
        return {"message": "user food  delete successful"}
    except Exception as e:
        return {"error": str(e)}