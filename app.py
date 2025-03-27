from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
import time
import threading
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Store session data
sessions = {}

@app.route('/')
def index():
    return render_template('index.html')  # Serve the index.html file

@app.route('/create')
def create():
    return render_template('create.html')  # Serve the create session page

@socketio.on('create_session')
def create_session(data):
    user_id = data['user_id']
    duration = data['duration']
    session_id = str(random.randint(1000, 9999))  # Generate a random 4-digit session ID
    sessions[session_id] = {
        'start_time': None,
        'user_data': {user_id: {'accuracy': 0, 'speed': 0, 'ready': False}},
        'duration': duration,
        'started': False
    }
    emit('session_created', {'session_id': session_id})

@socketio.on('join_session')
def join_session(data):
    session_id = data['session_id']
    user_id = data['user_id']

    # Debug logs to verify session data
    print(f"Attempting to join session: {session_id} with user ID: {user_id}")
    print(f"Current sessions: {sessions}")

    if session_id in sessions:
        if len(sessions[session_id]['user_data']) < 2:
            join_room(session_id)
            sessions[session_id]['user_data'][user_id] = {'accuracy': 0, 'speed': 0, 'ready': False}
            emit('session_joined', {'session_id': session_id, 'user_id': user_id}, room=session_id)
        else:
            emit('join_error', {'error': 'Session is full'})
    else:
        emit('join_error', {'error': 'Session does not exist'})

@socketio.on('ready_to_start')
def ready_to_start(data):
    session_id = data['session_id']
    user_id = data['user_id']

    if session_id in sessions:
        sessions[session_id]['user_data'][user_id]['ready'] = True

        # Check if all users are ready
        if all(user['ready'] for user in sessions[session_id]['user_data'].values()):
            sessions[session_id]['start_time'] = time.time()
            sessions[session_id]['started'] = True

            # Start a timer to end the session automatically
            threading.Thread(target=end_session_timer, args=(session_id, sessions[session_id]['duration'])).start()
            emit('session_started', {'duration': sessions[session_id]['duration']}, room=session_id)

@socketio.on('typing_progress')
def typing_progress(data):
    session_id = data['session_id']
    user_id = data['user_id']
    typed_text = data['typed_text']
    predefined_text = data['predefined_text']

    if session_id in sessions and sessions[session_id]['started']:
        # Calculate progress
        accuracy = sum(1 for a, b in zip(typed_text, predefined_text) if a == b) / len(predefined_text) * 100
        speed = len(typed_text.split()) / ((time.time() - sessions[session_id]['start_time']) / 60)

        # Store user data
        sessions[session_id]['user_data'][user_id] = {
            'accuracy': accuracy,
            'speed': speed
        }

        emit('update_progress', {
            'user_id': user_id,
            'accuracy': accuracy,
            'speed': speed
        }, room=session_id)

@socketio.on('end_session')
def end_session(data):
    session_id = data['session_id']
    if session_id in sessions:
        results = sessions.pop(session_id, {}).get('user_data', {})
        emit('session_ended', {'results': results}, room=session_id)

def end_session_timer(session_id, duration):
    time.sleep(duration)
    if session_id in sessions:
        sessions[session_id]['started'] = False  # Prevent further typing
        end_session({'session_id': session_id})    socketio.run(app, host='0.0.0.0', port=8080)




    socketio.run(app, host='0.0.0.0', port=8080)  # Ensure the app runs on all interfacesif __name__ == '__main__':