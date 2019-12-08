from typing import Dict, Hashable, Any
from uuid import UUID


class Session:
    def __init__(self, session_id: UUID, data: Dict = None):
        self.session_id = session_id
        self.data = data or {}

    def __getitem__(self, item: Hashable) -> Any:
        return self.data[item]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.data[key] = value

    def __contains__(self, item: Hashable) -> bool:
        return item in self.data


class SessionStore:
    def __init__(self, sessions: Dict[UUID, Session] = None):
        self.sessions = sessions or {}

    def __getitem__(self, item: UUID) -> Session:
        if item not in self.sessions:
            self.sessions[item] = Session(item)
        return self.sessions[item]

    def __setitem__(self, key: UUID, value: Session) -> None:
        self.sessions[key] = value

    def __contains__(self, item: UUID) -> bool:
        return item in self.sessions
