// import { useEffect, useState } from "react";
// import {
//     getStats,
//     getDevices,
//     addDevice,
//     getIncidents,
//     runScan,
//     updateIncidentStatus
// } from "./api";

// import "./App.css";


// function App() {
//     const [stats, setStats] = useState(null);
//     const [devices, setDevices] = useState([]);
//     const [incidents, setIncidents] = useState([]);

//     const [loading, setLoading] = useState(true);
//     const [scanning, setScanning] = useState(false);
//     const [addingDevice, setAddingDevice] = useState(false);
//     const [error, setError] = useState("");

//     const [newDevice, setNewDevice] = useState({
//         name: "",
//         host: "",
//         port: "",
//         service: "",
//         location: ""
//     });


//     // Loads all dashboard information from FastAPI
//     async function loadDashboard() {
//         try {
//             const [statsData, devicesData, incidentsData] =
//                 await Promise.all([
//                     getStats(),
//                     getDevices(),
//                     getIncidents()
//                 ]);

//             setStats(statsData);
//             setDevices(devicesData);
//             setIncidents(incidentsData);
//             setError("");
//         } catch {
//             setError("Could not connect to the backend");
//         } finally {
//             setLoading(false);
//         }
//     }


//     // Updates the new-device form values
//     function handleDeviceInput(event) {
//         const { name, value } = event.target;

//         setNewDevice({
//             ...newDevice,
//             [name]: value
//         });
//     }


//     // Adds a new device through FastAPI
//     async function handleAddDevice(event) {
//         event.preventDefault();

//         if (
//             !newDevice.name ||
//             !newDevice.host ||
//             !newDevice.port ||
//             !newDevice.service ||
//             !newDevice.location
//         ) {
//             setError("Fill all device fields");
//             return;
//         }

//         try {
//             setAddingDevice(true);

//             await addDevice({
//                 ...newDevice,
//                 port: Number(newDevice.port)
//             });

//             setNewDevice({
//                 name: "",
//                 host: "",
//                 port: "",
//                 service: "",
//                 location: ""
//             });

//             await loadDashboard();
//         } catch {
//             setError("Could not add device");
//         } finally {
//             setAddingDevice(false);
//         }
//     }


//     // Triggers a new network scan
//     async function handleScan() {
//         try {
//             setScanning(true);

//             await runScan();
//             await loadDashboard();
//         } catch {
//             setError("Network scan failed");
//         } finally {
//             setScanning(false);
//         }
//     }


//     // Changes the status of an incident ticket
//     async function handleStatusChange(id, status) {
//         try {
//             await updateIncidentStatus(id, status);
//             await loadDashboard();
//         } catch {
//             setError("Could not update incident");
//         }
//     }


//     // Loads dashboard and refreshes displayed data every 10 seconds
//     useEffect(() => {
//         loadDashboard();

//         const interval = setInterval(() => {
//             loadDashboard();
//         }, 10000);

//         return () => clearInterval(interval);
//     }, []);


//     return (
//         <div className="dashboard">

//             <div className="header">
//                 <div>
//                     <h1>NetOps Incident Monitor</h1>

//                     <p className="subtitle">
//                         Network Operations Dashboard
//                     </p>
//                 </div>

//                 <button
//                     className="scan-button"
//                     onClick={handleScan}
//                     disabled={scanning}
//                 >
//                     {scanning ? "Scanning..." : "Scan Network"}
//                 </button>
//             </div>


//             {error && (
//                 <div className="error">
//                     {error}
//                 </div>
//             )}


//             {loading && (
//                 <p>Loading dashboard...</p>
//             )}


//             {stats && (
//                 <div className="cards">

//                     <div className="card">
//                         <h3>Total Incidents</h3>
//                         <p>{stats.total_incidents}</p>
//                     </div>

//                     <div className="card">
//                         <h3>Open</h3>
//                         <p>{stats.open}</p>
//                     </div>

