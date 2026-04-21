import socketio
import eventlet
import threading

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

phone_connected = False
remote_command = None
remote_action = False

@sio.event
def connect(sid, environ):
    global phone_connected
    phone_connected = True
    print(f"\n📱 [SERVER] Telefon conectat cu succes! (ID: {sid})")

@sio.event
def disconnect(sid):
    global phone_connected, remote_command, remote_action
    phone_connected = False
    remote_command = None
    remote_action = False
    print("\n📱 [SERVER] Telefon deconectat. Trec pe tastatură.")

@sio.event
def command(sid, data):
    global remote_command
    remote_command = data

@sio.event
def action(sid, data):
    global remote_action
    remote_action = data

def start_server_loop():
    print("🚀 [SERVER] Socket.IO activ pe portul 8765. Aștept conexiuni...")
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 8765)), app, log_output=False)

def start_server_thread():
    thread = threading.Thread(target=start_server_loop, daemon=True)
    thread.start()