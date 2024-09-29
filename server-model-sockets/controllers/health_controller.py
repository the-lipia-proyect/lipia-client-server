from utils.responses_helper import ok

from utils.sockets_helper import socketio, Namespace


class HealthController(Namespace):
    def on_health():
        return ok({"message": "Healthy"})


socketio.on_namespace(HealthController("/health"))
