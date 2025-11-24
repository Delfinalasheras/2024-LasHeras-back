from app.service.dailyPlan_service import load_menu_from_db,save_menu_to_db

###FUNCIONES PRINCIAPALES
def get_or_build_menu(user_id: str,today: str):
    persisted_menu = load_menu_from_db(user_id, today)
    if persisted_menu:
        return persisted_menu
    else:
        new_menu = save_menu_to_db(user_id, today)
        return new_menu