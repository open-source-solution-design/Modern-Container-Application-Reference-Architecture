import os
from pulumi import Output
from pulumi_command import local
from pulumi_command import remote

def get(input):
    value = Output.from_input(input)
    return value.apply( os.environ[input] )
#-------------------------------------------------------------#
def local_run( command: str ):
    command = local.Command("local_command", create=command )
    return command.stdout
