Below is an example of a well-segmented network architecture, suitable for a Midstream/Downstream Oil & Gas environment (refinery plus dispersed pipelines), aligned with the Purdue Reference Model. The environment includes both business (IT) and industrial (OT/ICS) systems. This sample environment is large (over 50 devices) and can be used as a baseline for an Incident Response (IR) tabletop exercise.

⸻

Network Segments

Segment	Subnet
ICS Level 0/1 (Refinery)	192.168.10.0/24
ICS Level 2/3 (Refinery)	192.168.20.0/24
ICS DMZ (Refinery)	192.168.30.0/24
Pipeline ICS	192.168.40.0/24
Business/Enterprise Network	10.10.10.0/24
External/Corporate WAN	172.16.50.0/24



⸻

Devices

Below, devices are grouped by network segment. Each entry includes a brief purpose, a sample MAC address (fictitious), IP address, and subnet.

Hostname	Purpose	MAC Address	IP Address	Subnet
ICS Level 0/1 (192.168.10.0/24)				
PLC1	Refinery PLC controlling primary process	00:1A:C2:10:10:0A	192.168.10.10	192.168.10.0/24
PLC2	Refinery PLC (redundant/secondary)	00:1A:C2:10:10:0B	192.168.10.11	192.168.10.0/24
RTU1	Remote Terminal Unit for local instrumentation	00:1A:C2:10:10:0C	192.168.10.12	192.168.10.0/24
RTU2	Secondary RTU at refinery	00:1A:C2:10:10:0D	192.168.10.13	192.168.10.0/24
FieldSensor1	Temp/Pressure sensor (process feed)	00:1A:C2:10:10:0E	192.168.10.14	192.168.10.0/24
FieldSensor2	Flow sensor	00:1A:C2:10:10:0F	192.168.10.15	192.168.10.0/24
FieldSensor3	Additional sensor	00:1A:C2:10:10:10	192.168.10.16	192.168.10.0/24
PumpControl1	Motor/pump control interface	00:1A:C2:10:10:11	192.168.10.17	192.168.10.0/24

ICS Level 2/3 (192.168.20.0/24)
SCADA-Server1           | Primary SCADA server (Refinery)                  | 00:1A:C2:20:20:14 | 192.168.20.20   | 192.168.20.0/24
SCADA-Server2           | SCADA failover server                            | 00:1A:C2:20:20:15 | 192.168.20.21   | 192.168.20.0/24
HMI-Station1            | Operator HMI (Control Room)                      | 00:1A:C2:20:20:16 | 192.168.20.22   | 192.168.20.0/24
HMI-Station2            | Second operator HMI                              | 00:1A:C2:20:20:17 | 192.168.20.23   | 192.168.20.0/24
Eng-Workstation1        | Engineering workstation for PLC programming      | 00:1A:C2:20:20:18 | 192.168.20.24   | 192.168.20.0/24
ICS-FW1                 | Internal firewall between Level 0/1 and L2/3     | 00:1A:C2:20:20:19 | 192.168.20.25   | 192.168.20.0/24
ICS-Switch1             | Layer 2 switch (Refinery ICS core switch)        | 00:1A:C2:20:20:1A | 192.168.20.26   | 192.168.20.0/24
ICS-AV-Server           | Anti-virus server for ICS environment            | 00:1A:C2:20:20:1B | 192.168.20.27   | 192.168.20.0/24
ICS-IDS                 | Intrusion Detection Sensor for ICS               | 00:1A:C2:20:20:1C | 192.168.20.28   | 192.168.20.0/24

ICS DMZ (192.168.30.0/24)
DataHistorian1          | Process data historian                            | 00:1A:C2:30:30:1E | 192.168.30.30   | 192.168.30.0/24
DataHistorian2          | Secondary historian server                        | 00:1A:C2:30:30:1F | 192.168.30.31   | 192.168.30.0/24
ICS-WSUS-Server         | Windows update server for ICS                     | 00:1A:C2:30:30:20 | 192.168.30.32   | 192.168.30.0/24
ICS-PatchMgmt           | Patch management and deployment system           | 00:1A:C2:30:30:21 | 192.168.30.33   | 192.168.30.0/24
ICS-SecurityLogs        | Central log aggregator for ICS                    | 00:1A:C2:30:30:22 | 192.168.30.34   | 192.168.30.0/24
ICS-RemoteAccess        | Jump server / remote access gateway               | 00:1A:C2:30:30:23 | 192.168.30.35   | 192.168.30.0/24
ICS-AD-Proxy            | Limited Active Directory proxy for ICS accounts   | 00:1A:C2:30:30:24 | 192.168.30.36   | 192.168.30.0/24
ICS-DMZ-FW              | Firewall securing ICS DMZ to Business network     | 00:1A:C2:30:30:25 | 192.168.30.37   | 192.168.30.0/24
ICS-BackupServer        | Backup solution for ICS servers                   | 00:1A:C2:30:30:26 | 192.168.30.38   | 192.168.30.0/24

