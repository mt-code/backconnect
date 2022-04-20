from lib.framework.core import Parameter


class Headers(Parameter):
    name = "headers"
    description = "The headers to use for the request, multiple headers can be set using a space separated list."
    types = [str, list]
