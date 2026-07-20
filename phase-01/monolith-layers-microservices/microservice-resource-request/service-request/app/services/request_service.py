from app.schemas.resource_request import ResourceRequest
from app.repositories.request_repository import RequestRepository
from app.models.request import Request
from app.database import SessionLocal

from datetime import date, timedelta


class RequestService:

    # def __init__(self):
    #     self.repository = RequestRepository()

    def create_request(self, request: ResourceRequest):
        with SessionLocal() as session:
            repository = RequestRepository(session)
            new_request = Request(
                requested_by=request.requested_by,
                provider=request.provider,
                resource_type=request.resource_type,
                configuration=request.configuration,
                location=request.location,
                project_id=request.project_id,
                end_date=date.today() + timedelta(days=90)  # Default end date is 90 days from today
            )
            saved_request = repository.save(new_request)
            return {
                "id": saved_request.id,
                "status": "accepted",
                "message": "Request accepted for asynchronous processing."
            }