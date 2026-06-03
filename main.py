#!/usr/bin/env python3

import argparse
import sys
import json
import subprocess
from datetime import datetime
from scanner import PortScanner, DirectoryEnumerator, OutputFormatter

def banner():
    print(r"""
    ██╗  ██╗ █████╗  ██████╗ ███████╗███████╗ ██████╗  █████╗ ███╗   ██╗
    ██║ ██╔╝██╔══██╗██╔════╝ ██╔════╝██╔════╝██╔════╝ ██╔══██╗████╗  ██║
    █████╔╝ ███████║██║  ███╗█████╗  ███████╗██║      ███████║██╔██╗ ██║
    ██╔═██╗ ██╔══██║██║   ██║██╔══╝  ╚════██║██║      ██╔══██║██║╚██╗██║
    ██║  ██╗██║  ██║╚██████╔╝███████╗███████║╚██████╗ ██║  ██║██║ ╚████║
    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝
    
              [ Network Enumeration Tool | By 0xnotkyo]
    """)

def parse_ports(port_string):
    return [int(p.strip()) for p in port_string.split(',')]

def main():
    parser = argparse.ArgumentParser(
        description="KageScan - Network Enumeration Tool",
        usage="./main.py [TARGET] [OPTIONS]",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Example: python3 main.py 192.168.1.1 -p 80,443,22 -s --directory-scan"
    )
    
    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("-p", "--ports", default="80,443,22", help="Ports range (e.g., 21,22,80,443)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads (def: 100)")
    parser.add_argument("-o", "--output", help="Save results to JSON file")
    parser.add_argument("--directory-scan", action="store_true", help="Enable directory enumeration")
    parser.add_argument("--gobuster", action="store_true", help="Use gobuster for enumeration")
    parser.add_argument("-w", "--wordlist", default="wordlists/common.txt", help="Wordlist file for enumeration")
    parser.add_argument("--timeout", type=float, default=1.0, help="Connection timeout")
    parser.add_argument("-s", "--service-detection", action="store_true", help="Enable service detection")
    parser.add_argument("-c", "--copy", action="store_true", help="Copy open ports to clipboard (requires xclip)")
    
    if len(sys.argv) == 1:
        banner()
        parser.print_help()
        sys.exit(0)
        
    args = parser.parse_args()
    banner()
    
    start_time = datetime.now()
    ports_to_scan = parse_ports(args.ports)
    
    scanner = PortScanner(args.target, ports_to_scan, args.threads, args.timeout)
    open_ports = scanner.scan()
    
    services = scanner.detect_services(open_ports) if args.service_detection else {}
    
    directory_results = {}
    if args.directory_scan and open_ports:
        web_ports = [p for p in open_ports if p in [80, 443, 8080, 8000, 8443, 3000]]
        if web_ports:
            enum = DirectoryEnumerator(args.target, args.wordlist, args.gobuster)
            directory_results = enum.enumerate(web_ports)
    
    end_time = datetime.now()
    results = {
        "target": args.target,
        "scan_start": start_time.isoformat(),
        "scan_end": end_time.replace(microsecond=0).isoformat(),
        "duration_seconds": (end_time - start_time).total_seconds(),
        "open_ports": open_ports,
        "services": services,
        "directory_results": directory_results
    }
    
    OutputFormatter(args.target).print_results(results)
    
    if args.copy and open_ports:
        try:
            ports_str = ",".join(map(str, open_ports))
            process = subprocess.Popen(['xclip', '-sel', 'clip'], stdin=subprocess.PIPE)
            process.communicate(input=ports_str.encode())
            print(f"\n[*] Ports copied to clipboard: {ports_str}")
        except FileNotFoundError:
            print("\n[!] Error: xclip is not installed. Install it with 'sudo apt install xclip'")
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        sys.exit(1)
