from app.schemas.resource_request import ResourceRequest
from app.repositories.request_repository import RequestRepository


class RequestService:

    def __init__(self):
        self.repository = RequestRepository()

    def create_request(self, request: ResourceRequest):
        return {
            "status": "accepted",
            "message": "Request accepted for asynchronous processing."
        }