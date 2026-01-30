import psutil
import time
import os

def get_currently_listening():
    """Returns a set of active listening ports."""
    connections = psutil.net_connections(kind='inet')
    # We use a set for easy comparison logic
    return {conn.laddr.port for conn in connections if conn.status == 'LISTEN'}

def monitor():
    print("--- Security Watcher Mode Active ---")
    print("Capturing baseline... (Press Ctrl+C to stop)")
    
    # Step 1: Establish the baseline
    baseline_ports = get_currently_listening()
    print(f"Initial Open Ports: {baseline_ports}")
    
    try:
        while True:
            time.sleep(10) # Wait 10 seconds between checks
            current_ports = get_currently_listening()
            
            # Step 2: Compare
            new_ports = current_ports - baseline_ports
            closed_ports = baseline_ports - current_ports
            
            # Step 3: Alert
            if new_ports:
                for port in new_ports:
                    print(f"\n[!] ALERT: New port opened: {port}")
                # Update baseline so we don't alert again for the same port
                baseline_ports.update(new_ports)
                
            if closed_ports:
                for port in closed_ports:
                    print(f"\n[i] Info: Port closed: {port}")
                baseline_ports.difference_update(closed_ports)
                
    except KeyboardInterrupt:
        print("\nWatcher stopped by user.")

if __name__ == "__main__":
    monitor()