//                     <div className="card">
//                         <h3>Acknowledged</h3>
//                         <p>{stats.acknowledged}</p>
//                     </div>

//                     <div className="card">
//                         <h3>Resolved</h3>
//                         <p>{stats.resolved}</p>
//                     </div>

//                     <div className="card">
//                         <h3>High Severity</h3>
//                         <p>{stats.high}</p>
//                     </div>

//                     <div className="card">
//                         <h3>Medium Severity</h3>
//                         <p>{stats.medium}</p>
//                     </div>

//                 </div>
//             )}


//             <section className="section">

//                 <h2>Device Inventory</h2>

//                 <div className="table-container">

//                     <form onSubmit={handleAddDevice}>

//                         <table>
//                             <thead>
//                                 <tr>
//                                     <th>Name</th>
//                                     <th>Host</th>
//                                     <th>Port</th>
//                                     <th>Service</th>
//                                     <th>Location</th>
//                                     <th>Action</th>
//                                 </tr>
//                             </thead>

//                             <tbody>

//                                 {devices.map((device) => (
//                                     <tr key={device[0]}>
//                                         <td>{device[1]}</td>
//                                         <td>{device[2]}</td>
//                                         <td>{device[3]}</td>
//                                         <td>{device[4]}</td>
//                                         <td>{device[5]}</td>
//                                         <td></td>
//                                     </tr>
//                                 ))}


//                                 <tr className="add-device-row">

//                                     <td>
//                                         <input
//                                             name="name"
//                                             placeholder="Device name"
//                                             value={newDevice.name}
//                                             onChange={handleDeviceInput}
//                                         />
//                                     </td>

//                                     <td>
//                                         <input
//                                             name="host"
//                                             placeholder="google.com"
//                                             value={newDevice.host}
//                                             onChange={handleDeviceInput}
//                                         />
//                                     </td>

//                                     <td>
//                                         <input
//                                             name="port"
//                                             type="number"
//                                             placeholder="443"
//                                             value={newDevice.port}
//                                             onChange={handleDeviceInput}
//                                         />
//                                     </td>

//                                     <td>
//                                         <input
//                                             name="service"
//                                             placeholder="HTTPS"
//                                             value={newDevice.service}
//                                             onChange={handleDeviceInput}
//                                         />
//                                     </td>

//                                     <td>
//                                         <input
//                                             name="location"
//                                             placeholder="External"
//                                             value={newDevice.location}
//                                             onChange={handleDeviceInput}
//                                         />
//                                     </td>

//                                     <td>
//                                         <button
//                                             type="submit"
//                                             className="add-button"
//                                             disabled={addingDevice}
//                                         >
//                                             {addingDevice ? "Adding..." : "Add Device"}
//                                         </button>
//                                     </td>

//                                 </tr>

//                             </tbody>
//                         </table>

//                     </form>

//                 </div>

//             </section>


//             <section className="section">

//                 <h2>Incident Tickets</h2>

//                 <div className="table-container">

//                     <table>
//                         <thead>
//                             <tr>
//                                 <th>ID</th>
//                                 <th>Host</th>
//                                 <th>Port</th>
//                                 <th>Issue</th>
//                                 <th>Severity</th>
//                                 <th>Status</th>
//                                 <th>Created</th>
//                                 <th>Action</th>
//                             </tr>
//                         </thead>

//                         <tbody>

//                             {incidents.map((incident) => (
//                                 <tr key={incident[0]}>

//                                     <td>{incident[0]}</td>
//                                     <td>{incident[1]}</td>
//                                     <td>{incident[2]}</td>
//                                     <td>{incident[3]}</td>

//                                     <td>
//                                         <span
//                                             className={
//                                                 `severity ${incident[4].toLowerCase()}`
//                                             }
//                                         >
//                                             {incident[4]}
//                                         </span>
//                                     </td>

