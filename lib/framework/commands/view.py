import lib.framework.framework as framework
import lib.framework.utility.logger as logger
from lib.framework.core import Command


class View(Command):

    name = "view"
    summary = "View the specified payload(s)."
    args = ["payload"]
    description = """
Show the output for a specified payload. If the 'lhost' or 'lport' parameters are set, these will be used to replace the default placeholders.

You can view multiple payloads by passing them in a space separated format.

"view {payload}"
"view {payload_1} {payload_2} ..." """

    def validate(self, args):
        return True

    def execute(self, payloads_list):
        for payload_name in payloads_list:
            if payload_name in framework.payloads.available_payloads:
                payload = framework.payloads.available_payloads[payload_name]

                print()
                logger.success(payload_name)
                print(payload.get_payload())
            else:
                logger.error("Invalid payload")
