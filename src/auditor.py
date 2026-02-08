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
        # --script=banner: Grabs the initial text the service sends (very useful!)
        try:
            self.nm.scan(host, str(port), arguments='-sV --script=banner -T4')
            
            # Navigate the Nmap XML results
            if host in self.nm.all_hosts():
                p_data = self.nm[host]['tcp'][int(port)]
            
                # Extract detailed fields
                audit_info = {
                    "service": p_data.get('name'),
                    "product": p_data.get('product'),
                    "version": p_data.get('version'),
                    "cpe": p_data.get('cpe', ''),
                    "script": str(p_data.get('script', 'None')), # Script outputs (like banner)
                    "state": p_data.get('state')
                }
                # result = f"Audit Result: Port {port} is {state}. Service: {service} {product} {version}"
                return audit_info

            return "Audit failed: Host unreachable."
            
        except Exception as e:
            logger.error(f"Nmap Error: {e}")
            return None