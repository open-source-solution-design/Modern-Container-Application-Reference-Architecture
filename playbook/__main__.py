"""An AWS Python Pulumi AWS Module"""

import os
import sys
import json
import stat
import jinja2
import subprocess
import pulumi
import pulumi_command

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def run_cmd(cmd):
    retcode, output = subprocess.getstatusoutput( cmd )
    assert retcode == 0
    return output

def render_template( template_source, template_result, template_vars ):
    inventory_env      = jinja2.Environment( loader=jinja2.FileSystemLoader(THIS_DIR), trim_blocks=True )
    inventory_template = inventory_env.get_template(template_source)
    inventory_output   = inventory_template.render(vars=template_vars)
    with open(template_result, "w+") as f:
        f.write(inventory_output)

ssh_private_key                = os.environ['SSH_PRIVATE_KEY']
dns_ak                         = os.environ['DNS_AK']
dns_sk                         = os.environ['DNS_SK']

data = json.loads(
        run_cmd('pulumi stack output --json')
        )

pulumi.export("data", data)

vars.update( {
  'ssh_private_key': ssh_private_key,
  'k3s_server_public_ip': data['k3s_server_public_ip'],
  'db_server_public_ip': data['db_server_public_ip'],
  'dns_ak': dns_ak,
  'dns_sk': dns_sk
 } )

render_template('templates/id_rsa', 'hosts/id_rsa', vars)
os.chmod('hosts/id_rsa', stat.S_IRUSR)
render_template('templates/inventory', 'hosts/inventory', vars)

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
