from lib.framework.core import Parameter


class PostData(Parameter):
    name = "postdata"
    description = "The post data to be sent with the request, this can include the INJECT placeholder"
    types = [str]
