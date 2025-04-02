Industry: Water & Waste Water
Sector: N/A
Threat Type: Advanced Persistent Threat (APT) with ICS sabotage intent
Attack Type: Targeted disruption of water treatment and distribution systems (non-ransomware)
Impact: Possible sabotage of water quality, system shutdowns, and public health concerns
Financial Impact: Ranges from $500K for minor disruptions over a few hours, to $3M+ for extended outages and cleanup over multiple days, including regulatory fines and reputation damage

⸻

1. Scenario Title

Covert Flow: Targeted Disruption of Critical Water Supply

⸻

2. Description

This tabletop exercise places participants in the midst of a sophisticated cyber-attack targeting a municipal water and wastewater utility. The adversary’s goal is to infiltrate the business network, pivot into the industrial environment (ICS), and manipulate PLCs/RTUs responsible for water treatment and distribution processes.

Participants will walk through detecting early-stage compromises, containing lateral movement, and mitigating potential sabotage of the water filtration and pumping systems. This includes challenges in cross-segment traffic (Level 4 to Levels 3.5/3/2/1) and complexities of ICS networks.

⸻

3. Threat

a. Backstory

A highly motivated adversary—suspected to have nation-state resources—has been gathering intelligence on North American water utilities for months. Multiple water-related utilities across the region have reported increased phishing attempts and suspicious scanning of their external IP ranges. This particular water utility has been quietly singled out by the adversary for a more direct attack.

b. Industry/Technology Focus

The attacker is targeting ICS infrastructure used in water treatment (chlorination) and distribution systems. Key ICS components include:
	•	SCADA Servers (ICS-SCADA-01) for monitoring and controlling pumps, valves, and chemical dosing
	•	PLCs (ICS-PLC-01, ICS-PLC-02) and RTUs (ICS-RTU-01) that control the water flow, disinfection, and remote telemetry
	•	Sensors (flow, pressure, level) and actuators used for real-time monitoring and adjustments

c. Motivation
	•	Potential sabotage of local water service to undermine public trust and cause operational and financial damage.
	•	Possible alignment with hacktivist or nation-state goals (disruption of critical infrastructure, demonstration of power, or exertion of geopolitical pressure).

d. Preferred Attacks, Technology, and Exploits

The adversary relies on a combination of phishing, exploiting known vulnerabilities on perimeter devices, and leveraging weak remote access configurations. They have a working knowledge of ICS protocols like Modbus (TCP/502) and CIP/ENIP (TCP/44818) and know how to reprogram or manipulate PLC logic.

⸻

4. Scenario

a. Attacker Objectives
	1.	Gain initial foothold in enterprise network and establish persistence.
	2.	Pivot into ICS environment (Levels 3.5 -> 3 -> 2 -> 1).
	3.	Tamper with PLCs controlling water pumps (ICS-PLC-01) and the disinfection/chlorination system (ICS-PLC-02).
	4.	Disrupt water treatment processes (potentially leading to unsafe water release or service outage).
	5.	Evade detection long enough to cause measurable damage.

b. Initial Attack Vector

The likely initial compromise occurs via phishing targeting employees in the enterprise network, specifically those who occasionally work with ICS engineering staff. An email containing a malicious document is opened by Win10-Office02 (192.168.100.22), resulting in remote code execution. The attacker then enumerates network shares, user credentials, and sets up persistence on the file server FS01 (192.168.100.11).

c. Suggested MITRE ATT&CK TTP Chain

