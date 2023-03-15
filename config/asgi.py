"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

# import os
# import django
# from channels.routing import get_default_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# django.setup()

# application = get_default_application()

import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()


from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from chat.middleware import TokenAuthMiddleware
from django.urls import path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

import chat.routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            TokenAuthMiddleware(URLRouter(chat.routing.websocket_urlpatterns))
        ),
    }
)