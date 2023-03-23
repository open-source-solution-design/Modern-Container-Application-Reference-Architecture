import os
import sys
import subprocess
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

home_dir = str(Path.home())
THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def run_cmd(cmd):
    retcode, output = subprocess.getstatusoutput( cmd )
    assert retcode == 0
    return output

def render_template( template_source, template_result, template_vars ):
    inventory_env      = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    inventory_template = inventory_env.get_template(template_source)
    inventory_output   = inventory_template.render(vars=template_vars)
    with open(template_result, "w+") as f:
        f.write(inventory_output)

if __name__ == '__main__':

    dest_dir = sys.argv[1]
    ssh_private_key                = os.environ['SSH_PRIVATE_KEY']
    dns_ak                         = os.environ['DNS_AK']
    dns_sk                         = os.environ['DNS_SK']

    vars = {}
    vars.update( {
    'ssh_private_key': ssh_private_key,
    'k3s_server_public_ip': sys.argv[2],
    'db_server_public_ip': sys.argv[3],
    'dns_ak': dns_ak,
    'dns_sk': dns_sk
     } )

    render_template('templates/id_rsa', dest_dir+'hosts/', vars)
    render_template('templates/inventory', dest_dir+'hosts/', vars)
