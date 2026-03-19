import requests
from bs4 import BeautifulSoup
import sys
import time
import re
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

BANNER = f"""
{Fore.CYAN}==================================================
{Fore.YELLOW}       🇮🇳  TRACE OSINT - INDIA v3.0 🇮🇳
{Fore.CYAN}==================================================
{Fore.WHITE}  Advanced Indian Phone Number Tracking Tool
{Fore.WHITE}  Features: Operator, Circle, Maps & Nokos Check
{Fore.CYAN}==================================================
"""

def trace_india_pro(number: str):
    # 1. Strict Validation (Requirement: Must be India & 10 Digits)
    clean_num = re.sub(r'\D', '', number)
    
    # Handle +91 or 91 prefix
    if len(clean_num) > 10 and clean_num.startswith('91'):
        clean_num = clean_num[2:]
    
    if len(clean_num) != 10:
        print(f"{Fore.RED}[!] ERROR: This tool is strictly for INDIAN numbers (+91).")
        print(f"{Fore.RED}[!] Please enter exactly 10 digits.")
        return

    print(f"{Fore.BLUE}[*] Initializing OSINT Scan for: +91 {clean_num}...")
    time.sleep(1)

    # 2. URL and Connection
    # We use the path version from your friend's code as it's often more stable
    url = f"https://calltracer.in/in/{clean_num}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }

    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        
        data = {}

        # 3. Data Extraction (Enhanced)
        # Get Title
        if soup.title:
            data["Search Title"] = soup.title.string.strip()

        # Get Table Details
        for table in soup.select("table.trace-details"):
            for row in table.select("tr"):
                cols = row.find_all("td")
                if len(cols) == 2:
                    key = cols[0].get_text(strip=True).replace(":", "")
                    val = cols[1].get_text(strip=True)
                    data[key] = val

        # Get Maps Coordinates (Friend's logic - excellent addition!)
        iframe = soup.find("iframe")
        if iframe and iframe.get("src") and "q=" in iframe["src"]:
            coords = iframe["src"].split("q=")[1].split("&")[0]
            data["Coordinates"] = coords
            data["Google Maps"] = f"https://www.google.com/maps?q={coords}"

        # 4. Logical Check for NOKOS (Requirement)
        # If network/operator is missing, it's a dead number
        if not data or "Network" not in str(data):
            print(f"{Fore.RED}\n[X] RESULT: NUMBER INACTIVE / UNALLOCATED")
            print(f"{Fore.RED}[!] This number is 'Nokos' or not registered in India's database.")
            return

        # 5. Professional Output
        print(f"{Fore.GREEN}\n[+] DATA FOUND SUCCESSFULLY:")
        print(f"{Fore.CYAN}" + "-"*45)
        for k, v in data.items():
            print(f"{Fore.WHITE}{k:<18}: {Fore.YELLOW}{v}")
        print(f"{Fore.CYAN}" + "-"*45)
        print(f"{Fore.MAGENTA}[INFO] Scan completed at {time.strftime('%H:%M:%S')}")

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[ERROR] Connection failed: {e}")
    except Exception as e:
        print(f"{Fore.RED}[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    print(BANNER)
    try:
        target = input(Fore.WHITE + "Enter Indian Number (e.g., 9818338017): ").strip()
        trace_india_pro(target)
    except KeyboardInterrupt:
        sys.exit(f"\n{Fore.RED}[!] Process terminated by user.")
