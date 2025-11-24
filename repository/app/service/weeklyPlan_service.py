from ..config import db # Asumo que importas tu instancia 'db' de algun lado
from google.cloud import firestore
import json
from fastapi import HTTPException

def get_plan_by_week_service(user_id, week_start):
    try:
        user_wp_query = db.collection('WeeklyPlan').where('id_User', '==', user_id)
        matches = user_wp_query.stream()

        for wp in matches:
            wp_dict = wp.to_dict()
            if wp_dict.get('week_start') == week_start:
                return {"plan": wp_dict, "id": wp.id, "message": "Plan found successfully"}

        return {"plan": None, "id": None, "message": "No plan found for this week"}

    except Exception as e:
        return {"error": str(e)}


def save_or_update_plan_service(weekly_data):
    try:
        user_id = weekly_data["id_User"]
        week_start = weekly_data["week_start"]

        # 1. Buscar si ya existe un plan
        existing = get_plan_by_week_service(user_id, week_start)

        if existing.get("id"):  
            # 2. Si existe → UPDATE
            doc_ref = db.collection('WeeklyPlan').document(existing["id"])
            doc_ref.update(weekly_data)
            return {"message": "Plan updated successfully", "id": existing["id"]}

        else:
            # 3. Si no existe → CREATE
            new_doc = db.collection('WeeklyPlan').document()
            new_doc.set(weekly_data)
            return {"message": "Plan created successfully", "id": new_doc.id}

    except Exception as e:
        return {"error": str(e)}



