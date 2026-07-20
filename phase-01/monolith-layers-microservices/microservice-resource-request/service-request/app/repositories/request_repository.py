from sqlalchemy.orm import Session

from app.models.request import Request

class RequestRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, request: Request) -> Request:
        self.session.add(request)
        self.session.commit()
        self.session.refresh(request)
        return request
    
    def get_by_id(self, request_id: int) -> Request | None:
        return self.session.get(Request, request_id)