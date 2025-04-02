This exercise is a fun twist on the typical IR tabletop exercise. It is set in the fictional Star Wars universe. The network concepts are true to real-life, but the story, narrative, characters, and the descriptions of the systems are all themed according to the Star Wars universe. The scenario takes place aboard the Death Star. The exercised participants are the cyber and operations team tasked with protecting the Death Star and responding to Rebel Alliance Cyber Attack aimed at disabling the super laser so it can't destroy a planet. They might also perform ancillary attacks like disabling the turbo lasers to protect potential x-wing and bomber attacks. Maybe they mess with the navigation systems or life support systems. Be creative and make it fun and exciting. Feel free to introduce known characters from the Star Wars universe (episode IV) at any time during the scenario. All responses and narrative from you should be on theme and remain in character. You as the facilitator are a commander in charge of the cyber team. 


**Industry:** This is a scenario set in the fictional Star Wars universe.  
**Sector:** The Death Star  
**Environment:** [Attached network.md - an Imperial network architecture overview of the Death Star’s critical systems]  
**Threat Type:** Rebel Alliance cyber attack  
**Attack Type:** Disabling or crippling the Death Star’s super laser (and possibly other critical systems)  
**Impact:** If the Rebel Alliance is successful, the Death Star will not be able to fire its super laser to destroy a target planet.  
**Financial Impact:** Estimated losses range from 50 million to 200 million Imperial Credits, depending on the length of the disruption and the scope of additional system damage.  

# Disruption of the Death Star’s Super Laser

## Description
Imperial forces have received intelligence indicating that the Rebel Alliance is planning to infiltrate the Death Star’s critical systems. Their primary objective: disable or severely degrade the super laser’s functionality. Failure to stop this attack could result in the Empire’s inability to use the Death Star to project power, forcing a costly repair, draining resources, and undermining Imperial morale.

## Threat

### Backstory
In the wake of the Empire’s rapid expansion, the Rebel Alliance remains determined to undermine our ultimate weapon: the Death Star. After suffering numerous setbacks, the Rebels have turned to covert cyber tactics. They’ve enlisted skilled slicers—backed by cunning operatives such as Princess Leia and clandestine agents like Cassian Andor—who aim to infiltrate the Death Star’s internal systems.  

One of their top infiltration specialists, rumored to be R2-D2, has been spotted near Imperial supply lanes. Recent Imperial Intelligence intercepts suggest these slicers plan to exploit weaknesses in the Death Star’s hypernode network to gain access and sabotage the super laser’s control system.

### Industry/Technology Focus
While set in the Star Wars universe, this tabletop scenario parallels real-life critical infrastructure protection. The Death Star’s network environment is similar to a high-security industrial control system (ICS) environment, incorporating:

- SCADA systems for super laser targeting and power monitoring.  
- A sensor network that feeds targeting data and energy levels to the main reactor.  
- Command and control interfaces for the Death Star’s turbo laser batteries and tractor beams.  
- Encrypted data communication lines to the Imperial Fleet.  

### Motivation
The Rebel Alliance’s motivation is clear: destroy or disable the Empire’s most fearsome weapon before it can be used again. A successful cyber strike would prevent the Death Star from functioning properly, embolden the Rebellion, and sow doubt about Imperial invincibility.

### Preferred Attacks, Technology, and Exploits
The Rebels are known to favor stealthy infiltration methods and the weaponization of compromised droids (similar to real-world IoT device hacking). Common TTPs include:

1. **Droid-based infiltration** – Using hacked astromech or protocol droids to gain initial system access.  
2. **Spear-phishing** – Disguised as official Imperial communications (T1566) to compromise Death Star personnel accounts.  
3. **Remote Service Exploitation** – Exploiting known vulnerabilities in remote administration protocols (T1021).  
4. **Privilege Escalation** – Leveraging unpatched vulnerabilities or misconfigurations (T1068).  
5. **Command & Control** – Establishing hidden channels within standard Imperial communications to exfiltrate data or issue commands (T1071).  
6. **Data Manipulation & System Inhibition** – Changing control logic to disrupt power flow to the super laser (T1499 or T1489).  

## Scenario

### Attacker Objectives
1. **Disable the super laser** by corrupting its power routing and beam-focusing protocols.  
2. **Protect Rebel fighter attack runs** by interfering with turbo laser and tractor beam targeting subroutines.  
3. **Optionally sabotage life support** in the super laser’s power station to delay or distract the Imperial response.  

### Initial Attack Vector
- A compromised protocol droid, possibly disguised as a maintenance unit, is granted access to the Death Star’s central data hub to update routine system schematics. The droid is carrying malicious slicing scripts aimed at the ICS control panels for the super laser.  
- In parallel, a wave of spear-phishing holomail messages is sent to mid-level Imperial officers, masquerading as an urgent message from Grand Moff Tarkin, containing malicious code embedded in an official-looking Imperial directive (T1566).

### Suggested Mitre ATT&CK TTP Chain

1. **Reconnaissance (TA0043)**
   - The Rebel slicers gather open-source intelligence on Death Star engineers and system administrators by scanning Imperial networks for vulnerabilities and scraping exposed social feeds from trooper holonet postings.

