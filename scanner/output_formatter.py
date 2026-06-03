class OutputFormatter:
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    RED    = '\033[91m'
    BLUE   = '\033[94m'
    CYAN   = '\033[96m'
    RESET  = '\033[0m'

    def __init__(self, target):
        self.target = target

    def print_results(self, results):
        print(f"\n{self.BLUE}#========================================")
        print(f" SCAN REPORT: {self.target}")
        print(f"========================================{self.RESET}")
        
        if results.get('open_ports'):
            print(f"\n{self.YELLOW}[*] Open Ports:{self.RESET}")
            # Increased width to 30 for the new Banner Grabbing info
            print(f"{'PORT':<10} {'SERVICE / BANNER':<30}")
            print(f"{'-'*45}")
            for port in results['open_ports']:
                service = results.get('services', {}).get(port, "Unknown")
                print(f"  {self.GREEN}{port:<10}{service:<30}{self.RESET}")
        else:
            print(f"\n{self.RED}[!] No open ports found.{self.RESET}")

        if results.get('directory_results'):
            print(f"\n{self.YELLOW}[*] Directory Enumeration:{self.RESET}")
            for port, dirs in results['directory_results'].items():
                if dirs:
                    print(f"  {self.CYAN}Port {port}:{self.RESET}")
                    for path in dirs:
                        print(f"    {self.GREEN}[+] {path}{self.RESET}")
        
        print(f"\n{self.BLUE}#========================================{self.RESET}\n")
