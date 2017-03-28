from django.http import Http404
from django.contrib.auth.models import User, UserManager
from .models import *

def user_classes_processor(request):
    site_name = 'Clask'
    if request.user.is_authenticated() and request.user.is_superuser == False:
        try:
            user_id = request.user.id
            user_ob = User.objects.get(id=user_id)
            user_profile = UserProfile.objects.get(user=user_ob)

            
            if user_profile.classes.all().count() is not 0:
                #all_classes = user.profile.classes.all()
                classes_private = user_profile.classes.filter(is_private=True)
                classes_public = user_profile.classes.filter(is_private=False)
                if Notifications.objects.all().count() is not 0:
                    notifications = Notifications.objects.filter(user=user_profile, is_viewed=False).order_by('-date')[:3]
                    notification_count = Notifications.objects.filter(is_viewed=False, user=user_profile).count()
                    return {'notifications': notifications, 'classes_private': classes_private, 'classes_public': classes_public, 'notification_count': notification_count, 'site_name': site_name}
                else:
                    return {'classes_private': classes_private, 'classes_public': classes_public, 'site_name': site_name}
            else:
                if Notifications.objects.all().count() is not 0:
                    notifications = Notifications.objects.filter(user=user_profile, is_viewed=False).order_by('-date')[:3]
                    notification_count = Notifications.objects.filter(is_viewed=False, user=user_profile).count()
                    return {'notifications': notifications, 'notification_count': notification_count, 'site_name': site_name}
                else:
                    return {'site_name': site_name}
        except:
            raise Http404
    return {'site_name': site_name}