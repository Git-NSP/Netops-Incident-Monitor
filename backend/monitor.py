# import subprocess  # Runs system commands such as ping
# import socket  # Used for DNS resolution and TCP port checks
# import requests  # Sends HTTP/HTTPS requests for service health checks
# import time  # Used to wait between automatic monitoring cycles

# from triage import triage_incident  # Determines probable issue and severity
# from discovery import discover_route  # Discovers network hops using traceroute
# from database import create_table, save_incident, get_devices, incident_exists, save_route  # Handles database operations


# # Checks whether the host is reachable using ping
# def ping_host(host):
#     result = subprocess.run(
#         ["ping", "-n", "2", host],
#         capture_output=True,
#         text=True
#     )

#     return result.returncode == 0


# # Resolves the hostname to its IP address using DNS
# def check_dns(host):
#     try:
#         ip = socket.gethostbyname(host)
#         return ip
#     except socket.gaierror:
#         return None


# # Checks whether a specific TCP port is open on the host
# def check_port(host, port):
#     try:
#         sock = socket.socket()
#         sock.settimeout(2)

#         result = sock.connect_ex((host, port))
#         sock.close()

#         return result == 0

#     except OSError:
#         return False


# # Checks whether an HTTP/HTTPS service is responding
# def check_http(host, port):
#     try:
#         protocol = "https" if port == 443 else "http"
#         url = f"{protocol}://{host}:{port}"

#         response = requests.get(url, timeout=3)

#         return response.status_code

#     except requests.RequestException:
#         return None


# # Runs all network checks and triage for one device
# def monitor_device(name, host, port, service):
#     print(f"\nMonitoring: {name}")
#     print("----------------")

#     ip = check_dns(host)
#     dns_ok = ip is not None

#     ping_ok = ping_host(host)
#     port_ok = check_port(host, port)

#     # HTTP check is needed only for web services
#     if service.upper() in ["HTTP", "HTTPS"]:
#         status = check_http(host, port)
#         http_ok = status is not None
#     else:
#         status = None
#         http_ok = port_ok

#     if dns_ok:
#         print(f"DNS  PASS -> {ip}")
#     else:
#         print("DNS  FAIL")

#     if ping_ok:
#         print("Ping PASS")
#     else:
#         print("Ping FAIL")

#     if port_ok:
#         print(f"Port {port} OPEN")
#     else:
#         print(f"Port {port} CLOSED")

#     if service.upper() in ["HTTP", "HTTPS"]:
#         if http_ok:
#             print(f"HTTP PASS -> Status {status}")
#         else:
#             print("HTTP FAIL")

#     issue, severity = triage_incident(
#         dns_ok,
#         ping_ok,
#         port_ok,
#         http_ok
#     )

#     print(f"Probable Issue: {issue}")
#     print(f"Severity: {severity}")

#     if issue != "No issue detected":
#         if not incident_exists(host, port, issue):
#             save_incident(host, port, issue, severity)
#             print("New incident created")
#         else:
#             print("Incident already active")


# # Runs one monitoring cycle for all registered devices
# def monitor_all_devices():
#     devices = get_devices()

#     if not devices:
#         print("No devices found. Add devices using devices.py")
#         return

#     for device in devices:
#         id, name, host, port, service, location = device

#         monitor_device(
#             name,
#             host,
#             port,
#             service
#         )


# # Discovers and stores network paths for all registered devices
# def discover_all_routes():
#     devices = get_devices()

#     for device in devices:
#         device_id, name, host, port, service, location = device

#         print(f"\nDiscovering route to {name} ({host})...")

#         hops = discover_route(host)

#         save_route(device_id, hops)

#         if hops:
#             print(" -> ".join(hops))
#         else:
#             print("No route hops discovered")


# create_table()


# # Starts continuous monitoring when this file is run directly
# if __name__ == "__main__":
#     while True:
#         monitor_all_devices()

#         print("\nNext scan in 30 seconds...")
#         time.sleep(30)
        

import subprocess  # Runs system commands such as ping
import socket  # Used for DNS resolution and TCP port checks
import requests  # Sends HTTP/HTTPS requests for service health checks
import time  # Used to wait between automatic monitoring cycles

from triage import triage_incident  # Determines probable issue and severity
from discovery import discover_route  # Discovers network hops using traceroute
from database import (
    create_table,
    save_incident,
    get_devices,
    incident_exists,
    save_route
)  # Handles database operations


# Checks whether the host is reachable using ping
def ping_host(host):
    result = subprocess.run(
        ["ping", "-n", "2", host],
        capture_output=True,
        text=True
    )

    return result.returncode == 0


# Resolves the hostname to its IPv4 address using DNS
def check_dns(host):
    try:
        ip = socket.gethostbyname(host)
        return ip

    except socket.gaierror:
        return None


# Checks whether a specific TCP port is open on the host
def check_port(host, port):
    try:
        sock = socket.socket()
        sock.settimeout(2)

        result = sock.connect_ex((host, port))

        sock.close()

        return result == 0

    except OSError:
        return False


# Checks whether an HTTP/HTTPS service is responding
def check_http(host, port):
    try:
        protocol = "https" if port == 443 else "http"
        url = f"{protocol}://{host}:{port}"

        response = requests.get(
            url,
            timeout=3
        )

        return response.status_code

    except requests.RequestException:
        return None


# Runs all network checks and triage for one device
def monitor_device(name, host, port, service):
    print(f"\nMonitoring: {name}")
    print("----------------")

    ip = check_dns(host)

    dns_ok = ip is not None
    ping_ok = ping_host(host)
    port_ok = check_port(host, port)

    if service.upper() in ["HTTP", "HTTPS"]:
        status = check_http(host, port)
        http_ok = status is not None
    else:
        status = None
        http_ok = port_ok

    if dns_ok:
        print(f"DNS  PASS -> {ip}")
    else:
        print("DNS  FAIL")

    if ping_ok:
        print("Ping PASS")
    else:
        print("Ping FAIL")

    if port_ok:
        print(f"Port {port} OPEN")
    else:
        print(f"Port {port} CLOSED")

    if service.upper() in ["HTTP", "HTTPS"]:
        if http_ok:
            print(f"HTTP PASS -> Status {status}")
        else:
            print("HTTP FAIL")

    issue, severity = triage_incident(
        dns_ok,
        ping_ok,
        port_ok,
        http_ok
    )

    print(f"Probable Issue: {issue}")
    print(f"Severity: {severity}")

    if issue != "No issue detected":

        if not incident_exists(host, port, issue):
            save_incident(
                host,
                port,
                issue,
                severity
            )

            print("New incident created")

        else:
            print("Incident already active")


# Runs one monitoring cycle for all registered devices
def monitor_all_devices():
    devices = get_devices()

    if not devices:
        print("No devices found. Add devices using the dashboard.")
        return

    for device in devices:
        device_id, name, host, port, service, location = device

        monitor_device(
            name,
            host,
            port,
            service
        )


# Discovers and stores Layer-3 paths for all registered devices
def discover_all_routes():
    devices = get_devices()

    for device in devices:
        device_id, name, host, port, service, location = device

        print(
            f"\nDiscovering route from this computer "
            f"to {name} ({host})..."
        )

        hops = discover_route(host)

        save_route(device_id, hops)

        if hops:
            for hop_number, hop_ip in hops:
                print(
                    f"Hop {hop_number}: {hop_ip}"
                )
        else:
            print("No route hops discovered")


create_table()


# Starts continuous monitoring when this file is run directly
if __name__ == "__main__":

    while True:
        monitor_all_devices()

        print("\nNext scan in 30 seconds...")

        time.sleep(30)

