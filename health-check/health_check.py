import os

SERVERS = ["IP_1", "IP_2", "IP_N"]
STATUS = {server: False for server in SERVERS}


def ping_server(server: str) -> bool:
    """Ping the specified server and return True if it responds, False otherwise."""
    response = os.system(
        f"ping -n 4 -i 10 {server} >nul 2>&1"
    )  # ">nul 2>&1" hides the output
    return response == 0


def send_message() -> None:
    """Send a message to notify that a server is down."""
    # Code to send message goes here
    pass


def main() -> None:
    """Check the status of the servers and send a message if a server is down."""
    print(
        """
 _                _ _   _            _               _    
| |              | | | | |          | |             | |   
| |__   ___  __ _| | |_| |__     ___| |__   ___  ___| | __
| '_ \ / _ \/ _` | | __| '_ \   / __| '_ \ / _ \/ __| |/ /
| | | |  __/ (_| | | |_| | | | | (__| | | |  __/ (__|   < 
|_| |_|\___|\__,_|_|\__|_| |_|  \___|_| |_|\___|\___|_|\_\\
                                                                                                                   
"""
    )

    while True:
        for server in SERVERS:
            if not ping_server(server) and not STATUS[server]:
                print(f"Server {server} is down!")
                send_message()
                STATUS[server] = True
            else:
                STATUS[server] = False


if __name__ == "__main__":
    main()
