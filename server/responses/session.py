from server.sampleUsers import user_sessions


def get_user_session(username):
    return user_sessions[username]


def find_user_session(session_id):
    for user, value in user_sessions.items():
        if value == session_id:
            return user
    return None
