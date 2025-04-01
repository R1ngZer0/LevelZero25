Below is an example of a well-segmented network environment aligned with the Purdue Reference Model for an electric utility organization operating generation, transmission, and distribution assets. It illustrates a single generation plant, a single transmission yard, and multiple distribution substations. The environment is sized to be “large” (at least 50 nodes) and includes both traditional enterprise/business networks and ICS/OT networks (e.g., PLCs, RTUs, HMIs, etc.).

⸻

Network Segments

Segment                                     Subnet

⸻

Corporate LAN (Level 4)                    10.10.10.0/24
SCADA DMZ (Level 3.5)                      10.10.20.0/24
Control Center LAN (Level 3)               10.10.30.0/24

Generation Plant ICS (Level 2)             10.10.40.0/24
Generation Plant Field (Levels 1/0)        10.10.50.0/24

Transmission Yard ICS (Level 2)            10.20.40.0/24
Transmission Yard Field (Levels 1/0)       10.20.50.0/24

Dist Substation #1 ICS (Level 2)           10.30.40.0/24
Dist Substation #1 Field (Levels 1/0)      10.30.50.0/24

Dist Substation #2 ICS (Level 2)           10.40.40.0/24
Dist Substation #2 Field (Levels 1/0)      10.40.50.0/24

Dist Substation #3 ICS (Level 2)           10.50.40.0/24
Dist Substation #3 Field (Levels 1/0)      10.50.50.0/24

⸻



⸻

Devices

Hostname              Purpose                                    MAC Address         IP Address         Subnet

⸻

Corporate LAN (Level 4) – 10.10.10.0/24

CORP-DC1              Domain Controller                           00:50:56:AA:10:01   10.10.10.10        10.10.10.0/24
CORP-DC2              Backup Domain Controller                    00:50:56:AA:10:02   10.10.10.11        10.10.10.0/24
CORP-FS1              File Server                                 00:50:56:AA:10:03   10.10.10.12        10.10.10.0/24
CORP-WS1              User Workstation                            00:50:56:AA:10:04   10.10.10.101       10.10.10.0/24
CORP-WS2              User Workstation                            00:50:56:AA:10:05   10.10.10.102       10.10.10.0/24
CORP-LT1              Corporate Laptop                            00:50:56:AA:10:06   10.10.10.103       10.10.10.0/24
CORP-Email            Email Server                                00:50:56:AA:10:07   10.10.10.20        10.10.10.0/24
CORP-Web              Intranet Web Server                         00:50:56:AA:10:08   10.10.10.30        10.10.10.0/24

SCADA DMZ (Level 3.5) – 10.10.20.0/24

DMZ-SCADA1            SCADA Gateway                               00:50:56:BB:20:01   10.10.20.10        10.10.20.0/24
DMZ-Historian         Data Historian Replica                      00:50:56:BB:20:02   10.10.20.20        10.10.20.0/24
DMZ-WSUS              Update Server                               00:50:56:BB:20:03   10.10.20.30        10.10.20.0/24
DMZ-AV                Anti-Virus Relay                            00:50:56:BB:20:04   10.10.20.40        10.10.20.0/24
DMZ-Syslog            Central Syslog/Log Server                   00:50:56:BB:20:05   10.10.20.50        10.10.20.0/24
DMZ-FW                Firewall/Proxy                              00:50:56:BB:20:FF   10.10.20.254       10.10.20.0/24

Control Center LAN (Level 3) – 10.10.30.0/24

CTRL-SCADA1           Primary SCADA Server                        00:50:56:CC:30:01   10.10.30.10        10.10.30.0/24
CTRL-SCADA2           Backup SCADA Server                         00:50:56:CC:30:02   10.10.30.11        10.10.30.0/24
CTRL-Engineer1        Engineering Workstation                     00:50:56:CC:30:03   10.10.30.21        10.10.30.0/24
CTRL-Historian        Data Historian                              00:50:56:CC:30:04   10.10.30.22        10.10.30.0/24
CTRL-NOC1             Network Operations Center Workstation       00:50:56:CC:30:05   10.10.30.31        10.10.30.0/24
CTRL-NOC2             Network Operations Center Workstation       00:50:56:CC:30:06   10.10.30.32        10.10.30.0/24
CTRL-FW               Control Center Firewall                     00:50:56:CC:30:FF   10.10.30.254       10.10.30.0/24

Generation Plant ICS (Level 2) – 10.10.40.0/24

GEN-PLC1              PLC for Turbine Control                     00:50:56:DD:40:01   10.10.40.10        10.10.40.0/24
GEN-PLC2              Backup PLC for Turbine Control              00:50:56:DD:40:02   10.10.40.11        10.10.40.0/24
GEN-HMI1              HMI Station                                 00:50:56:DD:40:03   10.10.40.20        10.10.40.0/24
GEN-HMI2              Backup/Redundant HMI Station                00:50:56:DD:40:04   10.10.40.21        10.10.40.0/24
GEN-WS-Maint          Maintenance Workstation                     00:50:56:DD:40:05   10.10.40.30        10.10.40.0/24
GEN-FW                Generation ICS Firewall                     00:50:56:DD:40:FF   10.10.40.254       10.10.40.0/24

Generation Plant Field (Levels 1/0) – 10.10.50.0/24

