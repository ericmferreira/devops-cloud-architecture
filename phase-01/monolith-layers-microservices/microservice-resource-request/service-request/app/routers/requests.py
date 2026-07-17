from fastapi import APIRouter, status

from app.schemas.resource_request import ResourceRequest
from app.services.request_service import RequestService

router = APIRouter()
request_service = RequestService()

@router.get(
    "/requests/{id}",
    summary="Retrieve a provisioning request"
)
def get_request(id: int):
    return {
            "id": id, 
            "message": "Request retrieved successfully."
            }

@router.post(
    "/requests",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create a new provisioning request"
)
def create_request(request: ResourceRequest):
    return request_service.create_request(request)