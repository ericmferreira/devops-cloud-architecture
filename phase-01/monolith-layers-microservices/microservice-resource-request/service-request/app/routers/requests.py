from fastapi import APIRouter, status

from app.schemas.resource_request import ResourceRequest
from app.schemas.resource_response import ResourceResponse
from app.services.request_service import RequestService

router = APIRouter()
request_service = RequestService()

@router.get(
    "/requests/{id}",
    response_model=ResourceResponse,
    summary="Retrieve a provisioning request"
)
def get_request(id: int):
    request = request_service.get_request(id)

    return ResourceResponse.model_validate(request)

@router.post(
    "/requests",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create a new provisioning request"
)
def create_request(request: ResourceRequest):
    return request_service.create_request(request)