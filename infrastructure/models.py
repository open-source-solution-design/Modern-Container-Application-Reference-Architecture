from pydantic import BaseModel
from typing import Dict, Any

class IAC(BaseModel):
    IAC_provider: str
    cloud_provider: str
    service_or_resource_type: str
    status: str
    config: Dict[str, Any]

class Playbook(BaseModel):
    inventory: str  # dynamic or static
    playbook: str  # directory or git url
    config: Dict[str, Any]