Below is a condensed attack flow referencing MITRE ATT&CK for ICS tactic/technique IDs (examples provided; there are many relevant variations you might map more precisely):
	1.	Reconnaissance & Resource Development
	•	T0868 – Spearphishing: Gathering employee emails, organizational info.
	•	T0802 – Network Information Gathering: Adversary identifies ICS IP ranges, firewall rules, etc.
	2.	Initial Access
	•	T0833 – Engineering Workstation Compromise or T0809 – Exploit Public-Facing Application: In our scenario, the path is via phishing on the business network, then pivot to ICS.
	3.	Execution
	•	T0889 – Execution through API or T0807 – Program Download: Attacker uses malicious scripts on the enterprise workstation.
	4.	Persistence
	•	T0862 – Valid Accounts or T0813 – Remote Access Software: Adversary drops a backdoor or reuses legitimate credentials on FS01 or DC01.
	5.	Privilege Escalation
	•	T0811 – Exploit Application Vulnerability: After pivot, attacker escalates to domain admin or ICS admin privileges.
	6.	Lateral Movement
	•	T0882 – Remote Services: SSH/RDP into ICS-EngStation-02, then into ICS-SCADA-01.
	7.	Collection
	•	T0816 – Network Sniffing or T0883 – Data from Information Repositories: The adversary inspects traffic to/from ICS devices (Modbus/TCP 502, CIP 44818).
	8.	Command & Control
	•	T0886 – Standard Application Layer Protocol: The attacker uses HTTP/HTTPS or a known proxy to blend in with normal traffic in the DMZ.
	9.	Inhibit Response Function (Destructive ICS Impact)
	•	T0836 – Modify Control Logic: The attacker alters PLC logic to mismanage water flow or chemical dosing.
	•	T0806 – Modify ICS Environment: The adversary modifies set points in ICS-SCADA-01.
	10.	Impact

	•	T0804 – Damage to Property: Over-chlorination or shutting down pumps leading to water service outages or unsafe water release.

d. Additional Notes, Caveats, Details
	•	The water utility’s network segmentation is fairly standard, but remote management paths from enterprise to ICS (via DMZ) provide potential pivot points.
	•	Monitoring must exist on ICS-FW-01 and ICS-FW-02 for inbound remote access or suspicious traffic (i.e., unauthorized protocols).
	•	ICS domain controller (ICS-AD-01) and engineering workstations are prime targets for lateral movement—especially ICS-EngStation-01 (192.168.210.10), which can push new logic to PLCs.
	•	Attackers may attempt to hide malicious ladder logic updates as “routine maintenance” or “patches.”

⸻

5. Recommended Injects

Below are possible injects to include during the tabletop exercise to spur decision-making and cross-functional collaboration:
	1.	Phishing Email Discovery
	•	IT Security is alerted by an employee that a suspicious email was received. The email subject references “Quarterly ICS Security Guidance.” Another user reports opening the attachment on Win10-Office02.
	2.	Endpoint AV Alert
	•	The endpoint security solution flags a suspicious PowerShell script running on Win10-Office02 with a detected but unblocked behavior.
	3.	Unusual Traffic on FS01
	•	The SIEM triggers an alert about repeated failed login attempts to FS01 (192.168.100.11), followed by a successful login from a newly created user account.
	4.	Network Mapping
	•	NetFlow analysis from Router-01 (192.168.100.2) shows unusual port scans targeting ICS-FW-01 (192.168.210.1).
	5.	ICS-FW-01 Policy Change
	•	A newly added firewall rule on ICS-FW-01 permits inbound TCP/3389 from the DMZ-WSUS-01 server. This was not part of any authorized change request.
	6.	Unauthorized RDP to ICS-EngStation-02
	•	ICS administrators see an RDP session established at 2 AM local time from an external IP to ICS-EngStation-02 (via the DMZ VPN?). The session remains active for 30 minutes.
	7.	PLC Alarm
	•	ICS-SCADA-01 logs show repeated “PLC Communications Fault” with ICS-PLC-01. The alarm resets quickly but repeats every hour.
	8.	Water Quality Deviation
	•	Operators receive sensor readings indicating elevated chlorine levels. ICS-HMI-01 (192.168.220.11) flags the system moving beyond normal set points.
	9.	Public Inquiry
	•	The customer call center starts getting calls about water with an unusual taste/odor. Some local news inquiries begin to come in.
	10.	Regulatory Pressure

	•	The state environmental regulator requests an immediate security posture and risk assessment following rumors of a breach at the utility.