//                                     <td>
//                                         <span
//                                             className={
//                                                 `status ${incident[5].toLowerCase()}`
//                                             }
//                                         >
//                                             {incident[5]}
//                                         </span>
//                                     </td>

//                                     <td>{incident[6]}</td>

//                                     <td>

//                                         {incident[5] === "OPEN" && (
//                                             <button
//                                                 className="action-button"
//                                                 onClick={() =>
//                                                     handleStatusChange(
//                                                         incident[0],
//                                                         "ACKNOWLEDGED"
//                                                     )
//                                                 }
//                                             >
//                                                 Acknowledge
//                                             </button>
//                                         )}


//                                         {incident[5] === "ACKNOWLEDGED" && (
//                                             <button
//                                                 className="action-button resolve"
//                                                 onClick={() =>
//                                                     handleStatusChange(
//                                                         incident[0],
//                                                         "RESOLVED"
//                                                     )
//                                                 }
//                                             >
//                                                 Resolve
//                                             </button>
//                                         )}


//                                         {incident[5] === "RESOLVED" && (
//                                             <span className="done">
//                                                 Done
//                                             </span>
//                                         )}

//                                     </td>

//                                 </tr>
//                             ))}

//                         </tbody>
//                     </table>

//                 </div>

//             </section>

//         </div>
//     );
// }

// export default App;



import { useEffect, useState } from "react";
import {
    getStats,
    getDevices,
    addDevice,
    getIncidents,
    getTopology,
    runScan,
    discoverNetwork,
    updateIncidentStatus
} from "./api";

import "./App.css";


