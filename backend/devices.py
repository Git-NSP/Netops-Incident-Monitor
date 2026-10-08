from database import create_table, add_device, get_devices  # Handles device inventory

create_table()

print("1. Add device")
print("2. View devices")

choice = input("Choose option: ")

if choice == "1":
    name = input("Device name: ")
    host = input("Host: ")
    port = int(input("Port: "))
    service = input("Service: ")
    location = input("Location: ")

    add_device(name, host, port, service, location)

    print("Device added successfully")

elif choice == "2":
    devices = get_devices()

    print("\nDevice Inventory")
    print("----------------")

    for device in devices:
        print(device)

else:
    print("Invalid option")


