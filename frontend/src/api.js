const API_URL = "http://127.0.0.1:8000";

// Gets dashboard incident statistics
export async function getStats() {
    const response = await fetch(`${API_URL}/stats`);

    if (!response.ok) {
        throw new Error("Failed to load statistics");
    }

    return response.json();
}


// Gets registered network devices
export async function getDevices() {
    const response = await fetch(`${API_URL}/devices`);

    if (!response.ok) {
        throw new Error("Failed to load devices");
    }

    return response.json();
}


// Adds a new device to the monitoring inventory
export async function addDevice(device) {
    const response = await fetch(`${API_URL}/devices`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(device)
    });

    if (!response.ok) {
        throw new Error("Failed to add device");
    }

    return response.json();
}


// Gets incident tickets
export async function getIncidents() {
    const response = await fetch(`${API_URL}/incidents`);

    if (!response.ok) {
        throw new Error("Failed to load incidents");
    }

    return response.json();
}


// Gets network topology and discovered routes
export async function getTopology() {
    const response = await fetch(`${API_URL}/topology`);

    if (!response.ok) {
        throw new Error("Failed to load topology");
    }

    return response.json();
}


// Starts one network scan
export async function runScan() {
    const response = await fetch(`${API_URL}/scan`, {
        method: "POST"
    });

    if (!response.ok) {
        throw new Error("Network scan failed");
    }

    return response.json();
}


// Starts automatic route discovery
export async function discoverNetwork() {
    const response = await fetch(`${API_URL}/discover`, {
        method: "POST"
    });

    if (!response.ok) {
        throw new Error("Network discovery failed");
    }

    return response.json();
}


// Updates an incident ticket status
export async function updateIncidentStatus(id, status) {
    const response = await fetch(
        `${API_URL}/incidents/${id}/status`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ status })
        }
    );

    if (!response.ok) {
        throw new Error("Failed to update incident");
    }

    return response.json();
}


