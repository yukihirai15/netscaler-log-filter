# 🧠 NetScaler Log Filter v2.0
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

A Python-based automation script to extract and filter key events from **NetScaler logs**.  
Built for TAC engineers to quickly identify SSL, STA, and authentication-related issues.

---

## 🚀 Features
✅ Keyword or Regex-based search  
✅ Time-based log filtering (`--since`, `--until`)  
✅ Exclude specific keywords (`--exclude`)  
✅ Works with both single files and full directories  
✅ Generates clean, timestamped reports  
✅ Simple command-line interface  

---

## 📂 Project Structure
netscaler-log-filter/
│
├── nslog_filter_v2.py # Main script
├── requirements.txt # Dependencies
├── commands.txt # Example usage commands
├── sample/ns.log # Example NetScaler log
└── output/filtered_logs.txt # Sample output


## 🧰 Requirements

Python 3.8 or higher

Modules: argparse, datetime, re, os


(Optional) tqdm and colorama for UI enhancements

---

## 📖 Usage

### Basic keyword search
python nslog_filter.py --path .\ns.log --keywords "SSL"

### Search multiple keywords
python nslog_filter.py --path .\ns.log --keywords "SSL,error"

### Regex search
python nslog_filter.py --path .\ns.log --keywords "SSL.*failed" --regex

### Exclude noisy keywords
python nslog_filter.py --path .\ns.log --keywords "SSL,error" --exclude "DEBUG,INFO"

### Time-range filtering
python nslog_filter.py --path .\ns.log --keywords "SSL,error" --since "Oct 28 10:00:00" --until "Oct 28 18:00:00"

### Combined: regex + exclusion + time filter + custom output
python nslog_filter.py --path .\ns.log --keywords "SSL.*failed|cert.*error" --regex --exclude "DEBUG" --since "Oct 28 00:00:00" --until "Oct 29 00:00:00" --output filtered_ssl_errors.txt

See `commands.txt` for the full command reference, including supported keywords (SSL, AUTH, LDAP, RADIUS, SAML, GSLB, AAA, and more).
