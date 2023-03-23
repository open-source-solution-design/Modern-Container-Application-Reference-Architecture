"""An AWS Python Pulumi AWS Module"""
import pulumi
import pulumi_command

k3s_server_ip = pulumi_command.local.Command(
        "get_k3s_server_ip",
        create="pulumi stack output k3s_server_public_ip"
        )

db_server_ip = pulumi_command.local.Command(
        "get_db_server_ip",
        create="pulumi stack output db_server_public_ip"
        )

inventory_file = pulumi.Output.all(
        db_server=db_server_ip,
        k3s_server=k3s_server_ip
        ).apply("python3 scripts/render.py hosts/ args['k3s_server']['stdout'] args['db_server']['stdout']")

install_log_agent_cmd = pulumi_command.local.Command(
        "InstallAgent",
        create="ansible-playbook -i hosts/inventory jobs/init_log_agent -D"
        )
