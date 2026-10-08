# import sqlite3  # Used to store devices, topology, routes, and incidents
# from datetime import datetime  # Used to save the incident creation time


# # Creates all required database tables
# def create_table():
#     conn = sqlite3.connect("incidents.db")
#     cursor = conn.cursor()

#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS incidents (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             host TEXT NOT NULL,
#             port INTEGER NOT NULL,
#             issue TEXT NOT NULL,
#             severity TEXT NOT NULL,
#             status TEXT NOT NULL,
#             created_at TEXT NOT NULL
#         )
#     """)

#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS devices (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             host TEXT NOT NULL,
#             port INTEGER NOT NULL,
#             service TEXT NOT NULL,
#             location TEXT NOT NULL
#         )
#     """)

#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS connections (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             source_device_id INTEGER NOT NULL,
#             target_device_id INTEGER NOT NULL,
#             FOREIGN KEY (source_device_id) REFERENCES devices(id),
#             FOREIGN KEY (target_device_id) REFERENCES devices(id)
#         )
#     """)

#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS route_hops (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             device_id INTEGER NOT NULL,
#             hop_number INTEGER NOT NULL,
#             hop_ip TEXT NOT NULL,
#             FOREIGN KEY (device_id) REFERENCES devices(id)
#         )
#     """)

#     conn.commit()
#     conn.close()


# # Saves a new incident in the database
# def save_incident(host, port, issue, severity):
#     conn = sqlite3.connect("incidents.db")
#     cursor = conn.cursor()

#     created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     cursor.execute("""
#         INSERT INTO incidents
#         (host, port, issue, severity, status, created_at)
#         VALUES (?, ?, ?, ?, ?, ?)
#     """, (
#         host,
#         port,
#         issue,
#         severity,
#         "OPEN",
#         created_at
#     ))

#     conn.commit()
#     conn.close()


# # Checks whether the same problem already has an active incident
# def incident_exists(host, port, issue):
#     conn = sqlite3.connect("incidents.db")
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT id FROM incidents
#         WHERE host = ?
#         AND port = ?
#         AND issue = ?
#         AND status IN ('OPEN', 'ACKNOWLEDGED')
#     """, (host, port, issue))

#     incident = cursor.fetchone()

#     conn.close()

#     return incident is not None


# # Retrieves all stored incidents
# def get_incidents():
#     conn = sqlite3.connect("incidents.db")
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM incidents ORDER BY id DESC")
#     incidents = cursor.fetchall()

#     conn.close()

#     return incidents


# # Changes the status of an existing incident
# def update_incident_status(incident_id, status):
#     conn = sqlite3.connect("incidents.db")
#     cursor = conn.cursor()

#     cursor.execute("""
#         UPDATE incidents
#         SET status = ?
#         WHERE id = ?
#     """, (status, incident_id))

#     conn.commit()

#     updated = cursor.rowcount

#     conn.close()

#     return updated > 0


# # Returns basic incident statistics for reporting
# def get_incident_stats():
#     conn = sqlite3.connect("incidents.db")
#     cursor = conn.cursor()

#     cursor.execute("SELECT COUNT(*) FROM incidents")
#     total = cursor.fetchone()[0]

#     cursor.execute("SELECT COUNT(*) FROM incidents WHERE status = 'OPEN'")
#     open_count = cursor.fetchone()[0]

#     cursor.execute("""
#         SELECT COUNT(*) FROM incidents
#         WHERE status = 'ACKNOWLEDGED'
#     """)
#     acknowledged = cursor.fetchone()[0]

#     cursor.execute("""
#         SELECT COUNT(*) FROM incidents
#         WHERE status = 'RESOLVED'
#     """)
#     resolved = cursor.fetchone()[0]

#     cursor.execute("SELECT COUNT(*) FROM incidents WHERE severity = 'HIGH'")
#     high = cursor.fetchone()[0]

#     cursor.execute("SELECT COUNT(*) FROM incidents WHERE severity = 'MEDIUM'")
#     medium = cursor.fetchone()[0]

#     cursor.execute("SELECT COUNT(*) FROM incidents WHERE severity = 'LOW'")
#     low = cursor.fetchone()[0]

#     conn.close()

#     return {
#         "total_incidents": total,
#         "open": open_count,
#         "acknowledged": acknowledged,
#         "resolved": resolved,
#         "high": high,
#         "medium": medium,
#         "low": low
#     }


# # Saves a new device that should be monitored
# def add_device(name, host, port, service, location):
#     conn = sqlite3.connect("incidents.db")
#     cursor = conn.cursor()

#     cursor.execute("""
#         INSERT INTO devices
#         (name, host, port, service, location)
#         VALUES (?, ?, ?, ?, ?)
#     """, (
#         name,
#         host,
#         port,
#         service,
#         location
#     ))

#     device_id = cursor.lastrowid

#     conn.commit()
#     conn.close()

#     return device_id


# # Retrieves all registered devices
# def get_devices():
#     conn = sqlite3.connect("incidents.db")
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM devices ORDER BY id")
#     devices = cursor.fetchall()

#     conn.close()

#     return devices


# # Creates a manually configured connection between two devices
# def add_connection(source_device_id, target_device_id):
#     conn = sqlite3.connect("incidents.db")
#     cursor = conn.cursor()

#     cursor.execute("""
#         INSERT INTO connections
#         (source_device_id, target_device_id)
#         VALUES (?, ?)
#     """, (
#         source_device_id,
#         target_device_id
#     ))

#     conn.commit()
#     conn.close()


