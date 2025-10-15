from ..config import db

def create_categoryFood(catFood):
    try:
        # Convert the Pydantic model to a dictionary
        categoryFood_data_dict = catFood.dict()
        
        # Add the document to Firestore
        new_UsercategoryFood_ref = db.collection('CatFood').document()
        new_UsercategoryFood_ref.set(categoryFood_data_dict)
        
        return {"message": "category added successfully to user", "id": new_UsercategoryFood_ref.id}
    except Exception as e:
        return {"error": str(e)}
def getFood_category(id_cat):
    try:
        user_categories_query = db.collection('CatFood').where('id_Category', '==', id_cat)
        user_categories = user_categories_query.stream()
        
        categorie_list = []
        for categorie in user_categories:
            categorie_dict = categorie.to_dict()
            categorie_dict['id'] = categorie.id
            categorie_list.append(categorie_dict)
        
        if not categorie_list:
            return {"message": "No categories found for this id", "categories": []}
        
        return {"message": "List fetched successfully", "categories": categorie_list}
    except Exception as e:
        return {"error": str(e)}
def delete_cateFoodByCategory(id_cat):
    try:
        user_categories_query = db.collection('CatFood').where('id_Category', '==', id_cat)
        user_categories = user_categories_query.stream()
        
        for categorie in user_categories:
            catFood_ref = db.collection('CatFood').document(categorie.id)
            catFood_ref.delete()
        
        return {"message": "catFood delete succefully"}
    except Exception as e:
        return {"error": str(e)}
def delete_catFood(id_catFood): 
    try:
        # Referencia al documento del foodo
        food_ref = db.collection('CatFood').document(id_catFood)
        food_ref.delete()
        return { "message": "user food  delete successful"}
    except Exception as e:
        return {"error": str(e)}
