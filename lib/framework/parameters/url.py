from lib.framework.core import Parameter


class Url(Parameter):
    name = "url"
    description = "The target URL, this can include the INJECT placeholder"
    types = [str]