# # Retrieves manually configured topology connections
# def get_connections():
#     conn = sqlite3.connect("incidents.db")
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT
#             connections.id,
#             connections.source_device_id,
#             source.name,
#             connections.target_device_id,
#             target.name
#         FROM connections
#         JOIN devices AS source
#             ON connections.source_device_id = source.id
#         JOIN devices AS target
#             ON connections.target_device_id = target.id
#         ORDER BY connections.id
#     """)

#     connections = cursor.fetchall()

#     conn.close()

#     return connections


# # Replaces the previous discovered route for a device
# def save_route(device_id, hops):
#     conn = sqlite3.connect("incidents.db")
#     cursor = conn.cursor()

#     cursor.execute(
#         "DELETE FROM route_hops WHERE device_id = ?",
#         (device_id,)
#     )

#     for hop_number, hop_ip in enumerate(hops, start=1):
#         cursor.execute("""
#             INSERT INTO route_hops
#             (device_id, hop_number, hop_ip)
#             VALUES (?, ?, ?)
#         """, (
#             device_id,
#             hop_number,
#             hop_ip
#         ))

#     conn.commit()
#     conn.close()


# # Retrieves automatically discovered network routes
# def get_routes():
#     conn = sqlite3.connect("incidents.db")
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT
#             route_hops.device_id,
#             devices.name,
#             devices.host,
#             route_hops.hop_number,
#             route_hops.hop_ip
#         FROM route_hops
#         JOIN devices
#             ON route_hops.device_id = devices.id
#         ORDER BY route_hops.device_id, route_hops.hop_number
#     """)

#     routes = cursor.fetchall()

#     conn.close()

#     return routes


# # Returns configured topology and automatically discovered paths
# def get_topology():
#     return {
#         "devices": get_devices(),
#         "connections": get_connections(),
#         "discovered_routes": get_routes()
#     }


import sqlite3  # Used to store devices, routes, and incidents
from datetime import datetime  # Used to save the incident creation time


# Creates all required database tables
def create_table():
    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            host TEXT NOT NULL,
            port INTEGER NOT NULL,
            issue TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            host TEXT NOT NULL,
            port INTEGER NOT NULL,
            service TEXT NOT NULL,
            location TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS route_hops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER NOT NULL,
            hop_number INTEGER NOT NULL,
            hop_ip TEXT NOT NULL,
            FOREIGN KEY (device_id) REFERENCES devices(id)
        )
    """)

    conn.commit()
    conn.close()


# Saves a new incident in the database
def save_incident(host, port, issue, severity):
    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO incidents
        (host, port, issue, severity, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        host,
        port,
        issue,
        severity,
        "OPEN",
        created_at
    ))

    conn.commit()
    conn.close()


# Checks whether the same problem already has an active incident
def incident_exists(host, port, issue):
    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM incidents
        WHERE host = ?
        AND port = ?
        AND issue = ?
        AND status IN ('OPEN', 'ACKNOWLEDGED')
    """, (host, port, issue))

    incident = cursor.fetchone()

    conn.close()

    return incident is not None


# Retrieves all stored incidents
def get_incidents():
    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM incidents ORDER BY id DESC")
    incidents = cursor.fetchall()

    conn.close()

    return incidents


# Changes the status of an existing incident
def update_incident_status(incident_id, status):
    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE incidents
        SET status = ?
        WHERE id = ?
    """, (status, incident_id))

    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return updated > 0


# Returns basic incident statistics for reporting
def get_incident_stats():
    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM incidents")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM incidents WHERE status = 'OPEN'"
    )
    open_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM incidents
        WHERE status = 'ACKNOWLEDGED'
    """)
    acknowledged = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM incidents
        WHERE status = 'RESOLVED'
    """)
    resolved = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM incidents WHERE severity = 'HIGH'"
    )
    high = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM incidents WHERE severity = 'MEDIUM'"
    )
    medium = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM incidents WHERE severity = 'LOW'"
    )
    low = cursor.fetchone()[0]

    conn.close()

    return {
        "total_incidents": total,
        "open": open_count,
        "acknowledged": acknowledged,
        "resolved": resolved,
        "high": high,
        "medium": medium,
        "low": low
    }


# Saves a new device that should be monitored
def add_device(name, host, port, service, location):
    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO devices
        (name, host, port, service, location)
        VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        host,
        port,
        service,
        location
    ))

    device_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return device_id


# Retrieves all registered devices
def get_devices():
    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM devices ORDER BY id")
    devices = cursor.fetchall()

    conn.close()

    return devices


# Replaces the previous discovered route for a device
def save_route(device_id, hops):
    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM route_hops WHERE device_id = ?",
        (device_id,)
    )

    # Stores the real hop number returned by tracert
    for hop_number, hop_ip in hops:
        cursor.execute("""
            INSERT INTO route_hops
            (device_id, hop_number, hop_ip)
            VALUES (?, ?, ?)
        """, (
            device_id,
            hop_number,
            hop_ip
        ))

    conn.commit()
    conn.close()


# Retrieves automatically discovered network routes
def get_routes():
    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            route_hops.device_id,
            devices.name,
            devices.host,
            route_hops.hop_number,
            route_hops.hop_ip
        FROM route_hops
        JOIN devices
            ON route_hops.device_id = devices.id
        ORDER BY route_hops.device_id, route_hops.hop_number
    """)

    routes = cursor.fetchall()

    conn.close()

    return routes


# Returns devices and their automatically discovered Layer-3 paths
def get_topology():
    return {
        "devices": get_devices(),
        "discovered_routes": get_routes()
    }