Pipeline ICS (192.168.40.0/24)
PLC-Pipeline1           | Pipeline PLC controlling valve stations          | 00:1A:C2:40:40:28 | 192.168.40.40   | 192.168.40.0/24
PLC-Pipeline2           | Backup PLC at pipeline station                   | 00:1A:C2:40:40:29 | 192.168.40.41   | 192.168.40.0/24
RTU-Pipeline1           | Pipeline RTU (flow & pressure monitoring)        | 00:1A:C2:40:40:2A | 192.168.40.42   | 192.168.40.0/24
RTU-Pipeline2           | Secondary RTU for redundancy                     | 00:1A:C2:40:40:2B | 192.168.40.43   | 192.168.40.0/24
FlowSensor1             | Pipeline flow sensor                              | 00:1A:C2:40:40:2C | 192.168.40.44   | 192.168.40.0/24
FlowSensor2             | Pipeline flow sensor                              | 00:1A:C2:40:40:2D | 192.168.40.45   | 192.168.40.0/24
Pipeline-HMI1           | HMI at remote pipeline station                   | 00:1A:C2:40:40:2E | 192.168.40.46   | 192.168.40.0/24
Pipeline-ControlStation | Central pipeline control node                    | 00:1A:C2:40:40:2F | 192.168.40.47   | 192.168.40.0/24
FlowSensor3             | Additional pipeline sensor                        | 00:1A:C2:40:40:30 | 192.168.40.48   | 192.168.40.0/24
Pipeline-EngStation     | Engineering workstation for pipeline PLCs        | 00:1A:C2:40:40:31 | 192.168.40.49   | 192.168.40.0/24

Business/Enterprise (10.10.10.0/24)
Corp-DC1                | Primary Domain Controller                        | 00:1A:C2:10:10:32 | 10.10.10.50      | 10.10.10.0/24
Corp-DC2                | Secondary Domain Controller                      | 00:1A:C2:10:10:33 | 10.10.10.51      | 10.10.10.0/24
Exchange-Server         | Corporate email server                           | 00:1A:C2:10:10:34 | 10.10.10.52      | 10.10.10.0/24
FileServer1             | Central file server                              | 00:1A:C2:10:10:35 | 10.10.10.53      | 10.10.10.0/24
Business-Laptop1        | Employee laptop                                  | 00:1A:C2:10:10:36 | 10.10.10.54      | 10.10.10.0/24
Business-Laptop2        | Employee laptop                                  | 00:1A:C2:10:10:37 | 10.10.10.55      | 10.10.10.0/24
HR-Workstation1         | HR department desktop                            | 00:1A:C2:10:10:38 | 10.10.10.56      | 10.10.10.0/24
CFO-Workstation         | CFO’s main workstation                           | 00:1A:C2:10:10:39 | 10.10.10.57      | 10.10.10.0/24
CEO-Workstation         | CEO’s main workstation                           | 00:1A:C2:10:10:3A | 10.10.10.58      | 10.10.10.0/24
Finance-Server          | Financial application server                     | 00:1A:C2:10:10:3B | 10.10.10.59      | 10.10.10.0/24

External/Corporate WAN (172.16.50.0/24)
Perimeter-FW            | Perimeter firewall (Internet boundary)           | 00:1A:C2:50:50:3C | 172.16.50.60     | 172.16.50.0/24
VPN-Gateway             | VPN gateway for remote access                    | 00:1A:C2:50:50:3D | 172.16.50.61     | 172.16.50.0/24
Web-Server              | Public-facing web server                         | 00:1A:C2:50:50:3E | 172.16.50.62     | 172.16.50.0/24
Remote-AdminLaptop      | Remote admin’s laptop (VPN user)                 | 00:1A:C2:50:50:3F | 172.16.50.63     | 172.16.50.0/24
Email-Gateway           | Email relay/gateway                              | 00:1A:C2:50:50:40 | 172.16.50.64     | 172.16.50.0/24
External-Router         | Edge router to ISP                               | 00:1A:C2:50:50:41 | 172.16.50.65     | 172.16.50.0/24

⸻

Connections

Below are sample connections that illustrate typical traffic flows between hosts:

Source Hostname-IP-Port	Destination Hostname-IP-Port
PLC1 (192.168.10.10:502)	SCADA-Server1 (192.168.20.20:502)
SCADA-Server1 (192.168.20.20:1433)	DataHistorian1 (192.168.30.30:1433)
Eng-Workstation1 (192.168.20.24:3389)	SCADA-Server1 (192.168.20.20:3389)
ICS-FW1 (192.168.20.25:443)	ICS-DMZ-FW (192.168.30.37:443)
ICS-RemoteAccess (192.168.30.35:3389)	Pipeline-ControlStation (192.168.40.47:3389)
SCADA-Server2 (192.168.20.21:502)	PLC-Pipeline1 (192.168.40.40:502)
Business-Laptop1 (10.10.10.54:445)	FileServer1 (10.10.10.53:445)
CFO-Workstation (10.10.10.57:1433)	Finance-Server (10.10.10.59:1433)
Exchange-Server (10.10.10.52:25)	Email-Gateway (172.16.50.64:25)
Perimeter-FW (172.16.50.60:443)	External-Router (172.16.50.65:443)
Remote-AdminLaptop (172.16.50.63:443)	VPN-Gateway (172.16.50.61:443)
HMI-Station1 (192.168.20.22:502)	PLC2 (192.168.10.11:502)

Notes:
	•	Ports shown (e.g., 502 for Modbus, 3389 for RDP, 445 for SMB, 25 for SMTP, 1433 for SQL) reflect typical protocols in ICS and business environments.
	•	Firewalls between levels regulate traffic based on the organization’s security policies.
	•	Additional connections (e.g., ICS patching, AD authentication, internal DNS, etc.) would occur within and across the defined segments.
	•	This table is an illustrative snapshot; real environments may have more complex routing, VLANs, or additional security devices (IDS/IPS, etc.).