function App() {
    const [stats, setStats] = useState(null);
    const [devices, setDevices] = useState([]);
    const [incidents, setIncidents] = useState([]);
    const [topology, setTopology] = useState(null);

    const [loading, setLoading] = useState(true);
    const [scanning, setScanning] = useState(false);
    const [discovering, setDiscovering] = useState(false);
    const [addingDevice, setAddingDevice] = useState(false);
    const [error, setError] = useState("");

    const [newDevice, setNewDevice] = useState({
        name: "",
        host: "",
        port: "",
        service: "",
        location: ""
    });


    // Loads all dashboard information from FastAPI
    async function loadDashboard() {
        try {
            const [
                statsData,
                devicesData,
                incidentsData,
                topologyData
            ] = await Promise.all([
                getStats(),
                getDevices(),
                getIncidents(),
                getTopology()
            ]);

            setStats(statsData);
            setDevices(devicesData);
            setIncidents(incidentsData);
            setTopology(topologyData);
            setError("");
        } catch {
            setError("Could not connect to the backend");
        } finally {
            setLoading(false);
        }
    }


    // Updates the new-device form values
    function handleDeviceInput(event) {
        const { name, value } = event.target;

        setNewDevice({
            ...newDevice,
            [name]: value
        });
    }


    // Adds a new device through FastAPI
    async function handleAddDevice(event) {
        event.preventDefault();

        if (
            !newDevice.name ||
            !newDevice.host ||
            !newDevice.port ||
            !newDevice.service ||
            !newDevice.location
        ) {
            setError("Fill all device fields");
            return;
        }

        try {
            setAddingDevice(true);

            await addDevice({
                ...newDevice,
                port: Number(newDevice.port)
            });

            setNewDevice({
                name: "",
                host: "",
                port: "",
                service: "",
                location: ""
            });

            await loadDashboard();
        } catch {
            setError("Could not add device");
        } finally {
            setAddingDevice(false);
        }
    }


    // Triggers one network scan
    async function handleScan() {
        try {
            setScanning(true);

            await runScan();
            await loadDashboard();
        } catch {
            setError("Network scan failed");
        } finally {
            setScanning(false);
        }
    }


    // Runs traceroute discovery for registered devices
    async function handleDiscovery() {
        try {
            setDiscovering(true);

            await discoverNetwork();
            await loadDashboard();
        } catch {
            setError("Network path discovery failed");
        } finally {
            setDiscovering(false);
        }
    }


    // Changes the status of an incident ticket
    async function handleStatusChange(id, status) {
        try {
            await updateIncidentStatus(id, status);
            await loadDashboard();
        } catch {
            setError("Could not update incident");
        }
    }


    // Gets discovered hops belonging to one device
    function getDeviceHops(deviceId) {
        if (!topology) {
            return [];
        }

        return topology.discovered_routes
            .filter((route) => route[0] === deviceId)
            .sort((a, b) => a[3] - b[3]);
    }


    // Loads the dashboard and refreshes displayed data every 10 seconds
    useEffect(() => {
        loadDashboard();

        const interval = setInterval(() => {
            loadDashboard();
        }, 10000);

        return () => clearInterval(interval);
    }, []);


    return (
        <div className="dashboard">

            <div className="header">
                <div>
                    <h1>NetOps Incident Monitor</h1>

                    <p className="subtitle">
                        Network Operations Dashboard
                    </p>
                </div>

                <button
                    className="scan-button"
                    onClick={handleScan}
                    disabled={scanning}
                >
                    {scanning ? "Scanning..." : "Scan Network"}
                </button>
            </div>


            {error && (
                <div className="error">
                    {error}
                </div>
            )}


            {loading && (
                <p>Loading dashboard...</p>
            )}


            {stats && (
                <div className="cards">

                    <div className="card">
                        <h3>Total Incidents</h3>
                        <p>{stats.total_incidents}</p>
                    </div>

                    <div className="card">
                        <h3>Open</h3>
                        <p>{stats.open}</p>
                    </div>

                    <div className="card">
                        <h3>Acknowledged</h3>
                        <p>{stats.acknowledged}</p>
                    </div>

                    <div className="card">
                        <h3>Resolved</h3>
                        <p>{stats.resolved}</p>
                    </div>

                    <div className="card">
                        <h3>High Severity</h3>
                        <p>{stats.high}</p>
                    </div>

                    <div className="card">
                        <h3>Medium Severity</h3>
                        <p>{stats.medium}</p>
                    </div>

                </div>
            )}


            <section className="section">

                <h2>Device Inventory</h2>

                <div className="table-container">

                    <form onSubmit={handleAddDevice}>

                        <table>
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Host</th>
                                    <th>Port</th>
                                    <th>Service</th>
                                    <th>Location</th>
                                    <th>Action</th>
                                </tr>
                            </thead>

                            <tbody>

                                {devices.map((device) => (
                                    <tr key={device[0]}>
                                        <td>{device[1]}</td>
                                        <td>{device[2]}</td>
                                        <td>{device[3]}</td>
                                        <td>{device[4]}</td>
                                        <td>{device[5]}</td>
                                        <td></td>
                                    </tr>
                                ))}


                                <tr className="add-device-row">

                                    <td>
                                        <input
                                            name="name"
                                            placeholder="Device name"
                                            value={newDevice.name}
                                            onChange={handleDeviceInput}
                                        />
                                    </td>

                                    <td>
                                        <input
                                            name="host"
                                            placeholder="google.com"
                                            value={newDevice.host}
                                            onChange={handleDeviceInput}
                                        />
                                    </td>

                                    <td>
                                        <input
                                            name="port"
                                            type="number"
                                            placeholder="443"
                                            value={newDevice.port}
                                            onChange={handleDeviceInput}
                                        />
                                    </td>

                                    <td>
                                        <input
                                            name="service"
                                            placeholder="HTTPS"
                                            value={newDevice.service}
                                            onChange={handleDeviceInput}
                                        />
                                    </td>

                                    <td>
                                        <input
                                            name="location"
                                            placeholder="External"
                                            value={newDevice.location}
                                            onChange={handleDeviceInput}
                                        />
                                    </td>

                                    <td>
                                        <button
                                            type="submit"
                                            className="add-button"
                                            disabled={addingDevice}
                                        >
                                            {addingDevice
                                                ? "Adding..."
                                                : "Add Device"}
                                        </button>
                                    </td>

                                </tr>

                            </tbody>
                        </table>

                    </form>

                </div>

            </section>


            <section className="section">

                <h2>Incident Tickets</h2>

                <div className="table-container">

                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Host</th>
                                <th>Port</th>
                                <th>Issue</th>
                                <th>Severity</th>
                                <th>Status</th>
                                <th>Created</th>
                                <th>Action</th>
                            </tr>
                        </thead>

                        <tbody>

                            {incidents.map((incident) => (
                                <tr key={incident[0]}>

                                    <td>{incident[0]}</td>
                                    <td>{incident[1]}</td>
                                    <td>{incident[2]}</td>
                                    <td>{incident[3]}</td>

                                    <td>
                                        <span
                                            className={
                                                `severity ${incident[4].toLowerCase()}`
                                            }
                                        >
                                            {incident[4]}
                                        </span>
                                    </td>

                                    <td>
                                        <span
                                            className={
                                                `status ${incident[5].toLowerCase()}`
                                            }
                                        >
                                            {incident[5]}
                                        </span>
                                    </td>

                                    <td>{incident[6]}</td>

                                    <td>

                                        {incident[5] === "OPEN" && (
                                            <button
                                                className="action-button"
                                                onClick={() =>
                                                    handleStatusChange(
                                                        incident[0],
                                                        "ACKNOWLEDGED"
                                                    )
                                                }
                                            >
                                                Acknowledge
                                            </button>
                                        )}


                                        {incident[5] === "ACKNOWLEDGED" && (
                                            <button
                                                className="action-button resolve"
                                                onClick={() =>
                                                    handleStatusChange(
                                                        incident[0],
                                                        "RESOLVED"
                                                    )
                                                }
                                            >
                                                Resolve
                                            </button>
                                        )}


                                        {incident[5] === "RESOLVED" && (
                                            <span className="done">
                                                Done
                                            </span>
                                        )}

                                    </td>

                                </tr>
                            ))}

                        </tbody>
                    </table>

                </div>

            </section>


            <section className="section">

                <div className="topology-header">

                    <div>
                        <h2>Network Paths</h2>

                        <p className="topology-description">
                            Layer-3 paths discovered using traceroute
                        </p>
                    </div>

                    <button
                        className="discover-button"
                        onClick={handleDiscovery}
                        disabled={discovering}
                    >
                        {discovering
                            ? "Discovering..."
                            : "Discover Paths"}
                    </button>

                </div>


                <div className="topology-grid">

                    {devices.map((device) => {
                        const hops = getDeviceHops(device[0]);

                        return (
                            <div
                                className="route-card"
                                key={device[0]}
                            >

                                <div className="route-title">
                                    <h3>{device[1]}</h3>
                                    <span>{device[2]}</span>
                                </div>


                                {hops.length === 0 ? (

                                    <p className="no-route">
                                        No discovered route
                                    </p>

                                ) : (

                                    <div className="route">

                                        <div className="route-node source">
                                            <strong>Your Computer</strong>
                                        </div>

                                        {hops.map((hop) => (
                                            <div
                                                className="route-step"
                                                key={`${device[0]}-${hop[3]}`}
                                            >

                                                <div className="route-line">
                                                    ↓
                                                </div>

                                                <div className="route-node hop">
                                                    <span>
                                                        Hop {hop[3]}
                                                    </span>

                                                    <strong>
                                                        {hop[4]}
                                                    </strong>
                                                </div>

                                            </div>
                                        ))}

                                        <div className="route-line">
                                            ↓
                                        </div>

                                        <div className="route-node destination">
                                            <strong>
                                                {device[1]}
                                            </strong>

                                            <span>
                                                {device[2]}
                                            </span>
                                        </div>

                                    </div>

                                )}

                            </div>
                        );
                    })}

                </div>

            </section>

        </div>
    );
}


export default App;

