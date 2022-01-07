def log(message):
    print(f"[*] {message}")


def error(message):
    print(f"[!] {message}")


def success(message):
    print(f"[+] {message}")


def custom(prefix, message):
    print(f"[{prefix}] {message}")
