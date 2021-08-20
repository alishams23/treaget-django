from account.models import Notification


def notificationAdd(receiver, title, **kwargs):
    if "user" in kwargs:
        user = kwargs["user"]
    else:
        user = None
    if "body" in kwargs:
        body = kwargs["body"]
    else:
        body = None
    if "url" in kwargs:
        url = kwargs["url"]
    else:
        url = None

    notification = Notification(user=user, body=body, receiver=receiver, title=title, url=url)
    notification.save()