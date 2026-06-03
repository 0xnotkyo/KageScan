import subprocess
import os
import requests
import tempfile
from concurrent.futures import ThreadPoolExecutor

class DirectoryEnumerator:
    
    def __init__(self, target, wordlist="wordlists/common.txt", use_gobuster=False):
        self.target = target
        self.wordlist = wordlist
        self.use_gobuster = use_gobuster
    
    def check_gobuster_installed(self):
        try:
            result = subprocess.run(['gobuster', '--version'], capture_output=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def enumerate_with_gobuster(self, port):
        if not self.check_gobuster_installed():
            print("[!] Gobuster not found")
            return []
        
        protocol = "https" if port in [443, 8443] else "http"
        url = f"{protocol}://{self.target}:{port}"
        
        directories = []
        with tempfile.NamedTemporaryFile(mode='w+', delete=True) as tmp_output:
            cmd = [
                'gobuster', 'dir', '-u', url, '-w', self.wordlist, 
                '-t', '50', '-q', '--no-error', '-o', tmp_output.name
            ]
            
            if protocol == "https":
                cmd.append('-k')
            
            try:
                subprocess.run(cmd, timeout=300)
                
                tmp_output.seek(0)
                lines = tmp_output.readlines()
                
                for line in lines:
                    if line.strip():
                        path = line.split()[0].replace(',', '')
                        directories.append(path)
                        print(f"[+] Found: {url}{path}")
            
            except subprocess.TimeoutExpired:
                print(f"[!] Gobuster timed out on port {port}")
            except Exception as e:
                print(f"[!] Error running gobuster: {e}")
        
        return directories
    
    def enumerate_manually(self, port, directories):
        protocol = "https" if port in [443, 8443] else "http"
        base_url = f"{protocol}://{self.target}:{port}"
        found = []
        
        try:
            response = requests.get(base_url, timeout=5, allow_redirects=False)
            print(f"[+] {base_url} -> Status: {response.status_code}")
        except:
            pass
        
        if not os.path.exists(self.wordlist):
            print(f"[!] Warning: Wordlist file '{self.wordlist}' not found.")
        
        wordlist_dirs = []
        if os.path.exists(self.wordlist):
            with open(self.wordlist, 'r') as f:
                wordlist_dirs = [line.strip() for line in f if line.strip()]
        else:
            wordlist_dirs = [
                '/', '/admin', '/administrator', '/api', '/backup', '/blog',
                '/config', '/css', '/dashboard', '/dev', '/download', '/img',
                '/images', '/index.html', '/js', '/login', '/portal',
                '/private', '/public', '/test', '/tmp', '/upload', '/uploads'
            ]
        
        def check_directory(path):
            try:
                url = f"{base_url}{path}"
                response = requests.get(url, timeout=3, allow_redirects=False)
                
                if response.status_code == 200:
                    return path
                elif response.status_code in [301, 302]:
                    return f"{path} (redirect)"
                elif response.status_code == 403:
                    return f"{path} (forbidden)"
                elif response.status_code == 401:
                    return f"{path} (auth required)"
            except:
                pass
            return None
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(check_directory, path): path for path in wordlist_dirs}
            
            for future in futures:
                result = future.result()
                if result:
                    found.append(result)
                    print(f"[+] Found: {base_url}{result}")
        
        return found
    
    def enumerate(self, ports):
        results = {}
        for port in ports:
            print(f"\n[*] Enumerating directories on port {port}...")
            
            if self.use_gobuster and self.check_gobuster_installed():
                directories = self.enumerate_with_gobuster(port)
            else:
                directories = self.enumerate_manually(port, [])
            
            results[port] = directories
        
        return results
