# File Server & Upload Vulnerability Auditor

A lightweight Python command-line tool designed to audit file servers for exposed sensitive configuration files (like `.env`, `config.json`) and test upload endpoints for security flaws.

## Features
- **Argument Parsing:** Uses Python's `argparse` for clean, professional CLI usage.
- **Information Disclosure Check:** Automatically scans target URLs for high-risk files left exposed in public directories.
- **Upload Security Testing:** Tests file-upload paths against arbitrary file handling risks.
- **Automated Reporting:** Exports scan results into a structured `audit_report.json` file.

## Tech Stack
- **Language:** Python 3
- **Libraries:** `requests`, `argparse`, `json`

## How to Run
1. Install dependencies:
   ```bash
   pip install requests