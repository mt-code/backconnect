import argparse
import lib.framework.framework as framework


class ArgParser:
    def __init__(self):
        self.parser = None
        self.args = None

    def parse_params(self):
        self.parser = argparse.ArgumentParser(description='A tool to help leverage a command injection vulnerability '
                                                          '(or command execution shell) into a reverse shell by '
                                                          'testing various back connect payloads automatically.')

        self.parser.add_argument('-i', '--ip', help='The local listener IP')
        self.parser.add_argument('-p', '--port', help='The local listener port')
        self.parser.add_argument('-u', '--url', help='The target URL')

        self.parser.add_argument('--interactive',
                                 help='Starts in interactive mode, can be used in conjunction with other '
                                      'arguments.',
                                 action='store_true',)
        self.parser.add_argument('--list', help='Lists all of the available payloads', action='store_true')
        self.parser.add_argument('--view',
                                 help='View a specific payload, when --ip and --port are provided the payload is '
                                      'populated with these values')
        self.parser.add_argument('--payloads',
                                 help='Comma separated list of payloads to use, if no payloads are specified '
                                      'all of the available payloads are attempted.')

        try:
            self.args = self.parser.parse_args()
            self.set_framework_parameters()

            if self.args.list:
                framework.payloads.show()
                return

            if self.args.view:
                framework.available_commands["view"].execute(self.args.view.split(','))
                return

            if self.args.interactive:
                framework.start()
            elif self.validate_arguments():
                framework.available_commands["connect"].run([])
            else:
                self.parser.error("We are missing some required parameters.")
        except Exception as error:
            self.parser.error(str(error))

    def validate_arguments(self):
        try:
            if self.args.ip is None or self.args.port is None or self.args.url is None:
                raise Exception('The arguments --ip, --port and --url are required.')

        except Exception as error:
            self.parser.error(error)
            return False

        return True

    def set_framework_parameters(self):
        if self.args.ip:
            framework.parameters.set('lhost', [self.args.ip])

        if self.args.port:
            framework.parameters.set('lport', [self.args.port])

        if self.args.url:
            framework.parameters.set('url', [self.args.url])

        if self.args.payloads:
            framework.parameters.set('payloads', self.args.payloads.split(','))

