import psutil
import datetime
import os
import pandas as pd

def get_listening_ports():
    """
    Scans the local system for all listening network connections
    and maps them to their respective processes.
    """
    connections = psutil.net_connections(kind='inet')
    results = []

    for conn in connections:
        # We only care about ports that are actively "LISTENING" for incoming traffic
        if conn.status == 'LISTEN':
            try:
                # Attempt to get process details
                process = psutil.Process(conn.pid)
                proc_name = process.name()
                status = "Authorized" # You can later add logic to flag 'Unauthorized'
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                proc_name = "N/A (Access Denied)"
                status = "Hidden/System"

            results.append({
                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "IP_Address": conn.laddr.ip,
                "Port": conn.laddr.port,
                "PID": conn.pid,
                "Process_Name": proc_name,
                "Status": status
            })
    
    return results

def save_log(data):
    """Saves the scan results to a CSV file for security auditing."""
    file_name = "port_audit_log.csv"
    df = pd.DataFrame(data)
    
    # If the file doesn't exist, create it with headers. 
    # If it does, append the new scan results.
    if not os.path.isfile(file_name):
        df.to_csv(file_name, index=False)
    else:
        df.to_csv(file_name, mode='a', header=False, index=False)
    
    print(f"\n[+] Audit complete. Results saved to {file_name}")

if __name__ == "__main__":
    print("--- Secure Port Tracker Active ---")
    
    try:
        active_ports = get_listening_ports()
        
        # Print a clean table to the console
        if active_ports:
            print(pd.DataFrame(active_ports)[["Port", "Process_Name", "IP_Address", "PID"]])
            save_log(active_ports)
        else:
            print("No listening ports detected.")
            
    except PermissionError:
        print("ERROR: Please run PowerShell/VS Code as Administrator to see process details.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")