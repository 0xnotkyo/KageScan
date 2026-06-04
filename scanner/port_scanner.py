import socket
import concurrent.futures
import re

class PortScanner:
    
    def __init__(self, target, ports, threads=100, timeout=1.0):
        self.target = target
        self.ports = ports
        self.threads = threads
        self.timeout = timeout
        
    def scan_port(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        
        try:
            result = sock.connect_ex((self.target, port))
            if result == 0:
                return port
        except:
            pass
        finally:
            sock.close()
        return None
    
    def scan(self):
        open_ports = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            future_to_port = {executor.submit(self.scan_port, port): port for port in self.ports}
            for future in concurrent.futures.as_completed(future_to_port):
                port = future_to_port[future]
                try:
                    result = future.result()
                    if result:
                        open_ports.append(result)
                        print(f"[+] Port {result} is OPEN")
                except:
                    pass
        return sorted(open_ports)
    
    def detect_service(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3.0)
            sock.connect((self.target, port))
            
            if port in [80, 443, 8080, 8443]:
                try:
                    sock.send(b"GET / HTTP/1.1\r\nHost: " + self.target.encode() + b"\r\n\r\n")
                    response = sock.recv(1024).decode(errors='ignore')
                    match = re.search(r'Server: (.*)', response, re.IGNORECASE)
                    if match:
                        return match.group(1).strip()
                    return "Web Server"
                except:
                    pass

            sock.send(b"\n")
            banner = sock.recv(1024).decode(errors='ignore')
            sock.close()
            
            if banner:
                clean_banner = re.sub(r'[\x00-\x1f\x7f]', ' ', banner).strip()
                clean_banner = clean_banner.split(' ')[0].strip()
                return clean_banner[:30]
            
            return "Unknown Service"
            
        except:
            return "Unknown Service"
    
    def detect_services(self, open_ports):
        services = {}
        print(f"[*] Detecting services on {len(open_ports)} ports...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(self.detect_service, port): port for port in open_ports}
            for future in concurrent.futures.as_completed(futures):
                port = futures[future]
                try:
                    service = future.result()
                    services[port] = service
                    print(f"[+] Port {port}: {service}")
                except:
                    services[port] = "Unknown"
        return services
