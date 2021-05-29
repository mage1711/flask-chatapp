from app import app, socketio

if __name__ == '__main__':
    socketio.run(app, host='143.198.126.177',cors_allowed_origins="*")
