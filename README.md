# 🛡️ File Integrity Monitor (FIM)

## 📖 Overview
A lightweight, Python-based File Integrity Monitor designed to detect unauthorized modifications to critical files. This tool mimics the core functionality of enterprise Security Operations Center (SOC) solutions like Wazuh or Tripwire by calculating and comparing SHA-256 hashes against a secure JSON baseline. 

## 🚀 Features
* **Baseline Creation:** Generates secure SHA-256 cryptographic hashes of target files and stores them in a structured JSON database (`baseline.json`).
* **Continuous Monitoring:** Scans the established baseline and instantly alerts on three core events:
  * ✅ **SAFE:** The file is unchanged.
  * ⚠️ **CHANGED:** The file's hash has been altered (potential tampering, unauthorized access, or malware activity).
  * 🚨 **DELETED:** The file has been removed from the system.
* **Error Handling:** Built-in programmatic safeguards to handle corrupted files and parse complex file paths seamlessly.

## 🛠️ Tech Stack & Skills Demonstrated
* **Language:** Python 3.x
* **Core Libraries:** `hashlib`, `json`, `os`
* **Security Concepts:** Cryptographic Hashing, Data Serialization, SOC Alerting Logic, Threat Detection

## 💻 Usage
1. Clone the repository:
   ```bash
   git clone [https://github.com/osohail2006/File-Integrity-Monitor.git](https://github.com/osohail2006/File-Integrity-Monitor.git)
   cd File-Integrity-Monitor
