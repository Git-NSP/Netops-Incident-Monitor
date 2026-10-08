# Decides the probable issue and severity based on network check results
def triage_incident(dns_ok, ping_ok, port_ok, http_ok):
    if not dns_ok:
        return "DNS or hostname resolution issue", "HIGH"

    if dns_ok and not ping_ok and not port_ok:
        return "Host may be unreachable or network path may be blocked", "HIGH"

    if ping_ok and not port_ok:
        return "Service or TCP port unavailable", "HIGH"

    if port_ok and not http_ok:
        return "Web application/service is not responding correctly", "MEDIUM"

    return "No issue detected", "LOW"

