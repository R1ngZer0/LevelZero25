Industry: Electric Utility
Sector: Generation
Threat Type: State-Sponsored Advanced Persistent Threat (APT)
Attack Type: Coordinated ICS Disruption (Sabotage / Service Interruption)
Impact: Partial disruption of power generation, leading to brownouts/rolling outages
Financial Impact: Ranges from $5M - $50M depending on length of outages, remediation, and contractual penalties

⸻

Scenario: “Twilight Surge”

Description

This exercise explores how a sophisticated, state-sponsored threat actor targets a power generation company, seeking to disrupt its industrial control systems (ICS) with the ultimate goal of causing intermittent outages. Participants will walk through the detection, containment, and recovery processes, focusing on rapid decision-making in high-pressure operational environments. This scenario is rooted in real-world tactics from the MITRE ATT&CK for ICS framework (and some overlapping Enterprise TTPs for the IT portion).

⸻

Threat

Backstory

A suspected nation-state APT group has been quietly assessing and probing various energy sector entities over the last 18 months. Having previously tested the waters with smaller intrusions in regional distribution systems, the attackers now set their sights on a key generation facility that supplies power to a critical metro area. Intelligence sources suggest they are attempting to disrupt national infrastructure for political leverage. Their tradecraft includes ICS-specific malware modules, knowledge of power generation processes, and advanced stealth capabilities.

Industry/Technology Focus
	1.	Industrial Control Systems for hydro and gas-fired turbine generators
	2.	SCADA (Supervisory Control and Data Acquisition) systems integrated with the corporate network
	3.	Engineering Workstations (for PLC and RTU programming)
	4.	Historian Databases storing operational data, performance logs, and system engineering design

Motivation
	•	Geopolitical Leverage: Adversary seeks to weaken the target nation’s economy and create unrest.
	•	Disruption & Espionage: The attacker aims to collect sensitive operation data and, at the right moment, disrupt power production.

Preferred Attacks, Technology, and Exploits
	•	Spear Phishing for Initial Access (Enterprise ATT&CK: T1566.001): Using carefully crafted emails leveraging internal jargon and references.
	•	ICS Reconnaissance (ICS ATT&CK: T0842 – System Information Discovery): Utilizing compromised user accounts to explore the environment and identify ICS components.
	•	Privilege Escalation & Lateral Movement (Enterprise ATT&CK: T1078, T1550, ICS ATT&CK: T0886): Harvesting credentials and exploiting Windows services or Active Directory.
	•	Command & Control using custom malware beacons that disguise traffic as legitimate system management protocols.
	•	Manipulation of Control Logic (ICS ATT&CK: T0831, T0879): Inserting malicious code or parameters into PLC/RTU logic to interfere with turbine regulation and generator synchronization.

⸻

Scenario

Attacker Objectives
	1.	Disrupt Power Generation: Trigger intermittent shutdowns and restarts of turbines.
	2.	Damage Equipment (if feasible): Inject malicious parameters to reduce the life span of critical components.
	3.	Undermine Confidence: Erode public trust in the reliability and security of the power grid.

Initial Attack Vector
	•	Spear Phishing: A senior engineer in charge of turbine maintenance receives an email with a malicious Excel attachment labeled “Urgent Maintenance Schedules.” The attachment contains a macro that exploits a known vulnerability (Enterprise ATT&CK: T1137.001 – Office Application Startup). Once enabled, it downloads a remote access trojan (RAT) and establishes Command & Control.

Suggested MITRE ATT&CK TTP Chain

