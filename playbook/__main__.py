"""An AWS Python Pulumi AWS Module"""
import pulumi
import pulumi_command

inventory_file = pulumi.Output.all(
        k3s_server=k3s_server.public_ip,
        db_server=db_server.public_ip
        ).apply("python3 scripts/render.py hosts/ args['k3s_server'] args['db_server']")

install_log_agent_cmd = pulumi_command.local.Command(
        "InstallAgent",
        create="ansible-playbook -i hosts/inventory jobs/init_log_agent -D"
        )
