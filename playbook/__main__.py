"""An AWS Python Pulumi AWS Module"""

import os
import json
import subprocess
import pulumi_command

def run_cmd(cmd):
    retcode, output = subprocess.getstatusoutput( cmd )
    assert retcode == 0
    return output

data = json.loads(
        run_cmd('pulumi stack output --json')
        )

render_inventory_cmd = pulumi_command.local.Command(
        "Render",
        create=f"python3 render.py hosts/ {data['k3s_server_public_ip']} {data['db_server_public_ip']}"
        )

install_k3s_cluster_cmd = pulumi_command.local.Command(
        "SetupK3S",
        create="ansible-playbook -i hosts/inventory jobs/init_k3s_cluster -D"
        )

install_monitor_cmd = pulumi_command.local.Command(
        "InstallMonitor",
        create="ansible-playbook -i hosts/inventory jobs/init_monitor -D"
        )

install_log_agent_cmd = pulumi_command.local.Command(
        "InstallAgent",
        create="ansible-playbook -i hosts/inventory jobs/init_log_agent -D"
        )
