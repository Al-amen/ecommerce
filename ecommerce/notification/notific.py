from notification.models import UserObj, Notification

class SendNotification:
    def __init__(self, user, message):
        self.user = user
        self.message = message

        # Try to get the UserObj, and create it if it doesn't exist
        user_obj, created = UserObj.objects.get_or_create(user=self.user)

        # Now proceed with creating the notification
        notification = Notification.objects.create(message=self.message, is_read=False)
        notification.userobj.add(user_obj)
        notification.save()