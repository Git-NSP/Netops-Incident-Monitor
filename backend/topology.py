from database import create_table, get_devices, get_routes, save_route  # Handles device and route records
from discovery import discover_route  # Discovers Layer-3 paths using traceroute


create_table()


# Displays all registered devices
def show_devices():
    devices = get_devices()

    print("\nAvailable Devices")
    print("-----------------")

    for device in devices:
        print(f"{device[0]} - {device[1]} ({device[2]})")

    return devices


# Discovers the route from this computer to one selected device
def discover_device_route():
    devices = show_devices()

    if not devices:
        print("No devices found")
        return

    try:
        device_id = int(
            input("\nDevice ID: ")
        )
    except ValueError:
        print("Invalid device ID")
        return

    selected_device = None

    for device in devices:
        if device[0] == device_id:
            selected_device = device
            break

    if selected_device is None:
        print("Device not found")
        return

    device_id, name, host, port, service, location = selected_device

    print(
        f"\nDiscovering route from this computer "
        f"to {name} ({host})..."
    )

    hops = discover_route(host)

    save_route(device_id, hops)

    if not hops:
        print("No route hops discovered")
        return

    print("\nYour Computer")

    for hop_number, hop_ip in hops:
        print("      |")
        print("      v")
        print(f"Hop {hop_number}: {hop_ip}")

    print("      |")
    print("      v")
    print(f"{name} ({host})")


# Displays all previously discovered routes
def view_routes():
    routes = get_routes()

    if not routes:
        print("\nNo discovered routes found")
        return

    current_device = None

    for route in routes:
        device_id, name, host, hop_number, hop_ip = route

        if device_id != current_device:
            if current_device is not None:
                print()

            print(f"\n{name} ({host})")
            print("----------------")

            current_device = device_id

        print(
            f"Hop {hop_number}: {hop_ip}"
        )


print("1. Discover route to a device")
print("2. View discovered routes")

choice = input("Choose option: ")


if choice == "1":
    discover_device_route()

elif choice == "2":
    view_routes()

else:
    print("Invalid option")


