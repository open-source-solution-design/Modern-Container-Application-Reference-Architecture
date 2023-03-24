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

data = json.loads(
        run_cmd('pulumi stack output --json')
        )

vars = {}
vars['dns_ak'] = os.environ['DNS_AK']
vars['dns_sk'] = os.environ['DNS_SK']
vars['ssh_private_key'] = os.environ['SSH_PRIVATE_KEY']
vars['db_server_public_ip'] = data['db_server_public_ip']
vars['k3s_server_public_ip'] = data['k3s_server_public_ip']

render_template('templates/id_rsa', 'hosts/id_rsa', vars)
render_template('templates/inventory', 'hosts/inventory', vars)

setup_permission = pulumi_command.local.Command(
        "SetupPermission",
        create="chmod 0400 hosts/id_rsa"
        )

install_k3s_cluster = pulumi_command.local.Command(
        "SetupK3S",
        create="ansible-playbook -i hosts/inventory jobs/init_k3s_cluster -D",
        opts=pulumi.ResourceOptions(depends_on=[setup_permission])
        )

install_log_agent = pulumi_command.local.Command(
        "InstallAgent",
        create="ansible-playbook -i hosts/inventory jobs/init_log_agent -D",
        opts=pulumi.ResourceOptions(depends_on=[install_k3s_cluster])
        )
