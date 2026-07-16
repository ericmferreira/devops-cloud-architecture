from fastapi import APIRouter, status

router = APIRouter()

@router.get("/requests/{id}")
def get_request(id: int):
    return {
            "id": id, 
            "message": "Request retrieved successfully."
            }

@router.post(
    "/requests",
    status_code=status.HTTP_202_ACCEPTED
)
def create_request():
    return {
        "status": "accepted",
        "message": "Request accepted for asynchronous processing."
    }