def validate_port(port):
    try:
        port = int(port)

        if port < 1 or port > 65535:
            return False

        return True

    except ValueError:
        return False


port = input("Enter server port: ")

if validate_port(port):
    print(f"Port {port} is valid")
else:
    print("ERROR: Invalid port")