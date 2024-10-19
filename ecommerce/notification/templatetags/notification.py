from django import template
from notification.models import UserObj, Notification

register = template.Library()

@register.filter
def notification(user):
    if user.is_authenticated:
        try:
            user_obj = UserObj.objects.get(user=user)
        except UserObj.DoesNotExist:
            return None  # Return None if the user doesn't have a UserObj
        notification = Notification.objects.filter(userobj=user_obj, is_read=False).order_by('-id')
        if notification.exists():
            return notification
        else:
            return None
    else:
        return None

@register.filter
def notification_count(user):
    if user.is_authenticated:
        try:
            user_obj = UserObj.objects.get(user=user)
        except UserObj.DoesNotExist:
            return 0  # Return 0 if the user doesn't have a UserObj
        notification = Notification.objects.filter(userobj=user_obj, is_read=False)
        if notification.exists():
            return notification.count()
        else:
            return 0
    else:
        return 0
