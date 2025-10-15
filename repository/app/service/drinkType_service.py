from ..config import db

def create_drinkType(drinkType_data):
    try:
        new_drinkType_ref = db.collection('DrinkType').document()
        new_drinkType_ref.set(drinkType_data)
        return {"message": "drinkType added successfully", "id": new_drinkType_ref.id}
    except Exception as e:
        return {"error": str(e)}
def drinkType():
    try:
        drinkType_ref = db.collection('DrinkType')
        drinkType = drinkType_ref.stream()
        drinkType_list = []

        for drinkType in drinkType:
            drinkType_dict = drinkType.to_dict()
            drinkType_dict['id'] = drinkType.id
            drinkType_list.append(drinkType_dict)
            
        return {"drinkType": drinkType_list, "message": "drinkType get successful"}
    except Exception as e:
        return {"error": str(e)}, 500
def drinkType_by_id(drinkType_id):
    try:
        # Referencia al documento del drinkTypeo
        drinkType_ref = db.collection('DrinkType').document(drinkType_id)
        drinkType_doc =drinkType_ref.get()
        return {"drinkType": drinkType_doc.to_dict(), "message": "drinkType get successful"}
    except Exception as e:
        return {"error": str(e)}
def getUserDrinkTypes(id_user):
    try:
        user_drinkType_query = db.collection('DrinkType').where('id_user', '==', id_user)
        user_drinkType = user_drinkType_query.stream()

        default_drinkType_query = db.collection('DrinkType').where('id_user', '==', 'default')
        default_drinkType = default_drinkType_query.stream()


        type_list = []

        for drink_type in user_drinkType:
            type_dict = drink_type.to_dict()
            type_dict['id'] = drink_type.id
            type_list.append(type_dict)

        for drink_type in default_drinkType:
            type_dict = drink_type.to_dict()
            type_dict['id'] = drink_type.id
            type_list.append(type_dict)

        return {"message": "List fetched successfully", "drinkType": type_list}
    except Exception as e:
        return {"error": str(e)}
def deleteDrinkType(drinktype_id):
    try:
        drinktype_ref = db.collection('DrinkType').document(drinktype_id)
        drinktype_ref.delete()
        return {"message": "user drinkType  delete successful"}
    except Exception as e:
        return {"error": str(e)}