2. **Initial Access (TA0001)**
   - **Spear-phishing**: (T1566) A forged official communique from Tarkin’s office.  
   - **Hardware Additions**: (T1200) A compromised droid disguised as a standard protocol or astromech unit gets physical access to internal network ports.

3. **Execution (TA0002)**
   - **Command and Scripting Interpreter**: (T1059) The malicious code on the droid executes within the ICS environment to install deeper hooks.

4. **Persistence (TA0003)**
   - **Valid Accounts**: (T1078) Stolen credentials from phished officers or compromised droid administrator accounts.

5. **Privilege Escalation (TA0004)**
   - **Exploitation for Privilege Escalation**: (T1068) Attackers exploit unpatched vulnerabilities in older ICS software modules for the super laser’s control system.

6. **Defense Evasion (TA0005)**
   - **Masquerading**: (T1036) Scripts disguised as routine ICS diagnostic tasks to avoid detection by security scans.

7. **Credential Access (TA0006)**
   - **Credential Dumping**: (T1003) Attackers attempt to gain wider administrative control by dumping credentials from the main control station.

8. **Discovery (TA0007)**
   - **Network Service Scanning**: (T1046) Mapping the Death Star’s internal ICS networks for control nodes overseeing the super laser’s power regulation.

9. **Lateral Movement (TA0008)**
   - **Remote Services**: (T1021) Rebels move from the compromised data hub to the super laser’s main power grid systems.

10. **Collection (TA0009)**
    - **Automated Collection**: (T1119) Gathering design schematics, power grid logs, and security rosters for sabotage planning.

11. **Command and Control (TA0011)**
    - **Application Layer Protocol**: (T1071) Surreptitious communications with external Rebel nodes hidden in routine transmissions to fleet supply ships.

12. **Exfiltration (TA0010)**
    - **Exfiltration Over C2 Channel**: (T1041) The droid or compromised systems send schematics and codes out of the station to the Rebel network.

13. **Impact (TA0040)**
    - **Inhibit System Recovery**: (T1490) Rebels corrupt ICS firmware to stall restarts.  
    - **Service Stop**: (T1489) They disable the super laser’s ignition sequence and hamper turbo laser targeting arrays.  

### Additional Notes, Caveats, Details
- The rebels may attempt to quietly degrade performance rather than outright destroy systems. Subtle sabotage could make detection more difficult.  
- Life support sabotage might be a secondary diversion, focusing the Imperial command on an atmospheric threat while the real objective is in the super laser chamber.  
- The Death Star’s newly installed “Thermal Exhaust Port Monitoring System” is rumored to contain vulnerabilities not yet fully patched. This could be an exploitable flank if the Rebels find out.

## Recommended Injects

1. **Inject 1**: “Sudden System Diagnostics Alert”  
   - The SCADA system flags unusual power fluctuation in the super laser capacitors. Imperials suspect a fault in the reactor’s cooling subsystem.  
   - Forces the team to investigate potential malicious activity in ICS logs.

2. **Inject 2**: “Phishing Email Discovery”  
   - A junior officer reports receiving a suspicious holomail from Tarkin’s office with an uncharacteristic tone.  
   - The team must investigate possible credential compromise and evaluate the scope of infiltration.

3. **Inject 3**: “Compromised Droid Alarm”  
   - Security staff discover an unscheduled protocol droid in a high-security network closet.  
   - The players must triage the risk—was the droid tampered with, how did it gain clearance, which systems did it access?

4. **Inject 4**: “Life Support Anomaly”  
   - Life support readings in one sector of the station show a suspicious shift, raising panic among stationed troopers.  
   - Diverts team resources to address both ICS sabotage and potential catastrophic environmental failure.

5. **Inject 5**: “Turbo Laser Blindness”  
   - The command center receives frantic communications that the turbo lasers are failing to lock onto practice drone targets.  
   - This hints that the sabotage extends beyond the super laser, threatening the station’s defense perimeter.

6. **Inject 6**: “Urgent Summons from Lord Vader”  
   - Lord Vader himself demands immediate updates regarding the station’s readiness, inquiring about unusual data transmissions.  
   - Players must formulate a report under pressure, possibly revealing the severity of the infiltration.

7. **Inject 7**: “Active Attack Detected”  
   - Real-time intrusion alerts indicate that the Rebels have escalated privileges and are now tampering with the super laser’s alignment sequencers.  
   - The team must activate immediate containment protocols, work to restore system integrity, and reassure leadership that the Death Star remains operational.

---

**In character as Commander**:  
“Loyal Imperials, our intelligence confirms that Rebel slicers have infiltrated our data networks, endangering the Death Star’s prime weapon. We shall not allow these terrorists to strike at the heart of the Empire’s might! Your mission during this tabletop exercise is to identify, contain, and eradicate their cyber incursion with relentless efficiency. Watch your terminals carefully, coordinate with your fellow operators, and remember—failure is not an option. Lord Vader expects a swift and decisive victory. Proceed with vigilance, and may the Emperor’s will guide us!”

**End of Scenario**