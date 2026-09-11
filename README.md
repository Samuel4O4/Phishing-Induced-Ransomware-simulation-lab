# Phishing-Induced Ransomware — SOC Detection & Investigation Lab

![Status](https://img.shields.io/badge/status-completed-brightgreen)
![Environment](https://img.shields.io/badge/environment-home%20lab-blue)
![Stack](https://img.shields.io/badge/stack-Elastic%20%7C%20Wireshark%20%7C%20GoPhish-orange)

> ## ⚠️ **Disclaimer**
> This project was conducted strictly within a controlled home lab environment for educational and defensive security purposes only. All attack simulations were performed on virtual machines owned and managed by the author. No real users, organizations, or production systems were involved.
>
> The techniques demonstrated in this report are intended solely to help SOC analysts, incident responders, and defenders understand attacker behavior in order to improve detection and response capabilities.
>
> **This work must not be used for illegal activities or unauthorized access to systems.**

---

## Table of Contents

- [Overview](#1-overview)
- [Simulation Roles Overview](#2-simulation-roles-overview)
- [Lab Environment & Tools](#3-lab-environment--tools)
- [🔴 Attacker Simulation](#-attacker-simulation)
  - [1. Creating the Ransomware Payload](#1-creating-ransomware-payload)
  - [2. Phishing Scenario](#2-phishing-scenario)
  - [3. Payload Hosting and Delivery](#3-payload-hosting-and-delivery)
  - [4. Payload Execution](#4-payload-execution)
- [🔵 SOC Analyst Investigation](#-soc-analyst-investigation)
  - [1. Initial Security Posture Assessment](#1-initial-security-posture-assessment)
  - [2. Network Traffic Analysis](#2-network-traffic-analysis)
  - [3. Host-Based Investigation](#3-host-based-investigation)
  - [4. MITRE ATT&CK Mapping](#4-mitre-attck-mapping)

---

## 1. Overview

This report documents a **defensive security (SOC) learning exercise** focused on detecting and investigating a simulated phishing-driven ransomware incident using the **Elastic Stack**. The objective is not to develop or deploy malware, but to **understand attacker behavior at a high level** so that effective detection, triage, and response can be performed as a SOC analyst.

The scenario simulates a common real-world threat: a phishing email leading to malicious file execution on a user workstation, followed by ransomware activity. The exercise emphasizes **incident detection, investigation mindset, and response strategy.**

---

## 2. Simulation Roles Overview

### 🔴 Attacker Simulation

The attacker simulation represents a controlled emulation of common threat actor techniques used to understand how real-world attacks manifest in logs and alerts. Its purpose is to generate realistic telemetry that a SOC analyst would be expected to detect and investigate.

**Primary Goals:**
- Creating the ransomware payload
- Simulating a realistic phishing email containing a malicious payload
- Delivering the payload to the victim machine

### 🔵 SOC Analyst Investigation

The SOC analyst investigation represents the **defender's perspective after compromise**. This role focuses on alert validation, investigation, impact assessment, and containment planning using the Elastic Stack. The emphasis is on visibility, correlation, and incident response rather than attack execution.

**Primary Goals:**
- Detect malicious activity using Elastic & Wireshark
- Investigate endpoint behavior and timelines
- Assess impact and prevent further spread
<img width="1774" height="887" alt="Architecture" src="https://github.com/user-attachments/assets/98d51fd4-bb78-4601-aea9-f1ada80db75a" />

## 3. Lab Environment & Tools

### 🧪 Lab Environment

The simulation was conducted using two virtual machines configured in an isolated lab environment:

| Role | Machine |
|------|---------|
| Attacker Machine | Kali Linux |
| Victim Machine | Windows 10 |

### 🛠 Tools Used

| Tool | Purpose |
|------|---------|
| PyInstaller | Converting Python file to executable |
| GoPhish | Phishing campaign simulation |
| Python HTTP Server | Payload hosting |
| Wireshark | Traffic analysis |
| Elasticsearch | Log ingestion and SOC investigation |

---

## 🔴 Attacker Simulation

### 1. Creating Ransomware Payload

A Python script was created to simulate realistic ransomware behavior targeting a predefined directory.

**Payload Development**

The script performed the following actions:
- Targeted a specific folder (`C:\ImportantFiles`)
- Deleted shadow copies
- Identified files based on selected extensions (`.txt`, `.docx`, `.pdf`, `.jpg`, `.png`)
- Generated a unique symmetric encryption key using the `Fernet` algorithm
- Encrypted the contents of targeted files
- Renamed encrypted files by appending the `.encrypted` extension
- Displayed a graphical ransom notification

**Conversion to Executable Format**

The Python ransomware script was converted into a standalone Windows executable (`.exe`) using **Auto Py to Exe (PyInstaller)** to enable execution without requiring a Python interpreter.

To simulate realistic attacker tradecraft:
- The executable was renamed to resemble a legitimate financial transaction report.
- A PDF-style icon was assigned to increase credibility.

This approach demonstrates how adversaries combine payload packaging with social engineering techniques to increase the likelihood of user execution.

<img width="1718" height="878" alt="Python to EXE " src="https://github.com/user-attachments/assets/b73926cc-92de-4c22-9bba-6f8340b94693" />

---

### 2. Phishing Scenario

A phishing email was simulated to impersonate a financial institution (**Apex Bank**) and sent to a fictional employee (**Bob Smith – HR Department**). The email content socially engineered the victim into downloading what appeared to be a legitimate financial report.

**Phishing Infrastructure and Campaign Setup**

GoPhish was used as the phishing framework. The configuration followed a standard workflow to mirror how phishing campaigns are commonly executed.

- **Sending Profile Configuration** — A sending profile was configured to define the email delivery parameters (sender name, email address, and SMTP configuration). This step establishes how the phishing email appears to the recipient and is critical for generating realistic email telemetry.
- **Email Template Creation** — An email template was created to reflect a legitimate bank communication. The content referenced a yearly transaction report and included a download prompt designed to encourage user interaction.
- **Landing Page Configuration (Not Used)** — A landing page was created as part of the standard GoPhish workflow; however, it was not used in this scenario, as the objective was direct file download rather than credential harvesting.
- **Users and Groups Setup** — The target user (Bob Smith) was added under Users & Groups. This represents a typical enterprise user account within the HR department and allows campaign tracking at the individual level.
- **Campaign Launch** — After completing the configuration, a phishing campaign was created and launched. This action initiated email delivery to the target user and marked the start of the simulated attack timeline.

---

### 3. Payload Hosting and Delivery

To host the simulated malicious file, a lightweight Python HTTP server was activated on the attacker simulation machine. The file download URL was embedded directly into the phishing email body.

Once the URL was embedded and validated, the phishing campaign was sent successfully.

When the recipient clicked the download link, the file was retrieved from the hosted server, emulating a common real-world phishing delivery mechanism where payloads are hosted externally.

<img width="1862" height="905" alt="Phishing Mail" src="https://github.com/user-attachments/assets/72fbaed4-ff03-407e-afac-a0edf35fa6d2" />

---

### 4. Payload Execution

The victim downloads the file, believing it to be a legitimate bank transaction report.

Upon execution, the disguised executable runs the ransomware payload, resulting in immediate file encryption, deletion of the shadow copies, and presentation of the ransom notification.

<img width="1718" height="878" alt="Ransomware" src="https://github.com/user-attachments/assets/1a804ee5-8e3b-427a-aa65-31fbe07d613d" />
<img width="3436" height="808" alt="files" src="https://github.com/user-attachments/assets/698e01e8-bd02-40db-ba2e-40f33cdd414f" />

---

## 🔵 SOC Analyst Investigation

### 1. Initial Security Posture Assessment

Before beginning technical analysis, an assessment of the victim's security posture was conducted.

The investigation revealed significant user-side weaknesses:
- Windows Defender was manually disabled.
- The Windows Firewall was turned off.
- The victim relied solely on file icon and visible extension to determine file legitimacy.
- File extensions were hidden, causing a malicious executable (`.exe`) to appear as a benign PDF document.

This lack of basic security awareness directly enabled the successful execution of the malicious payload.

---

### 2. Network Traffic Analysis

As an initial investigation step, network traffic was analyzed using **Wireshark** to identify suspicious activity related to the phishing campaign.

**Findings**
- Identified outbound HTTP traffic from the victim machine to an external host.
- Observed a file download request initiated shortly after the phishing email interaction.
- HTTP GET request indicated retrieval of an executable file disguised as a transaction report.

**Conclusion**

Network evidence confirms successful delivery and download of the malicious file following phishing email engagement.

---

### 3. Host-Based Investigation

Following network confirmation, host-level investigation was conducted using **Elasticsearch**.

- During log review, Event IDs **4656** (Handle Requested), **4658** (Handle Closed), and **4663** (Attempt to Access an Object) were observed in high frequency against multiple user files within a short time window.

This pattern is consistent with ransomware behavior, where files are opened, modified, and rewritten during encryption.

- More importantly, an alert was triggered by a custom detection rule previously developed in the author's Detection Engineering Lab.
  > See related work: [Elastic Detection Engineering](https://app.notion.com/p/Elastic-Detection-Engineering-2dad295dbf4380c18b18f9a8951112db?pvs=21)
- The rule is designed to detect attempts to delete **Volume Shadow Copies**, a common ransomware technique used to inhibit recovery.

The alert fired immediately after execution of the malicious payload, confirming shadow copy manipulation behavior.

---

### 4. MITRE ATT&CK Mapping

To standardize the analysis and align the incident with industry frameworks, the observed behaviors were mapped using the **MITRE ATT&CK Framework**.

---

## 🎯 Key Takeaways

- Disabled endpoint protections (Defender, Firewall) combined with hidden file extensions significantly lowered the barrier for successful phishing-based compromise.
- Network-layer visibility (Wireshark) and host-layer visibility (Elastic/Windows Event Logs) together provided full-chain evidence of the attack, from delivery to impact.
- Custom detection engineering — specifically a rule targeting Volume Shadow Copy deletion — enabled near-immediate alerting on ransomware behavior.
- Mapping the incident to MITRE ATT&CK helps standardize reporting and supports building future detections around the same tactics and techniques.
