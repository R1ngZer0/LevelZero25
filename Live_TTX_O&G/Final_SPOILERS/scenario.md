Industry: Oil & Gas
Sector: Midstream and Downstream (Refinery + Dispersed Pipelines)
Environment: (Based on the attached network.md – includes segmented corporate network, ICS/OT network, DMZ, remote monitoring stations for pipelines, etc.)
Threat Type: State-Sponsored or Highly Sophisticated APT (not ransomware)
Attack Type: Industrial Network Disruption/Sabotage
Impact: Disruption to refining process flow, pipeline shutdown, safety concerns, and environmental implications. Operational downtime of 4–14 days could lead to major production losses and potential safety liabilities.
Financial Impact:
	•	Short (1-2 days): Up to $5 million (lost production, recovery costs)
	•	Medium (3-7 days): Up to $15 million (further damages, contract penalties, prolonged downtime)
	•	Long (8+ days): $30+ million (severe reputational harm, large-scale environmental liabilities, regulatory scrutiny)

⸻

Scenario Title

“Covert Hydrocarbon Interference”

⸻

Description

This tabletop exercise focuses on a sophisticated threat actor targeting the midstream and downstream operations of an oil & gas company. The attacker has identified critical gaps within corporate-IT to ICS/OT network segmentation and aims to sabotage fuel supply. In this scenario, they exploit a third-party vendor management system, pivot into the corporate network, and eventually manipulate critical ICS controllers tied to pipeline flow and refinery processes.

Participants will practice incident response (IR) procedures, assess corporate-to-OT network segmentation, ensure operational continuity, communicate effectively with stakeholders, and coordinate with external partners such as local law enforcement, industry peers, and regulators.

⸻

Threat

Backstory

An advanced persistent threat group, previously linked to attacks against critical infrastructure in other regions, has turned its sights on the organization. Over the last few months, threat intelligence sources have observed reconnaissance activities against oil & gas companies worldwide. The group’s hallmark is stealthy infiltration and sabotage of equipment that can cause either partial or complete disruption without drawing immediate attention.

Industry/Technology Focus
	•	Midstream: Pipeline SCADA systems, networked PLCs, pressure and flow controllers, remote terminal units (RTUs), and system management for distribution.
	•	Downstream: Refinery ICS/OT environment including control loops for hydrocarbon processing, blending, and refining.
	•	Corporate IT: ERP, HR, email, vendor management portals, data analytics platforms, and remote access solutions.

Motivation
	•	Geopolitical Leverage: Disruption to oil & gas operations can impact local fuel supply chains, potentially increasing energy prices and creating leverage for nation-state or criminal negotiations.
	•	Intellectual Property Theft: Secondary motive to exfiltrate proprietary refinery process data to assist the threat actor’s domestic energy development.
	•	Sabotage/Disruption: A primary end goal is to cause physical and economic harm, damaging critical infrastructure and the organization’s reputation.

Preferred Attacks, Technology, and Exploits
	•	Spearphishing & Social Engineering: Precise targeting of vendors and key personnel.
	•	Exploitation of Public-Facing Applications (MITRE ATT&CK ID: T1190): Targeting vulnerable vendor portal or corporate web applications.
	•	Valid Accounts (MITRE ATT&CK ID: T1078): Leveraging stolen credentials to gain privileged access.
	•	Abuse of Remote Services (MITRE ATT&CK ID: T1133): Exploiting misconfigured RDP/VPN/SSH paths between corporate and OT environments.
	•	Command and Scripting Interpreter (MITRE ATT&CK ID: T1059): Using PowerShell or custom malware implants to maintain stealth.
	•	Execution of Malicious ICS Payloads: Targeting PLC logic, SCADA configurations, or historian manipulation to disrupt physical processes.

⸻

Scenario

Attacker Objectives
	1.	Stealthy Entry: Establish initial foothold inside the corporate network, gather intel on ICS environment, collect valid credentials, and move laterally.
	2.	Pivot to ICS: Access the refinery’s control system and pipeline SCADA network, manipulate critical flow and pressure setpoints, potentially causing safety system triggers or forced shutdown.
	3.	Disruption of Operations: Sabotage refining processes (e.g., catalytic cracking units, distillation columns) and force pipeline operational shutdowns, causing massive revenue loss and supply chain disruption.
	4.	Cover Tracks: Deploy “cleanup” scripts and obscure logs to complicate investigation and forensics.

Initial Attack Vector
	•	Compromised Vendor Portal: The threat actor exploits an unpatched vulnerability (CVE is plausible, but not specified in the exercise) in the third-party vendor management system used for contract and maintenance work. This application is internet-facing and used by legitimate vendors to schedule on-site pipeline inspections and refinery maintenance tasks.
	•	Credential Harvesting: After gaining initial access, the attacker harvests valid accounts from the vendor portal database, including those belonging to internal employees who have single sign-on privileges.

Suggested Mitre ATT&CK TTP Chain