GEN-RTU1              RTU (Boiler Sensors)                        00:50:56:DD:50:01   10.10.50.10        10.10.50.0/24
GEN-RTU2              RTU (Steam Turbine Monitoring)              00:50:56:DD:50:02   10.10.50.11        10.10.50.0/24
GEN-IO1               I/O Module (Sensors & Actuators)            00:50:56:DD:50:03   10.10.50.20        10.10.50.0/24
GEN-IO2               I/O Module (Backup, Redundant)              00:50:56:DD:50:04   10.10.50.21        10.10.50.0/24

Transmission Yard ICS (Level 2) – 10.20.40.0/24

TRANS-PLC1            PLC (Transmission Breakers)                 00:50:56:EE:40:01   10.20.40.10        10.20.40.0/24
TRANS-HMI1            HMI Station                                 00:50:56:EE:40:02   10.20.40.20        10.20.40.0/24
TRANS-FW              Transmission ICS Firewall                   00:50:56:EE:40:FF   10.20.40.254       10.20.40.0/24

Transmission Yard Field (Levels 1/0) – 10.20.50.0/24

TRANS-RTU1            RTU (Line Monitoring)                       00:50:56:EE:50:01   10.20.50.10        10.20.50.0/24
TRANS-IO1             I/O Module (Circuit Breaker Sensors)        00:50:56:EE:50:02   10.20.50.20        10.20.50.0/24

Dist Substation #1 ICS (Level 2) – 10.30.40.0/24

DS1-PLC1              PLC (Feeder Control)                        00:50:56:AA:40:01   10.30.40.10        10.30.40.0/24
DS1-HMI1              Local HMI                                   00:50:56:AA:40:02   10.30.40.20        10.30.40.0/24
DS1-FW                Substation #1 ICS Firewall                  00:50:56:AA:40:FF   10.30.40.254       10.30.40.0/24

Dist Substation #1 Field (Levels 1/0) – 10.30.50.0/24

DS1-RTU1              RTU (Line Monitoring)                       00:50:56:AA:50:01   10.30.50.10        10.30.50.0/24

Dist Substation #2 ICS (Level 2) – 10.40.40.0/24

DS2-PLC1              PLC (Feeder Control)                        00:50:56:BB:40:01   10.40.40.10        10.40.40.0/24
DS2-FW                Substation #2 ICS Firewall                  00:50:56:BB:40:FF   10.40.40.254       10.40.40.0/24

Dist Substation #2 Field (Levels 1/0) – 10.40.50.0/24

DS2-RTU1              RTU (Line Monitoring)                       00:50:56:BB:50:01   10.40.50.10        10.40.50.0/24

Dist Substation #3 ICS (Level 2) – 10.50.40.0/24

DS3-PLC1              PLC (Feeder Control)                        00:50:56:CC:40:01   10.50.40.10        10.50.40.0/24
DS3-FW                Substation #3 ICS Firewall                  00:50:56:CC:40:FF   10.50.40.254       10.50.40.0/24

Dist Substation #3 Field (Levels 1/0) – 10.50.50.0/24

DS3-RTU1              RTU (Line Monitoring)                       00:50:56:CC:50:01   10.50.50.10        10.50.50.0/24

⸻



⸻

Connections

Below are some example connections illustrating typical data flows in this environment. (Note that real-world environments may have many more connections; these examples are for tabletop exercise reference.)

Source Hostname - IP : Port                          Destination Hostname - IP : Port

⸻

	1.	CORP-WS1 - 10.10.10.101:443   ——————>  CORP-Web - 10.10.10.30:443
(User accessing intranet)
	2.	CORP-WS2 - 10.10.10.102:3389 ——————>  CTRL-Engineer1 - 10.10.30.21:3389
(Remote engineering desktop session)
	3.	CTRL-SCADA1 - 10.10.30.10:502 —————–>  GEN-PLC1 - 10.10.40.10:502
(SCADA to PLC over Modbus/TCP)
	4.	CTRL-Historian - 10.10.30.22:1433 ———––>  DMZ-Historian - 10.10.20.20:1433
(Data replication between historians)
	5.	DMZ-SCADA1 - 10.10.20.10:443 ——————>  CTRL-SCADA1 - 10.10.30.10:443
(SCADA gateway communications)
	6.	GEN-HMI1 - 10.10.40.20:502  —————––>  GEN-PLC1 - 10.10.40.10:502
(Local HMI to PLC traffic)
	7.	TRANS-PLC1 - 10.20.40.10:2404 ––––––––>  TRANS-RTU1 - 10.20.50.10:2404
(IEC 104 communications for line status)
	8.	DS1-PLC1 - 10.30.40.10:20000 —————–>  DS1-RTU1 - 10.30.50.10:20000
(DNP3 communications for feeder control)
	9.	DS3-PLC1 - 10.50.40.10:44818 —————–>  DS3-RTU1 - 10.50.50.10:44818
(EtherNet/IP communications)
	10.	CORP-DC1 - 10.10.10.10:53  —————––>  CORP-WS1 - 10.10.10.101:53
(DNS requests from workstation to DC)

⸻

Use this environment description as a basis for tabletop incident response scenarios, focusing on how threats might pivot between segments or target critical control devices in generation, transmission, or distribution networks. Consider adding further detail (e.g., firewall rules, VLAN tags, advanced security controls) or adjusting to your organization’s specific architecture as needed.