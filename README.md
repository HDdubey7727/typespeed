# Typing Speed Comparison

This project is a real-time typing speed comparison application where two users can join a session, type simultaneously, and compare their typing speed and accuracy.

## Features
- Create a session with a unique 4-digit code.
- Join a session using the session code.
- Both users must confirm readiness before the session starts.
- Real-time typing progress updates for speed and accuracy.
- Session ends automatically after the specified duration.

## Requirements
- Python 3.7 or higher
- Dependencies listed in `requirements.txt`

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd typespeed
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Access the application:
   - On the host machine, open a browser and navigate to:
     ```
     http://127.0.0.1:8080/
     ```
   - On another device connected to the same network, find the host machine's IP address (e.g., `192.168.1.100`) and navigate to:
   - type config on terminal and check IPv4 address and use it on place of <host-ip>.
     ```
     http://<host-ip>:8080/
     ```

## Usage
1. **Create a Session**:
   - Click "Create Session" on the homepage.
   - Enter your user ID and session duration, then click "Create."
   - Share the session code with the second user.

2. **Join a Session**:
   - Click "Join Session" on the homepage.
   - Enter the session code and your user ID, then click "Join."

3. **Start the Session**:
   - Both users must click "Ready to Start" in the lobby.
   - The session starts simultaneously for both users.

4. **Typing**:
   - Type the predefined text as quickly and accurately as possible.
   - The session ends automatically after the specified duration.

## Troubleshooting
- Ensure both devices are on the same network.
- If the second device cannot connect, check the firewall settings on the host machine and allow port `8080`.

## License
This project is licensed under the MIT License.
