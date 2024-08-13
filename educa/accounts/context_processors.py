from .models import Message


def notifications(request):
    if request.user.is_authenticated:
        msg = Message.objects.filter(recipient_user=request.user, is_read=False)
    else:
        msg = None
    
    return {
        'notifications': msg
    }