import eventlet
import eventlet.wsgi
from eventlet.websocket import WebSocketWSGI
import json
import threading

phone_connected = False
active_ws = None
remote_command = "none"
remote_action = False
add_life_requested = False
start_game_requested = False
remote_name = None
pause_requested = False
mute_requested = False
skip_requested = False

@WebSocketWSGI
def handle_websocket(ws):
    global phone_connected, active_ws, remote_command, remote_action, add_life_requested, start_game_requested, \
        remote_name, pause_requested, mute_requested, skip_requested
    phone_connected = True
    active_ws = ws
    print("📱 [SERVER] Telefon conectat cu succes!")

    try:
        while True:
            message = ws.wait()
            if message is None:
                break

            data = json.loads(message)
            if data['type'] == 'command':
                remote_command = data['value']
            elif data['type'] == 'action':
                remote_action = data['value']
            elif data['type'] == 'add_life':
                add_life_requested = True
            elif data['type'] == 'start_game':
                start_game_requested = True
            elif data['type'] == 'save_score':
                remote_name = data['value']
            elif data['type'] == 'pause':
                pause_requested = True
            elif data['type'] == 'toggle_mute':
                mute_requested = True
            elif data['type'] == 'skip_score':
                skip_requested = True
    except Exception as e:
        pass
    finally:
        phone_connected = False
        active_ws = None
        remote_command = "none"
        print("❌ [SERVER] Telefon deconectat.")

def dispatch(environ, start_response):
    if environ['PATH_INFO'] == '/':
        return handle_websocket(environ, start_response)
    else:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Not Found']

def send_update(score, lives, game_state="MENU", is_muted=None):
    global active_connection, loop
    if phone_connected and active_ws:
        try:
            message = {'type': 'update_data', 'score': score, 'lives': lives, 'state': game_state}
            if is_muted is not None:
                message['is_muted'] = is_muted
            active_ws.send(json.dumps(message))
        except Exception:
            pass


def send_vibration(vibrate_type):
    if phone_connected and active_ws:
        try:
            active_ws.send(json.dumps({'type': 'vibrate', 'value': vibrate_type}))
        except Exception:
            pass


def start_server_loop():
    print("🚀 [SERVER] Server Anti-Crash activ pe portul 8765...")
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 8765)), dispatch, log_output=False)


def start_server_thread():
    thread = threading.Thread(target=start_server_loop, daemon=True)
    thread.start()