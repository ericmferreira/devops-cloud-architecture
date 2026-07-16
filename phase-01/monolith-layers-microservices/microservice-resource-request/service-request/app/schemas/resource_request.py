from pydantic import BaseModel
from typing import Any

class ResourceRequest(BaseModel):
    requested_by: str
    provider: str
    resource_type: str
    configuration: dict[str, Any]
