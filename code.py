# Credits to Talal Aldossary AKA mlwar4 - Simple DIY port scanner . !

import argparse
import socket
import nmap
import threading
from queue import Queue
from colorama import Fore, init

init()

GREEN = Fore.GREEN
RESET = Fore.RESET
RED = Fore.RED


def get_service_name(port):
    try:
        return socket.getservbyport(port)
    except:
        return "unknown"
    
def is_port_open(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)  # Set timeout to 1 second
    try:
        s.connect((host, port))
        return True
    except:
        return False
    finally:
        s.close()

def scan_thread(host, q, open_ports):
    while True:
        worker = q.get()
        if is_port_open(host, worker):
            open_ports.append(worker)
            print(f"{GREEN} + {worker}  {RESET}")

            #Take The Comments if you want it to print closed ports too.
       # else:
           # print(f"{RED}[-] {host}:{worker} is closed {RESET}")
      #  q.task_done()

def main(host, ports, show_conclusion):
    open_ports = []
    q = Queue()
    for port in ports:
        q.put(port)

    num_threads = 10  # Number of threads for concurrent scanning
    for _ in range(num_threads):
        t = threading.Thread(target=scan_thread, args=(host, q, open_ports))
        t.daemon = True
        t.start()

    q.join()

    if show_conclusion:
        if open_ports:
            print(f"\n{GREEN}[+] Open ports on {host}: {open_ports} {RESET}")
        else:
            print(f"\n{RED}[-] No open ports found on {host} {RESET}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Port Scanner")
    parser.add_argument("host", help="Host to scan")
    parser.add_argument("--ports", dest="port_range", default="1-1024", help="Port range to scan, default is 1-1024 (common ports)")
    parser.add_argument("-CON", action="store_true", help="Show conclusion (open ports summary)")
    args = parser.parse_args()
    host = args.host
    port_range = args.port_range
    show_conclusion = args.CON

    start_port, end_port = map(int, port_range.split("-"))
    ports = range(start_port, end_port + 1)

    main(host, ports, show_conclusion)
