import os

servers = ["IP_1", "IP_2", "IP_N"]
status = {server: False for server in servers}


def ping_server(server):
    response = os.system("ping -n 4 -i 10 " + server + " >nul 2>&1") # ">nul 2>&1" hide the output
    return response == 0


def send_message():
    # Code to send message goes here
    pass


print("""
 _                _ _   _            _               _    
| |              | | | | |          | |             | |   
| |__   ___  __ _| | |_| |__     ___| |__   ___  ___| | __
| '_ \ / _ \/ _` | | __| '_ \   / __| '_ \ / _ \/ __| |/ /
| | | |  __/ (_| | | |_| | | | | (__| | | |  __/ (__|   < 
|_| |_|\___|\__,_|_|\__|_| |_|  \___|_| |_|\___|\___|_|\_\\
                                                                                                                   
"""
)


while True:
    for server in servers:
        if not ping_server(server) and not status[server]:
            print(f"Server {server} is down!")
            send_message()
            status[server] = True
        else:
            status[server] = False
