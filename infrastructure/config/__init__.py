from pulumi_command import local
from pulumi_command import remote

def get_env( name ):
    env = local.Command(
            "command",
            create=f'printenv {name}'
            )
    return env.stdout

def local_run( command: str ):
    command = local.Command("local_command", create=command )
    return command.stdout
