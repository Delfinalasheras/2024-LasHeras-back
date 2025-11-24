from ..config import db

def create_plateFood(plateFood_data):
    try:
        # Convert the Pydantic model to a dictionary
        plateFood_data_dict = plateFood_data.dict()

        # Add the document to Firestore
        new_plateFood_ref = db.collection('PlateFood').document()
        new_plateFood_ref.set(plateFood_data_dict)

        return {"id": new_plateFood_ref.id}
    except Exception as e:
        return {"error": str(e)}
    
def get_user_plateFood(id_plate):
    plate_food_collection = db.collection('PlateFood')
    doc_ref = plate_food_collection.document(id_plate)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict() 
    else:
        return None 


def delete_plateFood_service(userplateFood_id):
    try:
        # Referencia al documento del plateFoodo
        plateFood_ref = db.collection('PlateFood').document(userplateFood_id)
        plateFood_ref.delete()
        return {"message": "user plateFood  delete successful"}
    except Exception as e:
        return {"error": str(e)}


def update_plateFood(userplateFood_id, plateFood_data):
    try:
        updated_data = plateFood_data.dict()
        plateFood_ref = db.collection('PlateFood').document(userplateFood_id)
        plateFood_ref.update(updated_data)

        return {"message": "plateFood updated successfully"}
    except Exception as e:
        return {"error": str(e)}
