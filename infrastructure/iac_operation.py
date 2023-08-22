from typing import Callable
from models import IAC, Playbook
from fastapi import HTTPException
from ansible.playbook import PlayBook
from ansible.utils.display import Display
from ansible.vars.manager import VariableManager
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor

# This is our cloud resource storage, you may need to replace it with a real database or other persistent storage
cloud_resources = {}

# Define a function to handle IAC operations, it accepts a callback function as a parameter
def handle_iac_operation(iac: IAC, callback: Callable):
    resource_key = f"{iac.IAC_provider}-{iac.cloud_provider}-{iac.service_or_resource_type}"
    if resource_key not in cloud_resources and iac.status != "create":
        raise HTTPException(status_code=404, detail="Resource not found")
    return callback(resource_key, iac)

def iac_operation(iac: IAC):
    # Define a callback function
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
            # Migration operations may be complicated, this is just an example
            cloud_resources[resource_key] = iac.config
        else:
            raise HTTPException(status_code=400, detail="Invalid status")
        return iac

    return handle_iac_operation(iac, callback)

def run_playbook(playbook: Playbook):
    # Initialize necessary ansible objects
    loader = DataLoader()
    display = Display()
    inventory_manager = InventoryManager(loader=loader, sources=playbook.inventory)
    variable_manager = VariableManager(loader=loader, inventory=inventory_manager)

    # Create the playbook executor, passing in the playbook, inventory, variable manager and loader
    playbook_executor = PlaybookExecutor(
        playbooks=[playbook.playbook],
        inventory=inventory_manager,
        variable_manager=variable_manager,
        loader=loader,
        passwords={}
    )

    # Run the playbook
    results = playbook_executor.run()

    # You might want to format the results or handle errors based on your needs
    return {"status": "success", "results": results}
