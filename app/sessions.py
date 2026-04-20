from threading import Lock


class SessionStore:
    def __init__(self):
        self._store: dict = {}
        self._lock = Lock()

    def create(self, session_id: str, meta: dict):
        with self._lock:
            self._store[session_id] = {**meta, "history": []}

    def exists(self, session_id: str) -> bool:
        return session_id in self._store

    def get(self, session_id: str) -> dict | None:
        return self._store.get(session_id)

    def update_history(self, session_id: str, history: list):
        with self._lock:
            if session_id in self._store:
                self._store[session_id]["history"] = history

    def delete(self, session_id: str):
        with self._lock:
            self._store.pop(session_id, None)


session_store = SessionStore()
