from fastapi import FastAPI, HTTPException
from cloud.models import ResourceConfig, CloudManager
from cloud.providers.aws_provider import AWSProvider
from pydantic import BaseModel
from typing import Dict, Any, Callable

app = FastAPI()

class IAC(BaseModel):
    IAC_provider: str
    cloud_provider: str
    service_or_resource_type: str
    status: str
    config: Dict[str, Any]

# 这是我们的云资源存储，你可能需要使用真实的数据库或者其他持久化存储替换它
cloud_resources = {}

# 定义一个处理IAC操作的函数，它接受一个回调函数作为参数
def handle_iac_operation(iac: IAC, callback: Callable):
    resource_key = f"{iac.IAC_provider}-{iac.cloud_provider}-{iac.service_or_resource_type}"
    if resource_key not in cloud_resources and iac.status != "create":
        raise HTTPException(status_code=404, detail="Resource not found")
    return callback(resource_key, iac)

@app.post("/iac/")
async def iac_operation(iac: IAC):
    # 定义回调函数
    def callback(resource_key: str, iac: IAC):
        if iac.status == "create":
            cloud_resources[resource_key] = iac.config
        elif iac.status == "delete":
            cloud_resources.pop(resource_key)
        elif iac.status == "update":
            cloud_resources[resource_key] = iac.config
        elif iac.status == "read":
            return cloud_resources[resource_key]
        elif iac.status == "migrate":
            # 迁移操作可能比较复杂，这里仅作示例
            cloud_resources[resource_key] = iac.config
        else:
            raise HTTPException(status_code=400, detail="Invalid status")
        return iac

    return handle_iac_operation(iac, callback)

from fastapi import FastAPI
from iac_operation import iac_operation, run_playbook
from models import IAC, Playbook

app = FastAPI()

@app.post("/iac/"
async def handle_iac_operation(iac: IAC):
    return iac_operation(iac)

@app.post("/playbook/")
async def handle_playbook_operation(playbook: Playbook):
    return run_playbook(playbook)
