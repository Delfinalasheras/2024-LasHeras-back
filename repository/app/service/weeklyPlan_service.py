from ..config import db # Asumo que importas tu instancia 'db' de algun lado
from google.cloud import firestore
import json
from fastapi import HTTPException

def get_plan_by_week_service(user_id, week_start):
    try:
        # Creamos el ID compuesto único
        user_wp_query = db.collection(
            'WeeklyPlan').where('id_User', '==', user_id)
        user_wp = user_wp_query.stream()
        for wp in user_wp:
            wp_dict = wp.to_dict()
            if wp_dict.get('week_start') == week_start:
                doc_id = wp.id
                break
        
        doc_ref = db.collection('WeeklyPlan').document(doc_id)
        doc = doc_ref.get()
        
        if doc.exists:
            return {"plan": doc.to_dict(), "message": "Plan found successfully"}
        else:

            return {"plan": None, "message": "No plan found for this week"}
            
    except Exception as e:
        return {"error": str(e)}
def update_plan_service(weekly_data):
    try:
        new_data = db.collection('WeeklyPlan').document()
        new_data.set(weekly_data)
        return {"message": "plan added successfully", "id": new_data.id}
    except Exception as e:
        return {"error": str(e)}


