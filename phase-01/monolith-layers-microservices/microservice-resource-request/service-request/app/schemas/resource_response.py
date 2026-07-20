from datetime import date
from typing import Any

from pydantic import BaseModel, ConfigDict


class ResourceResponse(BaseModel):
    id: int
    requested_by: str
    provider: str
    resource_type: str
    configuration: dict[str, Any]
    location: str
    project_id: str
    end_date: date
    status: str

    model_config = ConfigDict(from_attributes=True)