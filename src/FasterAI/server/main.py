from setup import create_app, socketio
from server import FactorialNamespace

import eventlet

if __name__ == "__main__":
    app = create_app()
    eventlet.monkey_patch()
    socketio.on_namespace(FactorialNamespace('/factorial'))
    socketio.run(app, host='0.0.0.0')
