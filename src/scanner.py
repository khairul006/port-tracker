import psutil

def get_listening_ports():
    """Returns a list of dictionaries with current listening port info."""
    connections = psutil.net_connections(kind='inet')
    results = []
    for conn in connections:
        if conn.status == 'LISTEN':
            try:
                proc = psutil.Process(conn.pid)
                name = proc.name()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                name = "Unknown"
            
            results.append({
                "port": conn.laddr.port,
                "ip": conn.laddr.ip,
                "process": name,
                "pid": conn.pid
            })
    return results