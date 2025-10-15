from ..config import db
from datetime import datetime, timedelta

def get_user_notifications(id_user):
    try:
        # Check if this query works without orderBy to test for indexing issues
        user_notifications_query = db.collection(
            'UserNotifications'
        ).where('user_id', '==', id_user)
        user_notifications = user_notifications_query.stream()
        
        Notification_list = []
        for Notification in user_notifications:
            Notification_dict = Notification.to_dict()
            Notification_dict['id'] = Notification.id
            if(Notification_dict['is_read']==False):
                Notification_list.append(Notification_dict)
            
        
        return {"message": "List fetched successfully", "notifications": Notification_list}
    
    except Exception as e:
        return {"error": f"Error fetching notifications: {str(e)}"}
def changeNotificationToRead(id_noti):
    try:

        noti_ref = db.collection('UserNotifications').document(id_noti)
        
        noti_ref.update({'is_read': True})
        
        return {"message": "Notification marked as read successfully"}
    
    except Exception as e:
        return {"error": str(e)}




