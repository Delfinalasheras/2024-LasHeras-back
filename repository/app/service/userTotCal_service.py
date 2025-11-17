from ..config import db
from datetime import timedelta, datetime


def createUserTotCal_service(userTotCal):
    
    try:
        new_totCal = db.collection('UserTotalCal').document()
        new_totCal.set(userTotCal)
        return {"message": "New Total added successfully", "id": new_totCal.id}
    except Exception as e:
        return {"error": str(e)}

def updateDailyCalories(calPerDay_id, macros_data):
    try:
        # updated_data = macros_data.dict()
        Macros_ref = db.collection('UserTotalCal').document(calPerDay_id)
        Macros_ref.update(macros_data)

        return {"message": "Macros updated successfully"}
    except Exception as e:
        return {"error": str(e)}

def get_totalCAL(user_id):
    try:
        user_TotCal_query = db.collection(
            'UserTotalCal').where('id_user', '==', user_id)
        user_totCal = user_TotCal_query.stream()
        
        totCal_list = []
        for totCal in user_totCal:
            totCal_dict = totCal.to_dict()
            totCal_dict['id'] = totCal.id
            totCal_list.append(totCal_dict)
        sorted_totCal_list = sorted(totCal_list, key=lambda x: x['day'])
        return {"message": "List fetched successfully", "totCals": totCal_list}
    except Exception as e:
        return {"error": str(e)}

def count_recent_consecutive_days_with_calories(user_id):
    try:

        user_TotCal_query = db.collection('UserTotalCal').where('id_user', '==', user_id)
        user_totCal = user_TotCal_query.stream()
        

        totCal_list = []
        for totCal in user_totCal:
            totCal_dict = totCal.to_dict()
            totCal_dict['id'] = totCal.id
            totCal_dict['day'] = totCal_dict['day'].date()
            totCal_list.append(totCal_dict)
        sorted_totCal_list = sorted(totCal_list, key=lambda x: x['day'], reverse=True)

        if not sorted_totCal_list:
            return  {0}

        day_to_totCal = {}
        for entry in sorted_totCal_list:
            day = entry['day']
            if day not in day_to_totCal:
                day_to_totCal[day] = entry['totCal']
            else:
                day_to_totCal[day] += entry['totCal']  
        today = datetime.now().date()
        consecutive_days = 0

        while True:
            if day_to_totCal.get(today, 0) > 0:
                consecutive_days += 1
            else:

                break

            # Move to the previous day
            today -= timedelta(days=1)

        return {consecutive_days}

    except Exception as e:
        return {"error": str(e)}
def get_total(user_id: str, date: datetime):
    try:
        start = datetime(date.year, date.month, date.day)
        end = start + timedelta(days=1)

        docs = db.collection('UserTotalCal')\
            .where('id_user', '==', user_id)\
            .stream()

        results = []
        for doc in docs:
            d = doc.to_dict()
            day = d.get('day')

            # Convertir Firestore timestamp (aware) a naive
            if day:
                day = day.replace(tzinfo=None)

            if day and start <= day < end:
                d["id"] = doc.id
                results.append(d)

        if not results:
            return []

        return results

    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}




    


