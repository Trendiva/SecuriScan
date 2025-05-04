
# SecuriScan

![SecuriScan Banner](SecuriScan.png)

**SecuriScan** is an advanced, Python-based cybersecurity tool designed to automate the process of scanning websites for a wide range of security vulnerabilities and misconfigurations. By detecting both common and complex threats, **SecuriScan** empowers web administrators, developers, and security professionals to proactively secure their websites and reduce their attack surface.

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

In today's digital world, website security is more important than ever. **SecuriScan** helps you quickly identify a variety of security vulnerabilities and misconfigurations, such as:

- **Outdated libraries** that might be vulnerable to known exploits.
- **Exposed admin panels** that are prone to brute-force attacks.
- **Missing security headers** that could leave your site susceptible to attacks like MITM (man-in-the-middle).
- **Advanced threats** such as Cross-Site Scripting (XSS), SQL Injection, Cross-Site Request Forgery (CSRF), and more.

This tool provides an automated approach for scanning websites, making it ideal for securing both production environments and local development sites.

## Key Features

**SecuriScan** offers a variety of powerful features for detecting vulnerabilities:

### **Outdated Libraries Detection**  
- Identifies vulnerable versions of third-party libraries (e.g., jQuery, Bootstrap) and flags known security risks.

### **Exposed Admin Panels**  
- Detects exposed admin panel URLs like `/admin`, `/wp-admin`, and `/administrator`, which could be vulnerable to unauthorized access or brute-force attacks.

### **Missing Security Headers**  
- Scans for missing HTTP headers, such as `Strict-Transport-Security`, `X-Content-Type-Options`, and `X-XSS-Protection`, ensuring your site is protected against common attack vectors.

### **Advanced Vulnerabilities Detection**  
- **CSRF**: Detects missing anti-CSRF tokens in forms, potentially leaving your site vulnerable to CSRF attacks.
- **Directory Traversal**: Flags unsafe file path manipulations (e.g., `../`) that can lead to sensitive file exposure.
- **XSS & SQL Injection**: Identifies common attack patterns and flags potential vulnerabilities for further investigation.

### **Local Environment Detection**  
- Automatically skips certain checks when scanning local environments (e.g., `localhost` or `127.0.0.1`), preventing false positives in development setups.

### **Retry Logic**  
- Implements a retry mechanism to handle intermittent network issues, ensuring reliable scans even in unstable environments.

## How It Works

**SecuriScan** uses a straightforward approach to scan websites for security flaws:

1. **Initial Request**: The tool fetches the website's HTML content using Python's `requests` library.
2. **Library Checks**: It scans the HTML for popular third-party libraries and compares them with known vulnerable versions.
3. **Security Header Analysis**: It inspects the HTTP response headers to ensure critical security headers are present.
4. **Vulnerability Detection**: It looks for potential attack vectors, such as XSS, CSRF, SQL Injection, and directory traversal vulnerabilities.
5. **Admin Panel Exposure**: It attempts to access common admin panel URLs to check for exposed entry points.
6. **Results**: The scan results are then displayed in the terminal, highlighting any vulnerabilities or misconfigurations found.

## Installation & Requirements

### Prerequisites

Ensure you have Python 3.x installed on your system. You'll also need the following Python libraries:

- `requests`: For making HTTP requests.
- `beautifulsoup4`: For parsing and navigating HTML content.

### Installing Dependencies

To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

1. Clone or download the **SecuriScan** repository to your local machine.
2. Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

3. Run the tool with the following command:

```bash
python cybersecurity_tool.py
```

4. Enter the URL of the website you want to scan when prompted.

### Example

```bash
Enter the website URL to scan: https://example.com
```

The script will then begin the scan and output results detailing any vulnerabilities or missing security headers.

## Example Usage

Here’s an example of what the scan results might look like for a vulnerable website:

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

We welcome contributions to **SecuriScan**! Whether you're fixing bugs, adding new features, or improving documentation, your help is greatly appreciated. To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a pull request.

### Areas for Contribution:
- Expanding AI-driven vulnerability detection methods.
- Adding new types of security checks.
- Enhancing performance and concurrency to speed up scanning.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### **SecuriScan**: The first step in securing your website and protecting your users from common and advanced security risks.
