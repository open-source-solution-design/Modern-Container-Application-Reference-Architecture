import os

def get(input):
    output = Output.from_input(input)
    return output.apply( os.environ[key_name] )
