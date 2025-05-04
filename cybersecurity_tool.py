
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
import logging
from urllib.parse import urlparse

# Setup logging
logging.basicConfig(filename='scan_results.log', level=logging.INFO, format='%(asctime)s - %(message)s')

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
    logging.info(f"Scanning {url}...")
    
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

    # Display results
    print("
--- Scan Results ---")
    if outdated_libs:
        print("Outdated Libraries:")
        for lib in outdated_libs:
            print(lib)
        logging.info("Outdated Libraries:")
        for lib in outdated_libs:
            logging.info(lib)
    else:
        print("No outdated libraries detected.")
        logging.info("No outdated libraries detected.")
    
    if exposed_panels:
        print("Exposed Admin Panels:")
        for panel in exposed_panels:
            print(panel)
        logging.info("Exposed Admin Panels:")
        for panel in exposed_panels:
            logging.info(panel)
    else:
        print("No exposed admin panels found.")
        logging.info("No exposed admin panels found.")
    
    if missing_headers:
        print("Missing Security Headers:")
        for header in missing_headers:
            print(header)
        logging.info("Missing Security Headers:")
        for header in missing_headers:
            logging.info(header)
    else:
        print("All critical security headers are present.")
        logging.info("All critical security headers are present.")
    
    if advanced_vulns:
        print("Advanced Vulnerabilities Detected:")
        for vuln in advanced_vulns:
            print(vuln)
        logging.info("Advanced Vulnerabilities Detected:")
        for vuln in advanced_vulns:
            logging.info(vuln)
    else:
        print("No advanced vulnerabilities detected.")
        logging.info("No advanced vulnerabilities detected.")

# Example usage
url = input("Enter the website URL to scan: ")
scan_website(url)
