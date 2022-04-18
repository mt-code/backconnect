from lib.framework.core import Parameter


class LPort(Parameter):
    name = "lport"
    description = "The listen port"
    types = [int]
    required = True
