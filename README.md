
# SecuriScan

**SecuriScan** is an advanced Python-based cybersecurity tool designed to automate the process of scanning websites for a wide range of security vulnerabilities and misconfigurations. By detecting common and complex threats, **SecuriScan** empowers web administrators, developers, and security professionals to proactively secure their websites.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Installation & Requirements](#installation--requirements)
- [Usage](#usage)
- [Example Usage](#example-usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

In today's digital age, ensuring the security of your website is more crucial than ever. **SecuriScan** helps you identify common security flaws such as outdated libraries, exposed admin panels, missing security headers, and advanced vulnerabilities like Cross-Site Request Forgery (CSRF), XSS, and SQL Injection. This tool offers an automated way to analyze and assess the security posture of any website, making it ideal for securing both production environments and local development sites.

## Key Features

**SecuriScan** offers the following key features:

- **Outdated Libraries Detection**: 
    - Scans for vulnerable or outdated versions of popular libraries such as jQuery, Bootstrap, and others.
    - Prevents exploits from known vulnerabilities in libraries.

- **Exposed Admin Panels**: 
    - Detects common admin panel paths (e.g., `/admin`, `/wp-admin`, `/administrator`).
    - Identifies publicly exposed admin panels that could be vulnerable to brute-force or unauthorized access.

- **Missing Security Headers**: 
    - Checks for missing HTTP security headers like `Strict-Transport-Security`, `X-Content-Type-Options`, and `X-XSS-Protection`.
    - Ensures that critical security measures are in place to mitigate attacks like man-in-the-middle (MITM).

- **Advanced Vulnerabilities Detection**: 
    - Identifies potential **Cross-Site Request Forgery (CSRF)** attacks by checking for missing anti-CSRF tokens in forms.
    - Flags **Directory Traversal** vulnerabilities by detecting unsafe file path manipulations (e.g., `../`).
    - Detects **XSS** and **SQL Injection** risks based on known patterns in the website’s content.

- **Local Environment Detection**: 
    - Automatically detects when the URL points to a local testing environment (e.g., `localhost` or `127.0.0.1`) and skips certain checks that are irrelevant for local setups.

- **Retry Logic**: 
    - Implements retry logic to handle slow or intermittent network issues, ensuring a reliable scanning experience.

## How It Works

**SecuriScan** works by sending HTTP requests to the target website and analyzing the HTML response for known patterns of security vulnerabilities. Here's a breakdown of the scanning process:

1. **Initial Request**: The tool fetches the website's HTML content using Python's `requests` library.
2. **Library Checks**: It scans for common third-party libraries and cross-references them with known vulnerable versions.
3. **Security Header Analysis**: It examines the HTTP response headers for essential security configurations.
4. **Vulnerability Detection**: The tool checks for common attack vectors like XSS, CSRF, SQL Injection, and directory traversal.
5. **Admin Panel Exposure**: It attempts to access common admin panel paths to identify any exposed entry points.
6. **Results**: The scan results are presented in the terminal, detailing any vulnerabilities found and offering recommendations.

## Installation & Requirements

**SecuriScan** requires Python 3.x and the following Python libraries:

- `requests`: For making HTTP requests.
- `beautifulsoup4`: For parsing and navigating HTML content.

### Installing Dependencies

You can easily install the required dependencies by using the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Usage

1. Clone or download the project.
2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python cybersecurity_tool.py
   ```
4. Enter the URL of the website you want to scan when prompted.

### Example:

```bash
Enter the website URL to scan: https://example.com
```

The script will then perform the scan and output results such as detected vulnerabilities, missing security headers, and more.

## Example Usage

Here’s how the scan might look for a vulnerable website:

```bash
Enter the website URL to scan: https://vulnerable-site.com

--- Scan Results ---
Outdated Libraries:
    Vulnerable jQuery version found: 3.5.1 in /assets/js/jquery.min.js

Exposed Admin Panels:
    /admin

Missing Security Headers:
    X-Content-Type-Options
    Strict-Transport-Security

Advanced Vulnerabilities Detected:
    Potential SQL Injection vulnerability detected in https://vulnerable-site.com
    Potential XSS vulnerability detected in https://vulnerable-site.com
```

## Contributing

We welcome contributions to **SecuriScan**! Feel free to fork the repository, submit issues, or create pull requests to improve the functionality of the tool. Here are some areas where contributions are welcome:

- Expanding AI-driven vulnerability detection.
- Adding new types of security checks.
- Improving performance and concurrency for faster scans.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### **SecuriScan**: Your first step towards securing your website and protecting your users from common security risks.
