from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack

from account import routing as account_routing

application = ProtocolTypeRouter({
   'websocket': AuthMiddlewareStack(
        URLRouter(
            account_routing.websocket_urlpatterns
        )
    )
})