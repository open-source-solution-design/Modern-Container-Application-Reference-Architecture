from fastapi import FastAPI
from models import IAC, Playbook
from iac_operation import iac_operation, run_playbook

app = FastAPI()

@app.post("/iac/")
async def handle_iac_operation(iac: IAC):
    return iac_operation(iac)

@app.post("/playbook/")
async def handle_playbook_operation(playbook: Playbook):
    return run_playbook(playbook)
