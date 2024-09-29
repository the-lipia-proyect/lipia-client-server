from flask_socketio import SocketIO, Namespace


socketio = SocketIO(
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True,
)
