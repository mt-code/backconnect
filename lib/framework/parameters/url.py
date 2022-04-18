from lib.framework.core import Parameter


class Url(Parameter):
    name = "url"
    description = "The target URL"
    types = [str]
    required = True
    injectable = True
