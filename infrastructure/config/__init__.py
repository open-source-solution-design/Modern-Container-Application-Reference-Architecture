import os
from pulumi import Output

def get(input):
    value = Output.from_input(input)
    return value.apply( os.environ[key_name] )
