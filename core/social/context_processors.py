from django.conf import settings


def theme_context(request):
    theme = 'light'  
    if request.user.is_authenticated:
        try:
            if hasattr(request.user, 'settings'):
                theme = request.user.settings.theme  
        except Exception:
            pass
    return {'theme': theme}
