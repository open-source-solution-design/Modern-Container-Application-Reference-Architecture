"""An AWS Python Pulumi AWS Module"""
import pulumi_command

k3s_server_ip = pulumi_command.local.Command( "get_k3s_server_ip", create="pulumi stack output k3s_server_public_ip" )
db_server_ip = pulumi_command.local.Command( "get_db_server_ip", create="pulumi stack output db_server_public_ip" )

render_inventory_cmd = pulumi_command.local.Command(
        "Render",
        create="python3 scripts/render.py hosts/ k3s_server_ip db_server_ip"
        )

install_log_agent_cmd = pulumi_command.local.Command(
        "InstallAgent",
        create="ansible-playbook -i hosts/inventory jobs/init_log_agent -D"
        )
