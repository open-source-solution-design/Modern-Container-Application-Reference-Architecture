import os
import sys
import stat
import jinja2
import subprocess

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

if __name__ == '__main__':

    ssh_private_key                = os.environ['SSH_PRIVATE_KEY']
    dns_ak                         = os.environ['DNS_AK']
    dns_sk                         = os.environ['DNS_SK']

    vars = {}
    vars.update( {
    'ssh_private_key': ssh_private_key,
    'k3s_server_public_ip': sys.argv[1],
    'db_server_public_ip': sys.argv[2],
    'dns_ak': dns_ak,
    'dns_sk': dns_sk
     } )

    render_template('templates/id_rsa', 'hosts/id_rsa', vars)
    render_template('templates/inventory', 'hosts/inventory', vars)
    os.chmod('hosts/id_rsa', stat.S_IRUSR)
