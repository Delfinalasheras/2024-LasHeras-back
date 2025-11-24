from ..config import db
from datetime import datetime, timedelta

def create_drink(drink_data):
    try:
        new_drink_ref = db.collection('Drink').document()
        new_drink_ref.set(drink_data)
        return {"message": "drink added successfully", "id": new_drink_ref.id}
    except Exception as e:
        return {"error": str(e)}
def drinks(user_id):
    try:
        user_drinks_query = db.collection(
            'Drink').where('id_User', '==', user_id)
        user_drinks = user_drinks_query.stream()

        drinks_list = []
        for drinks in user_drinks:
            drinks_dict = drinks.to_dict()
            drinks_dict['id'] = drinks.id
            drinks_list.append(drinks_dict)
        return {"message": "List fetched successfully", "Drinks": drinks_list}
    except Exception as e:
        return {"error": str(e)}
def drink_by_id(drink_id):
    try:
        # Referencia al documento del drinko
        drink_ref = db.collection('Drink').document(drink_id)
        drink_doc =drink_ref.get()
        return {"drink": drink_doc.to_dict(), "message": "drink get successful"}
    except Exception as e:
        return {"error": str(e)}
def delete_drink(drink_id):
    try:
        # Referencia al documento del foodo
        food_ref = db.collection('Drink').document(drink_id)
        food_ref.delete()
        return {"message": "user drink  delete successful"}
    except Exception as e:
        return {"error": str(e)}
def update_Drink(userDrink_id, Drink_data):
    try:
        updated_data = Drink_data.dict()
        Drink_ref = db.collection('Drink').document(userDrink_id)
        Drink_ref.update(updated_data)

        return {"message": "Drink updated successfully"}
    except Exception as e:
        return {"error": str(e)}

def GroupedDrinks(user_id):
    try:
        # Fetch all drinks for the user
        user_drinks_query = db.collection('Drink').where('id_User', '==', user_id)
        user_drinks = user_drinks_query.stream()

        # Fetch drink types for both the user and the default types
        drink_types_query = db.collection('DrinkType').where('id_user', 'in', [user_id, 'default'])
        drink_types = drink_types_query.stream()

        # Create a dictionary to group the drinks by type
        grouped_drinks = {}

        # First, map each drink type by its ID for easy lookup
        drink_type_map = {}
        for drink_type in drink_types:
            drink_type_dict = drink_type.to_dict()
            drink_type_dict['id'] = drink_type.id
            drink_type_map[drink_type.id] = drink_type_dict
            # Prepare the grouped structure
            grouped_drinks[drink_type.id] = {
                'foods': [],  # Will hold drink IDs
                'icon': drink_type_dict.get('icon', 'Wine Bottle'),  # Default to an icon if none
                'id_User': drink_type_dict['id_user'],
                'name': drink_type_dict['name'],
                'id': drink_type.id
            }

        # Iterate over each drink and group them by typeOfDrink
        for drink in user_drinks:
            drink_dict = drink.to_dict()
            drink_dict['id'] = drink.id
            drink_type_id = drink_dict['typeOfDrink']

            # Append the drink ID to the corresponding drink type group
            if drink_type_id in grouped_drinks:
                grouped_drinks[drink_type_id]['foods'].append(drink.id)

        # Return the grouped drinks in the desired structure
        return {"message": "List fetched successfully", "Drinks": list(grouped_drinks.values())}
    except Exception as e:
        return {"error": str(e)}