Below is a sample chain integrating both MITRE ATT&CK for Enterprise (for the IT side) and ICS (for the operational side).
	1.	Reconnaissance
	•	ICS ATT&CK: T0842 – System Information Discovery: Adversary identifies ICS devices, PLCs, and engineering workstations.
	2.	Initial Access
	•	Enterprise ATT&CK: T1566.001 – Spearphishing Attachment
	3.	Execution
	•	Enterprise ATT&CK: T1204.002 – Malicious File (macro execution in Excel)
	4.	Persistence
	•	Enterprise ATT&CK: T1547 – Boot or Logon Autostart Execution (adding malicious registry entries on the engineer’s workstation).
	5.	Privilege Escalation
	•	Enterprise ATT&CK: T1078 – Valid Accounts (compromising additional domain credentials via harvested hashes).
	6.	Defense Evasion
	•	Enterprise ATT&CK: T1562.001 – Disable or Modify Tools (disabling AV or modifying logs).
	7.	Lateral Movement
	•	Enterprise ATT&CK: T1021.002 – SMB/Windows Admin Shares (moving from corporate network to ICS segment).
	•	ICS ATT&CK: T0886 – Remote System Discovery (moving through ICS network).
	8.	Collection
	•	ICS ATT&CK: T0843 – Data from Information Repositories (historian logs, engineering design documents).
	9.	Command & Control
	•	Enterprise ATT&CK: T1071 – Application Layer Protocol (encrypted channels over common ports).
	10.	Inhibit Response Function

	•	ICS ATT&CK: T0814 – Alarm Suppression (attempting to suppress or delay alarm triggers).

	11.	Impact

	•	ICS ATT&CK: T0831 – Manipulation of Control (changing generator control logic).
	•	ICS ATT&CK: T0879 – Modify Control Logic (plant disruptions or forced shutdowns).

Additional Notes, Caveats, Details (If Applicable)
	•	The attackers maintain stealth until they are ready to act, often timing the final disruption event with peak demand (e.g., heatwave or cold snap).
	•	The ICS environment may not be fully isolated from the corporate network, which increases risk.
	•	Legacy systems with unpatched vulnerabilities or default credentials can significantly accelerate lateral movement.
	•	Because the attackers also exfiltrate data (e.g., engineering designs, shift schedules), significant brand and legal ramifications exist beyond the immediate operational impact.

⸻

Recommended Injects
	1.	Phishing Email & Malicious Attachment
	•	Inject: Send an email message to participants with an urgent “Maintenance Schedules” Excel file. When the participant opens it, an alert from the security team indicates macros were enabled, and suspicious outbound connections are detected.
	•	Outcome: Sparks discussion on email security, user awareness, and incident response procedures for containment.
	2.	Unusual Traffic Detected
	•	Inject: A corporate IDS alert for “multiple failed logins from a known engineer’s account.” Intrusion detection logs show attempts to connect from a newly provisioned VM in the environment.
	•	Outcome: Encourages participants to pivot into investigating compromised credentials, potential lateral movement.
	3.	Engineering Workstation Alert
	•	Inject: SCADA operator sees unexpected parameter changes on the HMI, followed by a forced restart of a turbine. Alarm notifications come in bursts and then abruptly stop, indicating potential alarm suppression.
	•	Outcome: Tests detection capabilities and ICS operational response—who’s notified, how quickly systems can be isolated, roles/responsibilities in ICS environment.
	4.	Suspicious PLC Logic Change
	•	Inject: ICS engineers find a new rung of ladder logic on the main turbine PLC. The logic is set to intermittently lower lubrication rates.
	•	Outcome: Forces detailed discussion on PLC version control, ICS change management, and the steps for verifying/rolling back control logic changes.
	5.	Financial & Regulatory Pressure
	•	Inject: Executive management informs the IR team that multiple customers are complaining about brownouts. Media coverage intensifies. Regulators demand status reports.
	•	Outcome: Triggers crisis communication protocols, coordination with regulatory bodies, and an accelerated response timeline.
	6.	Potential Insider Involvement
	•	Inject: Evidence surfaces that a disgruntled plant technician may have facilitated the phishing or provided initial ICS architecture diagrams.
	•	Outcome: Tests internal security controls and background checks, expands the scope of the investigation beyond purely external threats.
	7.	Supply Chain Indicator
	•	Inject: Newly discovered intelligence from a partner vendor reveals a known threat group compromised their software update server. The ICS environment recently downloaded a new module from that vendor.
	•	Outcome: Explores supply chain compromise mitigation, third-party risk management, and vendor relationship protocols.
	8.	Recovery Steps
	•	Inject: ICS vendor recommends performing full “cold start” on certain turbines to ensure no hidden malicious logic remains. This action would require at least 8 hours of downtime.
	•	Outcome: Forces participants to weigh downtime costs vs. security needs and to test their operational continuity plan.