Below is a high-level chain referencing Enterprise-focused Tactics, though in reality, ICS-specific Tactics (from ATT&CK for ICS) may overlap:
	1.	Reconnaissance
	•	T1592: Gather Victim Host Information (Scanning publicly available IT/OT infrastructure details)
	•	T1598: Phishing for Information (targeting employees/vendors)
	2.	Resource Development
	•	T1587.001: Develop Capabilities: Malware (custom RAT or ICS-tailored malware)
	3.	Initial Access
	•	T1190: Exploit Public-Facing Application (Vendor management portal)
	•	T1078: Valid Accounts (stolen vendor credentials)
	4.	Execution
	•	T1059: Command and Scripting Interpreter (PowerShell, Python, or custom ICS-specific payloads)
	5.	Persistence
	•	T1547: Boot or Logon Autostart Execution (Registry run keys, scheduled tasks in the IT environment)
	6.	Privilege Escalation
	•	T1068: Exploitation for Privilege Escalation (using known OS kernel or local service vulnerabilities)
	7.	Defense Evasion
	•	T1070: Indicator Removal on Host (clearing logs to hide ICS manipulations)
	8.	Credential Access
	•	T1003: OS Credential Dumping (harvesting domain admin or ICS engineer credentials)
	9.	Discovery
	•	T1046: Network Service Scanning (mapping ICS devices, PLCs, and SCADA servers)
	10.	Lateral Movement
	•	T1021: Remote Services (RDP/SSH to pivot between IT and OT segments)
	11.	Collection
	•	T1119: Automated Collection (scripts to gather ICS configs, PLC logic files)
	12.	Command and Control
	•	T1095: Non-Application Layer Protocol (custom ICS protocol tunnels or encryption to hide traffic)
	13.	Inhibit Response Function (ICS disruption)
	•	T831 (ICS-specific example – manipulate protective control parameters, e.g., turning off safety checks)
	14.	Impact
	•	T1489: Service Stop (stopping ICS data historian or SCADA services)
	•	T1496: Resource Hijacking (overloading ICS CPU resources, forcibly shutting down pipeline pumps)

Additional Notes, Caveats, Details
	•	Safety Instrumented Systems (SIS): If the attacker manipulates setpoints that cause frequent SIS trips or spurious shutdown, critical processes may go offline.
	•	Regulatory Compliance: Potential compliance ramifications with agencies overseeing pipeline safety and environmental regulations.
	•	Supply Chain Partners: Refining and distribution partners may also be affected if pipeline flow is halted, leading to possible legal claims.
	•	Data vs. Control Manipulation: Attackers may conduct false data injection to hide sabotage attempts from monitoring operators, further delaying detection.

⸻

Recommended Injects
	1.	Unusual Vendor Login Alert
	•	Timestamped logs indicate a vendor user account accessing the portal from a foreign IP address at 3:00 AM local time.
	•	The session triggers a high-volume data download from the portal, specifically ICS site schematics.
	2.	Suspicious IT Ticket
	•	Help Desk receives multiple complaints from employees about forced logouts and password resets.
	•	Security teams detect unexplained elevated privileges for a recently added vendor account.
	3.	SCADA Alarms & Automatic Shutdown
	•	Operators in the pipeline control room report repeated pressure fluctuations.
	•	A major pipeline loop segment shows forced valve closures in the ICS operator interface.
	•	SIS triggers a partial shutdown, claiming “High Pressure Anomaly” in one segment.
	4.	Refinery Control System Glitch
	•	Refinery unit operators notice setpoints on distillation columns and catalytic cracking units automatically reset to dangerously high or low thresholds.
	•	Communication from the data historian server becomes erratic; the server reboots unexpectedly multiple times.
	5.	External Inquiry from Regulator/Partner
	•	The local energy regulatory body requests an urgent meeting due to intelligence of a credible threat targeting national pipeline systems.
	•	A shipping partner complains that scheduled deliveries are delayed, citing unresponsive pipeline scheduling systems.
	6.	Threat Actor Statement or Discovery
	•	A short message or banner left on a compromised engineering workstation, stating that the facility is under “external control.”
	•	The security team recovers partial code fragments of ICS-specific malware from the DMZ logs, indicating a stealthy infiltration tailored for sabotage.
	7.	Emergency Response Escalation
	•	The Chief Information Security Officer (CISO) is informed that production must halt in certain units to investigate abnormal ICS commands.
	•	Senior leadership calls for crisis management procedures, prompting cross-functional teams (legal, PR, operations, safety, IT, HR) to assemble.
	8.	Financial Impact Projections
	•	CFO’s office demands immediate financial impact analysis for the downtime, referencing potential breach-of-contract penalties from commercial customers.
	•	Stock price begins to drop as rumors of a major cyber event circulate.
	9.	Forensic and IR Findings
	•	Preliminary forensics reveal malicious scripts that correlate with known APT TTPs.
	•	Malware includes modules specifically designed to interact with common ICS protocols (Modbus/TCP or OPC variants).

