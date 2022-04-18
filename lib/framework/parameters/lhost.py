from lib.framework.core import Parameter


class LHost(Parameter):
    name = "lhost"
    description = "The listen address"
    types = [str]
    required = True
