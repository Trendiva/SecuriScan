import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
import logging
import os
from urllib.parse import urlparse
from termcolor import colored

# Setup logging
output_folder = "SecuriScan_Results"
os.makedirs(output_folder, exist_ok=True)
log_file = os.path.join(output_folder, 'securescan_results.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# Branding
tool_name = "SecuriScan"
print(colored(f"--- Welcome to {tool_name} ---", 'cyan'))

# Retry logic for failed requests
def make_request(url, retries=3, timeout=5):
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=timeout)
            return response
        except requests.exceptions.RequestException as e:
            logging.error(f"Error: {e} - Retrying {attempt + 1}/{retries}...")
            time.sleep(2)  # Wait before retrying
    logging.error(f"Failed to fetch {url} after {retries} retries")
    return None

# Check if the URL is a local environment (localhost or 127.0.0.1)
def is_local_environment(url):
    parsed_url = urlparse(url)
    return parsed_url.hostname in ["localhost", "127.0.0.1"]

# Function to check for outdated libraries
def check_outdated_libraries(url):
    outdated_libraries = []
    known_vulnerable_versions = {
        "jquery": ["3.5.1", "3.4.1"],
        "bootstrap": ["3.3.7", "4.0.0"],
    }
    
    response = make_request(url)
    if not response:
        return ["Failed to fetch page"]
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    for script in soup.find_all("script"):
        src = script.get("src", "")
        for lib in known_vulnerable_versions:
            if lib in src:
                for version in known_vulnerable_versions[lib]:
                    if version in src:
                        outdated_libraries.append(f"Vulnerable {lib} version found: {version} in {src}")
    
    return outdated_libraries

# Function to check for exposed admin panels (skip for local environments)
def check_admin_panels(url):
    if is_local_environment(url):
        return ["Skipping admin panel check for local environment"]

    admin_panels = ["/admin", "/wp-admin", "/administrator"]
    exposed_panels = []
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(make_request, url + panel) for panel in admin_panels]
        for future in concurrent.futures.as_completed(futures):
            response = future.result()
            if response and response.status_code == 200:
                exposed_panels.append(f"Exposed admin panel found: {url}{admin_panels[futures.index(future)]}")
    
    return exposed_panels

# Function to check for important HTTP security headers
def check_http_headers(url):
    security_headers = [
        "Strict-Transport-Security", 
        "X-Content-Type-Options", 
        "X-XSS-Protection"
    ]
    missing_headers = []
    
    response = make_request(url)
    if not response:
        return ["Failed to fetch headers"]
    
    for header in security_headers:
        if header not in response.headers:
            missing_headers.append(f"Missing HTTP header: {header}")
    
    return missing_headers

# AI-based vulnerability detection (e.g., CSRF, Directory Traversal)
def check_for_advanced_vulnerabilities(url):
    advanced_vulnerabilities = []
    
    # CSRF Detection: Look for forms that don't have anti-CSRF tokens
    csrf_pattern = "input type='hidden' name='_csrf' value="
    response = make_request(url)
    if response and csrf_pattern not in response.text:
        advanced_vulnerabilities.append(f"Potential CSRF vulnerability detected in {url}")
    
    # Directory Traversal: Look for signs of file path manipulation (e.g., ../)
    traversal_pattern = "../"
    if traversal_pattern in response.text:
        advanced_vulnerabilities.append(f"Potential Directory Traversal vulnerability detected in {url}")
    
    return advanced_vulnerabilities

# Main function to perform the scan
def scan_website(url):
    logging.info(f"Scanning {url} with {tool_name}...")
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            'libraries': executor.submit(check_outdated_libraries, url),
            'admin_panels': executor.submit(check_admin_panels, url),
            'headers': executor.submit(check_http_headers, url),
            'advanced_vulnerabilities': executor.submit(check_for_advanced_vulnerabilities, url),
        }
        
        outdated_libs = futures['libraries'].result()
        exposed_panels = futures['admin_panels'].result()
        missing_headers = futures['headers'].result()
        advanced_vulns = futures['advanced_vulnerabilities'].result()

    # Display results with branding
    print(colored(f"\n--- {tool_name} Scan Results ---", 'cyan'))
    
    output_file = os.path.join(output_folder, f"{url.replace('https://', '').replace('http://', '').replace('/', '_')}_scan.txt")
    with open(output_file, 'w') as f:
        if outdated_libs:
            f.write("Outdated Libraries:\n")
            for lib in outdated_libs:
                f.write(lib + '\n')
                print(colored(lib, 'red'))
            logging.info("Outdated Libraries: " + ", ".join(outdated_libs))
        else:
            f.write("No outdated libraries detected.\n")
            print(colored("No outdated libraries detected.", 'green'))
        
        if exposed_panels:
            f.write("\nExposed Admin Panels:\n")
            for panel in exposed_panels:
                f.write(panel + '\n')
                print(colored(panel, 'yellow'))
            logging.info("Exposed Admin Panels: " + ", ".join(exposed_panels))
        else:
            f.write("No exposed admin panels found.\n")
            print(colored("No exposed admin panels found.", 'green'))
        
        if missing_headers:
            f.write("\nMissing Security Headers:\n")
            for header in missing_headers:
                f.write(header + '\n')
                print(colored(header, 'yellow'))
            logging.info("Missing Security Headers: " + ", ".join(missing_headers))
        else:
            f.write("All critical security headers are present.\n")
            print(colored("All critical security headers are present.", 'green'))
        
        if advanced_vulns:
            f.write("\nAdvanced Vulnerabilities Detected:\n")
            for vuln in advanced_vulns:
                f.write(vuln + '\n')
                print(colored(vuln, 'red'))
            logging.info("Advanced Vulnerabilities Detected: " + ", ".join(advanced_vulns))
        else:
            f.write("No advanced vulnerabilities detected.\n")
            print(colored("No advanced vulnerabilities detected.", 'green'))

    print(colored(f"Scan results saved to: {output_file}", 'cyan'))

# Example usage
url = input(f"Enter the website URL to scan using {tool_name}: ")
scan_website(url)

# Pause the execution at the end
input("Press Enter to exit...")
