# import subprocess  # Runs the Windows tracert command
# import re  # Extracts IPv4 addresses from traceroute output


# # Discovers Layer-3 network hops between this machine and a destination
# def discover_route(host):
#     try:
#         result = subprocess.run(
#             ["tracert", "-4", "-d", "-h", "15", "-w", "1000", host],
#             capture_output=True,
#             text=True,
#             timeout=50
#         )

#         hops = []

#         # Examine every traceroute output line
#         for line in result.stdout.splitlines():
#             line = line.strip()

#             if not line:
#                 continue

#             # Hop lines begin with a hop number
#             if not re.match(r"^\d+\s+", line):
#                 continue

#             ip_addresses = re.findall(
#                 r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
#                 line
#             )

#             if ip_addresses:
#                 hops.append(ip_addresses[-1])

#         return hops

#     except subprocess.TimeoutExpired:
#         print(f"Traceroute to {host} timed out")
#         return []

#     except OSError as error:
#         print(f"Could not run tracert: {error}")
#         return []


import subprocess  # Runs the Windows tracert command
import re  # Extracts hop numbers and IPv4 addresses


# Discovers Layer-3 network hops from this computer to a destination
def discover_route(host):
    try:
        result = subprocess.run(
            ["tracert", "-4", "-d", "-h", "15", "-w", "1000", host],
            capture_output=True,
            text=True,
            timeout=50
        )

        hops = []

        # Examines every traceroute output line
        for line in result.stdout.splitlines():
            line = line.strip()

            if not line:
                continue

            hop_match = re.match(r"^(\d+)\s+", line)

            if not hop_match:
                continue

            hop_number = int(hop_match.group(1))

            ip_addresses = re.findall(
                r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
                line
            )

            if ip_addresses:
                hops.append(
                    (hop_number, ip_addresses[-1])
                )

            elif "Request timed out" in line:
                hops.append(
                    (hop_number, "Request timed out")
                )

        return hops

    except subprocess.TimeoutExpired:
        print(f"Traceroute to {host} timed out")
        return []

    except OSError as error:
        print(f"Could not run tracert: {error}")
        return []


