import nmap
import logging

logger = logging.getLogger("PortTracker")

class NetworkAuditor:
    def __init__(self):
        # Initialize the Nmap PortScanner
        self.nm = nmap.PortScanner()

    def scan_port(self, host, port):
        """
        Performs a detailed service/version scan on a specific port.
        """
        logger.info(f"🔍 Starting external audit on {host}:{port}...")
        
        # -sV: Service/Version detection
        # -T4: Faster execution
        try:
            self.nm.scan(host, str(port), arguments='-sV -T4')
            
            # Navigate the Nmap XML results
            if host in self.nm.all_hosts():
                port_data = self.nm[host]['tcp'][int(port)]
                
                service = port_data.get('name', 'unknown')
                product = port_data.get('product', 'unknown')
                version = port_data.get('version', 'unknown')
                state = port_data.get('state', 'unknown')

                result = f"Audit Result: Port {port} is {state}. Service: {service} {product} {version}"
                return result
            return "Audit failed: Host unreachable."
            
        except Exception as e:
            return f"Audit Error: {str(e)}"