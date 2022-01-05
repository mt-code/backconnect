from lib.framework.core import Parameter


class Payloads(Parameter):
    name = "payloads"
    description = "The payloads to use, if this is not set all payloads will be tried."
    types = [str, list]
