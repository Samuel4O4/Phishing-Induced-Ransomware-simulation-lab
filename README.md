# Phishing-Induced Ransomware Attack & Detection Lab

![Cybersecurity](https://img.shields.io/badge/Focus-SOC%20%7C%20Detection%20%7C%20Incident%20Response-blue)
![Environment](https://img.shields.io/badge/Environment-Isolated%20Lab-green)
![SIEM](https://img.shields.io/badge/SIEM-Elastic%20Stack-orange)
![Network Analysis](https://img.shields.io/badge/Network-Wireshark-blue)

## ⚠️ Disclaimer

This project was conducted strictly within a controlled home laboratory environment for educational and defensive security purposes only.

All attack simulations were performed against virtual machines owned and managed by the author. No real users, organizations, or production systems were involved.

The techniques demonstrated in this project are intended to help SOC analysts, incident responders, and defenders understand attacker behavior and improve detection and response capabilities.

This work must not be used for illegal activities or unauthorized access to systems.

---

## 📌 Project Overview

This project demonstrates the **detection and investigation of a simulated phishing-driven ransomware incident** from a SOC analyst perspective.

The scenario represents a realistic attack chain in which a phishing email delivers a malicious executable to a victim workstation. After execution, the simulated ransomware performs destructive file operations, including file encryption and attempts to remove Volume Shadow Copies.

The primary focus of this project is **defensive security**:

* Understanding attacker behavior
* Identifying relevant security telemetry
* Analyzing network traffic
* Investigating endpoint activity
* Developing and validating detection logic
* Mapping observed behavior to MITRE ATT&CK
* Performing incident response and containment

---

## 🎯 Objectives

The main objectives of this lab were to:

* Simulate a realistic phishing-based initial access scenario
* Generate endpoint and network telemetry from ransomware activity
* Analyze malicious network traffic using Wireshark
* Investigate Windows security events using Elastic
* Detect ransomware-related behavior using a custom detection rule
* Identify attempts to delete Volume Shadow Copies
* Build an incident timeline
* Map observed behavior to MITRE ATT&CK
* Practice SOC investigation and incident-response methodology

---

## 🏗️ Lab Architecture

The lab was built using isolated virtual machines.

```text
                         ┌──────────────────────┐
                         │    Attacker VM       │
                         │      Kali Linux      │
                         │                      │
                         │  GoPhish             │
                         │  Python HTTP Server  │
                         └──────────┬───────────┘
                                    │
                         Phishing / HTTP Download
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     Victim VM        │
                         │     Windows 10       │
                         │                      │
                         │  Malicious Payload   │
                         │  File Encryption     │
                         └──────────┬───────────┘
                                    │
                          Security Telemetry
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Elastic Stack     │
                         │                      │
                         │  Detection           │
                         │  Investigation       │
                         │  Event Analysis      │
                         └──────────────────────┘

                         ┌──────────────────────┐
                         │      Wireshark       │
                         │  Network Analysis    │
                         └──────────────────────┘
```

---

## 🧪 Environment & Tools

### Virtual Machines

| Component            | Platform      |
| -------------------- | ------------- |
| Attacker Simulation  | Kali Linux    |
| Victim Workstation   | Windows 10    |
| SIEM / Investigation | Elastic Stack |

### Tools

* **GoPhish** — Phishing campaign simulation
* **Python** — Controlled ransomware behavior simulation
* **PyInstaller / Auto PY to EXE** — Executable packaging
* **Python HTTP Server** — Payload hosting
* **Wireshark** — Network traffic analysis
* **Elasticsearch / Elastic Stack** — Security log analysis and detection
* **MITRE ATT&CK** — Adversary behavior mapping

---

# 🔴 Attack Simulation

## 1. Ransomware Payload Simulation

A controlled Python-based ransomware simulation was created to generate realistic endpoint telemetry.

The simulation targeted a predefined laboratory directory:

```text
C:\ImportantFiles
```

The simulated behavior included:

* Identifying selected file types
* Generating a unique symmetric encryption key
* Encrypting files using the Fernet algorithm
* Renaming encrypted files
* Attempting to remove Volume Shadow Copies
* Displaying a simulated ransom notification

The payload was packaged as a Windows executable for the purpose of reproducing a realistic execution scenario inside the isolated lab.

> **Note:** The repository focuses on the defensive investigation and telemetry generated by the simulation rather than providing deployable ransomware.

---

## 2. Phishing Simulation

A phishing campaign was created using **GoPhish**.

The scenario simulated a financial institution sending a transaction-report email to a fictional HR employee.

### Attack Flow

```text
Phishing Email
      ↓
User Interaction
      ↓
Malicious File Download
      ↓
Payload Execution
      ↓
Ransomware Activity
```

The phishing email was designed to demonstrate how social engineering can be combined with malicious file delivery.

The landing page functionality was not used because the objective was **malicious file delivery rather than credential harvesting**.

---

## 3. Payload Delivery

A lightweight Python HTTP server was used to host the simulated malicious executable.

The download link was embedded within the phishing email.

After the victim interacted with the email, the Windows workstation generated HTTP traffic associated with the file download.

This created network telemetry that could subsequently be investigated using Wireshark.

---

## 4. Payload Execution

The victim executed the downloaded executable believing it to be a legitimate financial document.

The simulated ransomware then generated observable behavior including:

```text
Executable Execution
       ↓
File Enumeration
       ↓
File Access
       ↓
File Encryption
       ↓
File Renaming
       ↓
Shadow Copy Deletion Attempt
```

---

# 🔵 SOC Investigation

## 1. Security Posture Assessment

Before investigating the attack, the victim workstation's security posture was assessed.

The laboratory configuration contained several weaknesses:

* Windows Defender was disabled
* Windows Firewall was disabled
* File extensions were hidden
* The user relied heavily on the displayed file icon to determine file legitimacy

This configuration helped demonstrate how basic security controls and user awareness can influence the success of phishing-based attacks.

---

## 2. Network Traffic Analysis

Wireshark was used to investigate network activity surrounding the phishing event.

### Findings

The investigation identified:

* Outbound HTTP communication from the victim workstation
* A file download shortly after the phishing interaction
* An HTTP `GET` request associated with retrieval of the executable
* Communication between the victim workstation and the attacker simulation host

### Investigation Flow

```text
Phishing Interaction
        ↓
HTTP Connection
        ↓
HTTP GET Request
        ↓
Executable Download
        ↓
Local Execution
```

### Conclusion

The network evidence established a relationship between the phishing interaction and the subsequent malicious file download.

---

# 🔎 3. Host-Based Investigation

Following the network investigation, endpoint telemetry was analyzed using Elastic.

Several Windows Security Event IDs were observed at high frequency within a short period:

| Event ID | Description                             |
| -------- | --------------------------------------- |
| 4656     | A handle to an object was requested     |
| 4658     | The handle to an object was closed      |
| 4663     | An attempt was made to access an object |

The events showed repeated access to multiple files within the victim directory.

A high volume of file-access activity occurring within a short time window is an important behavioral indicator when investigating potential ransomware activity.

### Observed Pattern

```text
File Access
    ↓
File Modification
    ↓
Repeated Activity
    ↓
Multiple Files
    ↓
Short Time Window
```

This behavior provided additional evidence supporting the ransomware hypothesis.

---

# 🚨 4. Detection Engineering

A custom Elastic detection rule was used to identify attempts to delete **Volume Shadow Copies**.

Volume Shadow Copies can provide a mechanism for recovering previous versions of files. Attackers may attempt to remove them during ransomware attacks to make recovery more difficult.

The detection rule generated an alert shortly after execution of the simulated malicious payload.

### Detection Flow

```text
Malicious Execution
        ↓
Shadow Copy Deletion Attempt
        ↓
Windows Telemetry
        ↓
Elastic Detection Rule
        ↓
SOC Alert
        ↓
Investigation
```

This demonstrated the value of combining **behavior-based detection** with endpoint telemetry rather than relying exclusively on file signatures.

---

# 🧭 5. Incident Timeline

The simulated incident can be summarized as follows:

```text
1. Phishing Email Sent
          ↓
2. Victim Receives Email
          ↓
3. Victim Opens Email
          ↓
4. Malicious File Downloaded
          ↓
5. Malicious Executable Executed
          ↓
6. Ransomware Behavior Begins
          ↓
7. Shadow Copy Deletion Attempt
          ↓
8. Multiple Files Accessed
          ↓
9. Files Encrypted
          ↓
10. Elastic Detection Triggered
          ↓
11. SOC Investigation Begins
          ↓
12. Containment & Recovery
```

---

# 🛡️ 6. Incident Response

The investigation follows a standard incident-response approach.

### Identification

* Validate the security alert
* Identify the affected workstation
* Review process and file activity
* Analyze network connections
* Determine whether ransomware behavior occurred

### Containment

Potential containment actions include:

* Isolating the affected workstation from the network
* Blocking malicious network communication
* Preventing further execution of the payload
* Identifying other potentially affected systems

### Eradication

* Remove the malicious payload
* Identify and remove persistence mechanisms if present
* Restore security controls
* Verify that malicious processes are no longer running

### Recovery

* Restore affected files from clean backups
* Validate system integrity
* Re-enable endpoint security controls
* Monitor the workstation for recurring suspicious activity

### Lessons Learned

The incident demonstrates the importance of:

* Email security controls
* Endpoint protection
* Network monitoring
* File-extension visibility
* User security awareness
* Centralized logging
* Behavioral detection
* Reliable offline backups
* Rapid endpoint isolation

---

# 🧩 7. MITRE ATT&CK Mapping

The observed behaviors were mapped to the **MITRE ATT&CK Framework** to provide a standardized representation of the simulated attack chain.

| Attack Stage     | Observed Behavior              | MITRE ATT&CK      |
| ---------------- | ------------------------------ | ----------------- |
| Initial Access   | Phishing email                 | T1566             |
| Execution        | Malicious executable execution | T1204 / T1204.002 |
| Impact           | File encryption                | T1486             |
| Inhibit Recovery | Shadow Copy deletion           | T1490             |

> The mapping represents the behavior observed within this specific laboratory simulation.

---

# 📊 Detection & Investigation Highlights

This project demonstrates several practical SOC capabilities:

### Network Analysis

* HTTP traffic analysis
* File download investigation
* Identification of suspicious network activity
* Packet-level investigation using Wireshark

### Endpoint Investigation

* Windows Security Event analysis
* File-access activity investigation
* Behavioral analysis
* Timeline reconstruction

### Detection Engineering

* Custom Elastic detection rule
* Ransomware behavior detection
* Shadow Copy deletion detection
* Alert validation

### Incident Response

* Alert triage
* Incident investigation
* Impact assessment
* Containment planning
* Recovery strategy

---

# 📁 Repository Structure

```text
phishing-ransomware-soc-lab/
│
├── README.md
│
├── attack-simulation/
│   ├── phishing/
│   ├── payload/
│   └── delivery/
│
├── detection/
│   ├── elastic/
│   └── wireshark/
│
├── investigation/
│   ├── timeline.md
│   ├── network-analysis.md
│   └── host-analysis.md
│
├── incident-response/
│   ├── containment.md
│   ├── eradication.md
│   └── recovery.md
│
├── mitre/
│   └── attack-mapping.md
│
├── architecture/
│   └── lab-architecture.png
│
└── screenshots/
```

---

# 🎓 Key Takeaways

This lab provided hands-on experience with a complete simulated attack-and-defense lifecycle:

```text
Attack Simulation
       ↓
Telemetry Generation
       ↓
Detection
       ↓
Investigation
       ↓
Threat Identification
       ↓
Incident Response
       ↓
Recovery
```

The most important lesson from the project was that effective SOC operations require understanding **both attacker behavior and defender visibility**.

Rather than simply identifying that ransomware occurred, the investigation focused on answering:

* **How did the attack begin?**
* **What did the attacker execute?**
* **What evidence was generated?**
* **What happened on the endpoint?**
* **What network activity occurred?**
* **How could the behavior be detected?**
* **What actions should a SOC analyst take?**

---

## 🚀 Future Improvements

Potential extensions to this lab include:

* Integrating Sysmon for richer endpoint telemetry
* Building additional Elastic detection rules
* Creating automated alert enrichment
* Integrating threat intelligence
* Adding automated incident-response workflows
* Implementing SOAR automation using **n8n**
* Simulating lateral movement in a controlled environment
* Adding additional ransomware detection techniques
* Creating automated IOC extraction and reporting

---

## 👨‍💻 Author

**Samuel Adham**

Cybersecurity Enthusiast | SOC Analyst | Detection & Incident Response

This project was created as part of a hands-on cybersecurity learning journey focused on understanding attacker behavior and developing practical defensive security skills.
