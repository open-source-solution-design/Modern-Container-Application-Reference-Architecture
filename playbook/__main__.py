"""An AWS Python Pulumi AWS Module"""
import pulumi_command

k3s_server_public_ip = pulumi_command.local.Command( "k3s_server_public_ip", create="pulumi stack output k3s_server_public_ip" )
db_server_public_ip = pulumi_command.local.Command( "db_server_public_ip", create="pulumi stack output db_server_public_ip" )

render_inventory_cmd = pulumi_command.local.Command(
        "Render",
        create="python3 render.py hosts/ k3s_server_public_ip db_server_public_ip"
        )

install_k3s_cluster_cmd = pulumi_command.local.Command(
        "SetupK3S",
        create="ansible-playbook -i hosts/inventory jobs/init_k3s_cluster -D"
        )

install_log_agent_cmd = pulumi_command.local.Command(
        "InstallAgent",
        create="ansible-playbook -i hosts/inventory jobs/init_log_agent -D"
        )
